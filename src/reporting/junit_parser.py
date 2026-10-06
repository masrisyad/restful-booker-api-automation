from pathlib import Path
import re
import xml.etree.ElementTree as ET

from src.reporting.models import TestCaseResult, TestSummary


_SECRET_PATTERNS = (
    re.compile(r"(?i)(password|token|authorization|cookie)(\s*[=:]\s*)([^\s,;]+)"),
)


def _redact(value):
    text = value or ""
    for pattern in _SECRET_PATTERNS:
        text = pattern.sub(r"\1\2[REDACTED]", text)
    return text


def _display_name(name):
    readable = name.removeprefix("test_").replace("_", " ").strip()
    return readable[:1].upper() + readable[1:] if readable else name


def _test_status(testcase):
    for status in ("failure", "error", "skipped"):
        element = testcase.find(status)
        if element is not None:
            return status, element
    return "passed", None


def parse_junit_report(path, suite="all"):
    report_path = Path(path)
    if not report_path.is_file():
        return TestSummary(
            suite=suite,
            infrastructure_error="JUnit XML tidak tersedia. Eksekusi test mungkin berhenti sebelum report dibuat.",
        )

    try:
        root = ET.parse(report_path).getroot()
    except (ET.ParseError, OSError):
        return TestSummary(
            suite=suite,
            infrastructure_error="JUnit XML tidak dapat dibaca karena file rusak atau tidak lengkap.",
        )

    results = []
    for testcase in root.iter("testcase"):
        raw_name = testcase.get("name", "test tanpa nama")
        class_name = testcase.get("classname", "")
        node_id = f"{class_name}::{raw_name}" if class_name else raw_name
        status, detail_element = _test_status(testcase)
        if status == "failure":
            status = "failed"
        message = ""
        details = ""
        if detail_element is not None:
            message = _redact(detail_element.get("message", ""))
            details = _redact(detail_element.text or "")

        try:
            duration = float(testcase.get("time", "0"))
        except ValueError:
            duration = 0.0

        results.append(
            TestCaseResult(
                node_id=node_id,
                name=_display_name(raw_name),
                suite=class_name or suite,
                status=status,
                duration=duration,
                message=message,
                details=details,
            )
        )

    if not results:
        return TestSummary(
            suite=suite,
            infrastructure_error="JUnit XML tidak berisi hasil test. Eksekusi tidak dianggap lulus.",
        )

    return TestSummary(suite=suite, tests=results)
