from dataclasses import dataclass
from urllib.parse import quote

import requests


@dataclass(frozen=True)
class JiraConfig:
    base_url: str = ""
    email: str = ""
    api_token: str = ""
    timeout: int = 30

    def validate(self):
        values = (self.base_url, self.email, self.api_token)
        if not any(values):
            return False

        missing = []
        if not self.base_url:
            missing.append("JIRA_BASE_URL")
        if not self.email:
            missing.append("JIRA_EMAIL")
        if not self.api_token:
            missing.append("JIRA_API_TOKEN")
        if missing:
            raise RuntimeError("Konfigurasi Jira belum lengkap: " + ", ".join(missing))
        return True

    @property
    def normalized_base_url(self):
        return self.base_url.rstrip("/")


class JiraClient:

    def __init__(self, config, session=None):
        if not config.validate():
            raise RuntimeError("Konfigurasi Jira belum tersedia")
        self.config = config
        self.session = session or requests.Session()

    def add_comment(self, issue_key, document):
        encoded_issue_key = quote(issue_key, safe="")
        response = self.session.post(
            f"{self.config.normalized_base_url}/rest/api/3/issue/{encoded_issue_key}/comment",
            auth=(self.config.email, self.config.api_token),
            json={"body": document},
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            timeout=self.config.timeout,
        )
        response.raise_for_status()
