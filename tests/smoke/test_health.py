import pytest


@pytest.mark.smoke
def test_api_health_check(base_client):
    response = base_client.get("/ping")

    assert response.status_code == 201
