from src.reporting.junit_parser import parse_junit_report


def test_parse_junit_report_summarizes_all_statuses(tmp_path):
    junit = tmp_path / "junit.xml"
    junit.write_text(
        """<?xml version="1.0" encoding="utf-8"?>
<testsuite name="api" tests="4">
  <testcase classname="tests.smoke" name="test_health_check" time="0.1" />
  <testcase classname="tests.smoke" name="test_auth" time="0.2">
    <failure message="expected 200">AssertionError: password=secret-value</failure>
  </testcase>
  <testcase classname="tests.smoke" name="test_setup" time="0.3">
    <error message="connection error">Timeout</error>
  </testcase>
  <testcase classname="tests.smoke" name="test_optional" time="0.4">
    <skipped message="not configured" />
  </testcase>
</testsuite>""",
        encoding="utf-8",
    )

    summary = parse_junit_report(junit, suite="smoke")

    assert summary.total == 4
    assert summary.passed == 1
    assert summary.failed == 1
    assert summary.errors == 1
    assert summary.skipped == 1
    assert summary.duration == 1.0
    assert summary.status == "failed"
    assert summary.tests[0].name == "Health check"
    assert "secret-value" not in summary.tests[1].details
    assert "[REDACTED]" in summary.tests[1].details


def test_parse_junit_report_marks_missing_file_as_error(tmp_path):
    summary = parse_junit_report(tmp_path / "missing.xml")

    assert summary.status == "error"
    assert summary.total == 0
    assert "tidak tersedia" in summary.infrastructure_error


def test_parse_junit_report_marks_empty_suite_as_error(tmp_path):
    junit = tmp_path / "junit.xml"
    junit.write_text("<testsuite tests=\"0\"></testsuite>", encoding="utf-8")

    summary = parse_junit_report(junit)

    assert summary.status == "error"
    assert "tidak berisi" in summary.infrastructure_error
