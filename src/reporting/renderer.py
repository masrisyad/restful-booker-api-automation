from html import escape
from pathlib import Path

from src.reporting.models import ExecutionMetadata, TestSummary


_STATUS_LABELS = {
    "passed": "Lulus",
    "failed": "Gagal",
    "error": "Error",
    "skipped": "Dilewati",
}


def _format_duration(seconds):
    if seconds < 1:
        return f"{seconds * 1000:.0f} ms"
    return f"{seconds:.2f} detik"


def _test_rows(summary):
    rows = []
    for test in summary.tests:
        details = ""
        if test.message or test.details:
            technical_text = "\n\n".join(part for part in (test.message, test.details) if part)
            details = (
                '<details><summary>Lihat detail teknis</summary>'
                f'<pre>{escape(technical_text)}</pre></details>'
            )
        rows.append(
            "<tr>"
            f'<td><strong>{escape(test.name)}</strong><small>{escape(test.node_id)}</small>{details}</td>'
            f'<td><span class="test-status {escape(test.status)}">{_STATUS_LABELS[test.status]}</span></td>'
            f'<td class="number">{_format_duration(test.duration)}</td>'
            "</tr>"
        )
    return "".join(rows)


def render_stakeholder_report(summary, metadata, output_path):
    if not isinstance(summary, TestSummary):
        raise TypeError("summary must be a TestSummary")
    if not isinstance(metadata, ExecutionMetadata):
        raise TypeError("metadata must be an ExecutionMetadata")

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    status = summary.status
    generated_at = metadata.generated_at or "Tidak tersedia"
    run_link = (
        f'<a href="{escape(metadata.run_url, quote=True)}">Buka GitHub Actions</a>'
        if metadata.run_url
        else "Eksekusi lokal"
    )
    infrastructure_error = ""
    if summary.infrastructure_error:
        infrastructure_error = (
            '<section class="notice" aria-labelledby="technical-error">'
            '<h2 id="technical-error">Kendala eksekusi</h2>'
            f'<p>{escape(summary.infrastructure_error)}</p></section>'
        )

    html = f"""<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Hasil Pengujian API</title>
<style>
/* Control-room layout: verdict first, evidence second, technical trace last. */
:root {{
  --bg: #eef3f7; --surface: #ffffff; --surface-alt: #e8eef3;
  --ink: #14212b; --muted: #536472; --line: #c5d1da; --accent: #145f82;
  --good: #176b45; --good-soft: #dff3e8; --bad: #a12b34; --bad-soft: #f9e3e5;
  --warn: #8a5700; --warn-soft: #fff0ce; --shadow: rgba(22, 48, 64, .12);
  --display: Georgia, "Times New Roman", serif;
  --body: "Segoe UI", Arial, sans-serif; --data: Consolas, "Courier New", monospace;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --bg: #0f181f; --surface: #17242d; --surface-alt: #21313c;
    --ink: #eef5f8; --muted: #afbdc6; --line: #3b4e5a; --accent: #76c0df;
    --good: #79d6a5; --good-soft: #173d2b; --bad: #ff9ca3; --bad-soft: #4b2428;
    --warn: #f5ca72; --warn-soft: #4a3718; --shadow: rgba(0, 0, 0, .3); color-scheme: dark;
  }}
}}
:root[data-theme="dark"] {{
  --bg: #0f181f; --surface: #17242d; --surface-alt: #21313c;
  --ink: #eef5f8; --muted: #afbdc6; --line: #3b4e5a; --accent: #76c0df;
  --good: #79d6a5; --good-soft: #173d2b; --bad: #ff9ca3; --bad-soft: #4b2428;
  --warn: #f5ca72; --warn-soft: #4a3718; --shadow: rgba(0, 0, 0, .3); color-scheme: dark;
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--bg); color: var(--ink); font-family: var(--body); line-height: 1.55; padding-inline: 16px; padding-block: 32px 64px; }}
a {{ color: var(--accent); font-weight: 650; }}
a:focus-visible, summary:focus-visible {{ outline: 3px solid var(--accent); outline-offset: 3px; }}
main {{ width: min(1080px, 100%); margin: 0 auto; display: grid; gap: 24px; }}
.hero {{ background: var(--surface); border-top: 8px solid var(--accent); box-shadow: 0 12px 34px var(--shadow); padding: clamp(24px, 5vw, 52px); display: grid; gap: 24px; }}
.eyebrow {{ color: var(--muted); font: 700 .75rem/1.2 var(--data); letter-spacing: .11em; text-transform: uppercase; }}
.verdict {{ display: flex; align-items: center; gap: 14px; flex-wrap: wrap; }}
h1 {{ font: 700 clamp(2rem, 6vw, 4.2rem)/.98 var(--display); margin: 0; letter-spacing: -.035em; text-wrap: balance; }}
.badge {{ border: 2px solid currentColor; padding: 6px 12px; font: 800 .82rem/1 var(--data); letter-spacing: .08em; }}
.badge.passed {{ color: var(--good); background: var(--good-soft); }}
.badge.failed, .badge.error {{ color: var(--bad); background: var(--bad-soft); }}
.conclusion {{ max-width: 68ch; font-size: 1.08rem; margin: 0; }}
.meta {{ display: flex; flex-wrap: wrap; gap: 10px 24px; color: var(--muted); font-size: .88rem; }}
.meta code {{ color: var(--ink); font-family: var(--data); overflow-wrap: anywhere; }}
.stats {{ display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 2px; background: var(--line); border: 1px solid var(--line); }}
.stat {{ background: var(--surface); padding: 20px; min-width: 0; }}
.stat .label {{ color: var(--muted); font: 700 .72rem/1.2 var(--data); letter-spacing: .07em; text-transform: uppercase; }}
.stat .value {{ display: block; margin-top: 6px; font: 700 clamp(1.5rem, 4vw, 2.5rem)/1 var(--display); font-variant-numeric: tabular-nums; }}
section.panel, section.notice {{ background: var(--surface); border: 1px solid var(--line); padding: clamp(20px, 4vw, 36px); min-width: 0; }}
section.notice {{ border-left: 6px solid var(--bad); background: var(--bad-soft); }}
h2 {{ font: 700 clamp(1.35rem, 3vw, 1.8rem)/1.15 var(--display); margin: 0 0 18px; text-wrap: balance; }}
.table-wrap {{ overflow-x: auto; }}
table {{ width: 100%; border-collapse: collapse; min-width: 650px; }}
th {{ color: var(--muted); font: 700 .72rem/1.2 var(--data); letter-spacing: .07em; text-align: left; text-transform: uppercase; border-bottom: 2px solid var(--line); padding: 12px; }}
td {{ border-bottom: 1px solid var(--line); padding: 16px 12px; vertical-align: top; }}
td small {{ display: block; color: var(--muted); font-family: var(--data); margin-top: 3px; overflow-wrap: anywhere; }}
td.number {{ font-family: var(--data); font-variant-numeric: tabular-nums; white-space: nowrap; }}
.test-status {{ font: 800 .75rem/1 var(--data); text-transform: uppercase; }}
.test-status.passed {{ color: var(--good); }} .test-status.failed, .test-status.error {{ color: var(--bad); }} .test-status.skipped {{ color: var(--warn); }}
details {{ margin-top: 12px; }} summary {{ color: var(--accent); cursor: pointer; font-weight: 650; }}
pre {{ max-width: 100%; overflow-x: auto; white-space: pre-wrap; overflow-wrap: anywhere; background: var(--surface-alt); border: 1px solid var(--line); padding: 14px; font: .78rem/1.55 var(--data); }}
.empty {{ color: var(--muted); }}
footer {{ color: var(--muted); font-size: .82rem; border-top: 1px solid var(--line); padding-top: 18px; }}
@media (max-width: 720px) {{ .stats {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
@media (max-width: 420px) {{ body {{ padding-block: 16px 40px; }} .stats {{ grid-template-columns: 1fr; }} }}
@media print {{ body {{ background: var(--surface); }} .hero {{ box-shadow: none; }} }}
</style>
</head>
<body>
<main>
  <header class="hero">
    <span class="eyebrow">Laporan pengujian otomatis · {escape(summary.suite)}</span>
    <div class="verdict"><h1>Hasil Pengujian API</h1><span class="badge {status}">{summary.status_label}</span></div>
    <p class="conclusion">{escape(summary.conclusion)}</p>
    <div class="meta">
      <span>Waktu: <code>{escape(generated_at)}</code></span>
      <span>Branch: <code>{escape(metadata.branch)}</code></span>
      <span>Commit: <code>{escape(metadata.commit_sha[:12])}</code></span>
      <span>{run_link}</span>
    </div>
  </header>
  <section class="stats" aria-label="Ringkasan hasil">
    <div class="stat"><span class="label">Total</span><span class="value">{summary.total}</span></div>
    <div class="stat"><span class="label">Lulus</span><span class="value">{summary.passed}</span></div>
    <div class="stat"><span class="label">Gagal</span><span class="value">{summary.failed}</span></div>
    <div class="stat"><span class="label">Error</span><span class="value">{summary.errors}</span></div>
    <div class="stat"><span class="label">Dilewati</span><span class="value">{summary.skipped}</span></div>
    <div class="stat"><span class="label">Durasi</span><span class="value">{_format_duration(summary.duration)}</span></div>
  </section>
  {infrastructure_error}
  <section class="panel" aria-labelledby="test-detail">
    <h2 id="test-detail">Detail pengujian</h2>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Pengujian</th><th>Status</th><th>Durasi</th></tr></thead>
        <tbody>{_test_rows(summary) or '<tr><td colspan="3" class="empty">Tidak ada hasil test yang dapat ditampilkan.</td></tr>'}</tbody>
      </table>
    </div>
  </section>
  <footer>Report otomatis · Repository {escape(metadata.repository)} · Issue {escape(metadata.issue_key or "tidak terdeteksi")} · Dilewati {summary.skipped}</footer>
</main>
</body>
</html>
"""
    output.write_text(html, encoding="utf-8")
    return output
