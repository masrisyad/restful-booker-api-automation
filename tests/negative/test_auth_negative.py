import pytest

from src.clients.auth_client import AuthClient


@pytest.mark.negative
def test_token_requires_configured_credentials():
    auth_client = AuthClient("https://example.com")

    with pytest.raises(
        RuntimeError,
        match="API_USERNAME and API_PASSWORD must be configured",
    ):
        auth_client.get_token()


@pytest.mark.negative
def test_authentication_with_invalid_username(auth_client):
    response = auth_client.authenticate(
        {
            "username": "invalid-user",
            "password": auth_client.password,
        }
    )

    assert response.status_code == 200
    assert response.json() == {"reason": "Bad credentials"}


@pytest.mark.negative
def test_authentication_with_invalid_password(auth_client):
    response = auth_client.authenticate(
        {
            "username": auth_client.username,
            "password": "invalid-password",
        }
    )

    assert response.status_code == 200
    assert response.json() == {"reason": "Bad credentials"}


@pytest.mark.negative
def test_authentication_with_missing_username(auth_client):
    response = auth_client.authenticate(
        {
            "password": auth_client.password,
        }
    )

    assert response.status_code == 200
    assert response.json() == {"reason": "Bad credentials"}


@pytest.mark.negative
def test_authentication_with_missing_password(auth_client):
    response = auth_client.authenticate(
        {
            "username": auth_client.username,
        }
    )

    assert response.status_code == 200
    assert response.json() == {"reason": "Bad credentials"}
