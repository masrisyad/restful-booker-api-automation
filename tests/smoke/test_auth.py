import pytest


@pytest.mark.smoke
def test_authentication_with_valid_credentials(auth_client):
    response = auth_client.authenticate_with_configured_credentials()

    assert response.status_code == 200

    response_body = response.json()

    assert "token" in response_body
    assert isinstance(response_body["token"], str)
    assert response_body["token"]


@pytest.mark.smoke
def test_authentication_token_is_reusable(auth_token):
    assert isinstance(auth_token, str)
    assert auth_token
