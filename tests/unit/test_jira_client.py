from unittest.mock import Mock

import pytest

from src.integrations.jira_client import JiraClient, JiraConfig


def test_jira_config_allows_empty_but_rejects_partial():
    assert JiraConfig().validate() is False

    partial_configs = (
        (JiraConfig(base_url="https://example.atlassian.net"), "JIRA_EMAIL"),
        (JiraConfig(email="qa@example.com"), "JIRA_BASE_URL"),
        (JiraConfig(api_token="top-secret"), "JIRA_BASE_URL"),
        (
            JiraConfig(base_url="https://example.atlassian.net", email="qa@example.com"),
            "JIRA_API_TOKEN",
        ),
    )
    for config, missing_name in partial_configs:
        with pytest.raises(RuntimeError, match=missing_name):
            config.validate()


def test_jira_config_normalizes_trailing_slash():
    config = JiraConfig(
        base_url="https://example.atlassian.net///",
        email="qa@example.com",
        api_token="top-secret",
    )

    assert config.normalized_base_url == "https://example.atlassian.net"


def test_add_comment_uses_basic_auth_and_adf_body():
    response = Mock()
    session = Mock()
    session.post.return_value = response
    config = JiraConfig(
        base_url="https://example.atlassian.net/",
        email="qa@example.com",
        api_token="top-secret",
        timeout=12,
    )
    document = {
        "type": "doc",
        "version": 1,
        "content": [{"type": "paragraph", "content": [{"type": "text", "text": "LULUS"}]}],
    }

    JiraClient(config, session=session).add_comment("RBA 20", document)

    session.post.assert_called_once_with(
        "https://example.atlassian.net/rest/api/3/issue/RBA%2020/comment",
        auth=("qa@example.com", "top-secret"),
        json={"body": document},
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        timeout=12,
    )
    response.raise_for_status.assert_called_once_with()
    assert "top-secret" not in str(document)
    assert "qa@example.com" not in str(document)
