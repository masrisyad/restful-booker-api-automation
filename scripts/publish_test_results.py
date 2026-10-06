import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import (  # noqa: E402
    JIRA_API_TOKEN,
    JIRA_BASE_URL,
    JIRA_EMAIL,
    R2_ACCESS_KEY_ID,
    R2_ACCOUNT_ID,
    R2_BUCKET_NAME,
    R2_PUBLIC_BASE_URL,
    R2_SECRET_ACCESS_KEY,
    REQUEST_TIMEOUT,
)
from src.integrations.jira_client import JiraClient, JiraConfig  # noqa: E402
from src.integrations.r2_storage import R2Config, R2Storage  # noqa: E402
from src.reporting import ExecutionMetadata, parse_junit_report, render_stakeholder_report  # noqa: E402


ISSUE_KEY_PATTERN = re.compile(r"\b([A-Z][A-Z0-9]+-\d+)\b", re.IGNORECASE)


def extract_issue_key(*candidates):
    for candidate in candidates:
        match = ISSUE_KEY_PATTERN.search(candidate or "")
        if match:
            return match.group(1).upper()
    return ""


def read_github_event(path):
    if not path:
        return {}
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def build_metadata(explicit_issue_key=""):
    event = read_github_event(os.getenv("GITHUB_EVENT_PATH"))
    pull_request = event.get("pull_request") or {}
    head = pull_request.get("head") or {}
    title = pull_request.get("title", "")
    commit_message = (event.get("head_commit") or {}).get("message", "")

    branch = (
        os.getenv("GITHUB_HEAD_REF")
        or head.get("ref")
        or os.getenv("GITHUB_REF_NAME")
        or os.getenv("GIT_BRANCH")
        or "local"
    )
    issue_key = extract_issue_key(explicit_issue_key, branch, title, commit_message)
    server_url = os.getenv("GITHUB_SERVER_URL", "https://github.com")
    repository = os.getenv("GITHUB_REPOSITORY", "local")
    run_id = os.getenv("GITHUB_RUN_ID", "local")
    run_url = ""
    if run_id != "local" and repository != "local":
        run_url = f"{server_url}/{repository}/actions/runs/{run_id}"

    return ExecutionMetadata(
        repository=repository,
        branch=branch,
        commit_sha=os.getenv("GITHUB_SHA", "local"),
        run_url=run_url,
        run_id=run_id,
        run_attempt=os.getenv("GITHUB_RUN_ATTEMPT", "1"),
        issue_key=issue_key,
        generated_at=datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
    )


def _safe_segment(value):
    segment = re.sub(r"[^A-Za-z0-9._-]+", "-", value or "").strip("-._")
    return segment or "untracked"


def build_object_prefix(metadata):
    repository_name = metadata.repository.rsplit("/", 1)[-1]
    run = f"{_safe_segment(metadata.run_id)}-{_safe_segment(metadata.run_attempt)}"
    return "/".join(
        (
            _safe_segment(repository_name),
            _safe_segment(metadata.issue_key or "untracked"),
            run,
        )
    )


def _adf_paragraph(text, *, strong=False):
    text_node = {"type": "text", "text": text}
    if strong:
        text_node["marks"] = [{"type": "strong"}]
    return {"type": "paragraph", "content": [text_node]}


def _adf_link_paragraph(label, url):
    return {
        "type": "paragraph",
        "content": [
            {
                "type": "text",
                "text": label,
                "marks": [{"type": "link", "attrs": {"href": url}}],
            }
        ],
    }


