from json import JSONDecodeError

from src.clients.base_client import BaseClient


class AuthClient(BaseClient):

    def __init__(self, base_url, username=None, password=None):
        super().__init__(base_url)
        self.username = username
        self.password = password

    def authenticate(self, payload):
        return self.post("/auth", json=payload)

    def authenticate_with_configured_credentials(self):
        if not self.username or not self.password:
            raise RuntimeError(
                "API_USERNAME and API_PASSWORD must be configured"
            )

        return self.authenticate(
            {
                "username": self.username,
                "password": self.password,
            }
        )

    def get_token(self):
        response = self.authenticate_with_configured_credentials()

        if response.status_code != 200:
            raise RuntimeError(
                "Authentication request failed with status "
                f"{response.status_code}"
            )

        try:
            response_body = response.json()
        except (JSONDecodeError, ValueError):
            response_body = {}

        token = response_body.get("token") if isinstance(response_body, dict) else None

        if not isinstance(token, str) or not token:
            raise RuntimeError(
                "Authentication response did not contain a valid token"
            )

        return token
