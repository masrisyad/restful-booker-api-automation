import pytest

from config.settings import API_PASSWORD, API_USERNAME, BASE_URL
from src.clients.auth_client import AuthClient
from src.clients.base_client import BaseClient


@pytest.fixture
def base_client():
    return BaseClient(BASE_URL)


@pytest.fixture
def auth_client():
    return AuthClient(BASE_URL, API_USERNAME, API_PASSWORD)


@pytest.fixture
def auth_token(auth_client):
    return auth_client.get_token()