def build_jira_comment(summary, metadata, report_url):
    content = [
        _adf_paragraph(f"API Automation: {summary.status_label}", strong=True),
        _adf_paragraph(f"Suite: {summary.suite}"),
        _adf_paragraph(
            f"Total: {summary.total} | Lulus: {summary.passed} | "
            f"Gagal: {summary.failed} | Error: {summary.errors} | "
            f"Dilewati: {summary.skipped}"
        ),
        _adf_paragraph(f"Durasi: {summary.duration:.3f} detik"),
        _adf_paragraph(summary.conclusion),
        _adf_paragraph(
            f"Repository: {metadata.repository} | Branch: {metadata.branch} | "
            f"Commit: {metadata.commit_sha}"
        ),
        _adf_link_paragraph("Buka laporan lengkap", report_url),
    ]
    if metadata.run_url:
        content.append(_adf_link_paragraph("Buka GitHub Actions", metadata.run_url))

    return {"type": "doc", "version": 1, "content": content}


def publish_reports(summary, metadata, report_paths):
    r2_config = R2Config(
        account_id=R2_ACCOUNT_ID or "",
        access_key_id=R2_ACCESS_KEY_ID or "",
        secret_access_key=R2_SECRET_ACCESS_KEY or "",
        bucket_name=R2_BUCKET_NAME or "",
        public_base_url=R2_PUBLIC_BASE_URL or "",
    )
    if not r2_config.validate():
        print("R2 publication dilewati: konfigurasi belum tersedia.")
        return ""

    storage = R2Storage(r2_config)
    prefix = build_object_prefix(metadata)
    uploads = (
        (report_paths["stakeholder"], "stakeholder-report.html", "text/html; charset=utf-8"),
        (report_paths["technical"], "report.html", "text/html; charset=utf-8"),
        (report_paths["junit"], "junit.xml", "application/xml; charset=utf-8"),
    )
    report_url = ""
    uploaded_count = 0
    for file_path, file_name, content_type in uploads:
        if not Path(file_path).is_file():
            print(f"Upload dilewati: {file_name} tidak tersedia.")
            continue
        url = storage.upload(file_path, f"{prefix}/{file_name}", content_type)
        uploaded_count += 1
        if file_name == "stakeholder-report.html":
            report_url = url
    if not report_url:
        raise RuntimeError("Stakeholder report gagal diunggah ke R2")
    print(f"{uploaded_count} report berhasil diunggah ke Cloudflare R2.")
    return report_url


def notify_jira(summary, metadata, report_url):
    config = JiraConfig(
        base_url=JIRA_BASE_URL or "",
        email=JIRA_EMAIL or "",
        api_token=JIRA_API_TOKEN or "",
        timeout=REQUEST_TIMEOUT,
    )
    if not config.validate():
        print("Notifikasi Jira dilewati: konfigurasi belum tersedia.")
        return False
    if not metadata.issue_key:
        print("Notifikasi Jira dilewati: issue key tidak terdeteksi.")
        return False
    if not report_url:
        raise RuntimeError("Notifikasi Jira memerlukan URL report R2")

    comment = build_jira_comment(summary, metadata, report_url)
    JiraClient(config).add_comment(metadata.issue_key, comment)
    print(f"Ringkasan test dikirim ke Jira untuk {metadata.issue_key}.")
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description="Render dan publish hasil test API")
    parser.add_argument("--junit", default="reports/junit.xml")
    parser.add_argument("--technical-report", default="reports/report.html")
    parser.add_argument("--output", default="reports/stakeholder-report.html")
    parser.add_argument("--suite", default=os.getenv("TEST_SUITE", "all"))
    parser.add_argument("--issue-key", default=os.getenv("JIRA_ISSUE_KEY", ""))
    parser.add_argument("--render-only", action="store_true")
    args = parser.parse_args(argv)

    metadata = build_metadata(args.issue_key)
    summary = parse_junit_report(args.junit, suite=args.suite)
    render_stakeholder_report(summary, metadata, args.output)
    print(f"Stakeholder report dibuat: {args.output}")

    if args.render_only:
        return 0

    report_paths = {
        "stakeholder": args.output,
        "technical": args.technical_report,
        "junit": args.junit,
    }
    report_url = publish_reports(summary, metadata, report_paths)
    notify_jira(summary, metadata, report_url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
