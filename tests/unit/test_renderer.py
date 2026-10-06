from src.reporting.models import (
    ExecutionMetadata,
    TestCaseResult as CaseResult,
    TestSummary as Summary,
)
from src.reporting.renderer import render_stakeholder_report


def test_render_stakeholder_report_escapes_untrusted_content(tmp_path):
    summary = Summary(
        suite="smoke<script>",
        tests=[
            CaseResult(
                node_id="tests::test_bad",
                name="Bad <script>alert(1)</script>",
                suite="smoke",
                status="failed",
                duration=1.25,
                message="Expected <200>",
                details="<img src=x onerror=alert(1)>",
            )
        ],
    )
    metadata = ExecutionMetadata(
        repository="owner/repo",
        branch="RBA-20-report",
        commit_sha="abcdef1234567890",
        run_url="https://github.com/owner/repo/actions/runs/1",
        issue_key="RBA-20",
        generated_at="2026-10-07T10:00:00+07:00",
    )
    output = tmp_path / "stakeholder.html"

    render_stakeholder_report(summary, metadata, output)
    html = output.read_text(encoding="utf-8")

    assert "Hasil Pengujian API" in html
    assert "GAGAL" in html
    assert "Ada 1 pengujian gagal atau error" in html
    assert "Bad &lt;script&gt;alert(1)&lt;/script&gt;" in html
    assert "<img src=x" not in html
    assert "RBA-20" in html


def test_render_stakeholder_report_shows_infrastructure_error(tmp_path):
    summary = Summary(suite="all", infrastructure_error="JUnit rusak")
    output = tmp_path / "stakeholder.html"

    render_stakeholder_report(summary, ExecutionMetadata(), output)
    html = output.read_text(encoding="utf-8")

    assert "Kendala eksekusi" in html
    assert "JUnit rusak" in html
    assert "ERROR" in html
