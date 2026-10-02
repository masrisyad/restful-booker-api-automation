import pytest

from config.settings import BASE_URL
from src.clients.base_client import BaseClient


@pytest.fixture
def base_client():
    return BaseClient(BASE_URL)