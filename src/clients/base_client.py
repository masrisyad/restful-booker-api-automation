import requests

from config.settings import REQUEST_TIMEOUT


class BaseClient:

    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def get(self, endpoint, **kwargs):
        return self.session.get(
            f"{self.base_url}{endpoint}",
            timeout=REQUEST_TIMEOUT,
            **kwargs,
        )

    def post(self, endpoint, **kwargs):
        return self.session.post(
            f"{self.base_url}{endpoint}",
            timeout=REQUEST_TIMEOUT,
            **kwargs,
        )

    def put(self, endpoint, **kwargs):
        return self.session.put(
            f"{self.base_url}{endpoint}",
            timeout=REQUEST_TIMEOUT,
            **kwargs,
        )

    def patch(self, endpoint, **kwargs):
        return self.session.patch(
            f"{self.base_url}{endpoint}",
            timeout=REQUEST_TIMEOUT,
            **kwargs,
        )

    def delete(self, endpoint, **kwargs):
        return self.session.delete(
            f"{self.base_url}{endpoint}",
            timeout=REQUEST_TIMEOUT,
            **kwargs,
        )