from dataclasses import dataclass, field


@dataclass(frozen=True)
class TestCaseResult:
    node_id: str
    name: str
    suite: str
    status: str
    duration: float = 0.0
    message: str = ""
    details: str = ""


@dataclass
class TestSummary:
    suite: str
    tests: list[TestCaseResult] = field(default_factory=list)
    infrastructure_error: str = ""

    @property
    def total(self):
        return len(self.tests)

    @property
    def passed(self):
        return sum(test.status == "passed" for test in self.tests)

    @property
    def failed(self):
        return sum(test.status == "failed" for test in self.tests)

    @property
    def errors(self):
        return sum(test.status == "error" for test in self.tests)

    @property
    def skipped(self):
        return sum(test.status == "skipped" for test in self.tests)

    @property
    def duration(self):
        return sum(test.duration for test in self.tests)

    @property
    def status(self):
        if self.infrastructure_error:
            return "error"
        if self.failed or self.errors:
            return "failed"
        return "passed"

    @property
    def status_label(self):
        return {
            "passed": "LULUS",
            "failed": "GAGAL",
            "error": "ERROR",
        }[self.status]

    @property
    def conclusion(self):
        if self.status == "passed":
            return "Semua pengujian yang dijalankan berhasil. Tidak ada kegagalan yang perlu ditindaklanjuti."
        if self.status == "failed":
            problem_count = self.failed + self.errors
            return (
                f"Ada {problem_count} pengujian gagal atau error. Tim perlu meninjau detail "
                "sebelum perubahan dilanjutkan."
            )
        return (
            "Eksekusi mengalami error teknis. Hasil belum dapat dipakai sebagai keputusan kualitas "
            "sampai penyebabnya diperbaiki."
        )


@dataclass(frozen=True)
class ExecutionMetadata:
    repository: str = "local"
    branch: str = "local"
    commit_sha: str = "local"
    run_url: str = ""
    run_id: str = "local"
    run_attempt: str = "1"
    issue_key: str = ""
    generated_at: str = ""
