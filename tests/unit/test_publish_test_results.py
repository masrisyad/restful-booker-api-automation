from unittest.mock import Mock

import pytest

from src.reporting.models import (
    ExecutionMetadata,
    TestCaseResult as CaseResult,
    TestSummary as Summary,
)
import scripts.publish_test_results as publish_module
from scripts.publish_test_results import (
    build_jira_comment,
    build_object_prefix,
    extract_issue_key,
)


def test_extract_issue_key_uses_first_matching_candidate():
    assert extract_issue_key("RBA-20", "RBA-99-other") == "RBA-20"
    assert extract_issue_key("", "feature/rba-21-report") == "RBA-21"
    assert extract_issue_key("no ticket") == ""


def test_object_prefix_is_immutable_and_sanitized():
    metadata = ExecutionMetadata(
        repository="owner/restful-booker-api-automation",
        issue_key="RBA-20",
        run_id="12345",
        run_attempt="2",
    )

    assert build_object_prefix(metadata) == (
        "restful-booker-api-automation/RBA-20/12345-2"
    )


def test_jira_comment_contains_stakeholder_summary_and_links():
    summary = Summary(
        suite="smoke",
        tests=[
            CaseResult(
                node_id="tests::test_health",
                name="Health",
                suite="smoke",
                status="passed",
                duration=0.2,
            )
        ],
    )
    metadata = ExecutionMetadata(
        repository="owner/repo",
        branch="RBA-20-report",
        commit_sha="abc",
        run_url="https://github.com/owner/repo/actions/runs/1",
        issue_key="RBA-20",
    )
    report_url = "https://reports.example.com/report.html"

    comment = build_jira_comment(summary, metadata, report_url)
    serialized = str(comment)

    assert comment["type"] == "doc"
    assert comment["version"] == 1
    assert "API Automation: LULUS" in serialized
    assert "Total: 1 | Lulus: 1 | Gagal: 0 | Error: 0 | Dilewati: 0" in serialized
    assert "Semua pengujian" in serialized
    assert report_url in serialized
    assert metadata.run_url in serialized
    assert "JIRA_API_TOKEN" not in serialized


def test_jira_comment_omits_missing_run_link():
    comment = build_jira_comment(
        Summary(suite="all"),
        ExecutionMetadata(issue_key="RBA-20"),
        "https://reports.example.com/report.html",
    )

    links = [
        mark["attrs"]["href"]
        for paragraph in comment["content"]
        for node in paragraph.get("content", [])
        for mark in node.get("marks", [])
        if mark["type"] == "link"
    ]

    assert links == ["https://reports.example.com/report.html"]


def test_notify_jira_skips_when_configuration_is_empty(monkeypatch, capsys):
    monkeypatch.setattr(publish_module, "JIRA_BASE_URL", None)
    monkeypatch.setattr(publish_module, "JIRA_EMAIL", None)
    monkeypatch.setattr(publish_module, "JIRA_API_TOKEN", None)

    notified = publish_module.notify_jira(
        Summary(suite="all"),
        ExecutionMetadata(issue_key="RBA-20"),
        "https://reports.example.com/report.html",
    )

    assert notified is False
    assert "konfigurasi belum tersedia" in capsys.readouterr().out


def test_notify_jira_rejects_partial_configuration(monkeypatch):
    monkeypatch.setattr(publish_module, "JIRA_BASE_URL", "https://example.atlassian.net")
    monkeypatch.setattr(publish_module, "JIRA_EMAIL", "qa@example.com")
    monkeypatch.setattr(publish_module, "JIRA_API_TOKEN", None)

    with pytest.raises(RuntimeError, match="JIRA_API_TOKEN"):
        publish_module.notify_jira(
            Summary(suite="all"),
            ExecutionMetadata(issue_key="RBA-20"),
            "https://reports.example.com/report.html",
        )


def test_notify_jira_delegates_comment_to_client(monkeypatch):
    monkeypatch.setattr(publish_module, "JIRA_BASE_URL", "https://example.atlassian.net")
    monkeypatch.setattr(publish_module, "JIRA_EMAIL", "qa@example.com")
    monkeypatch.setattr(publish_module, "JIRA_API_TOKEN", "top-secret")
    client = Mock()
    client_class = Mock(return_value=client)
    monkeypatch.setattr(publish_module, "JiraClient", client_class)
    summary = Summary(suite="all")
    metadata = ExecutionMetadata(issue_key="RBA-20")
    report_url = "https://reports.example.com/report.html"

    notified = publish_module.notify_jira(summary, metadata, report_url)

    assert notified is True
    client.add_comment.assert_called_once_with(
        "RBA-20",
        build_jira_comment(summary, metadata, report_url),
    )
    assert "top-secret" not in str(client.add_comment.call_args)
