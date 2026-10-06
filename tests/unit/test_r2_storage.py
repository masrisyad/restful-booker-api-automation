from unittest.mock import Mock

import pytest

from src.integrations.r2_storage import R2Config, R2Storage


def valid_config():
    return R2Config(
        account_id="account",
        access_key_id="access",
        secret_access_key="secret",
        bucket_name="reports",
        public_base_url="https://reports.example.com/base/",
    )


def test_r2_config_allows_empty_but_rejects_partial():
    assert R2Config().validate() is False

    with pytest.raises(RuntimeError, match="R2_BUCKET_NAME"):
        R2Config(account_id="account").validate()


def test_upload_uses_content_type_and_returns_encoded_public_url(tmp_path):
    report = tmp_path / "report.html"
    report.write_text("<h1>ok</h1>", encoding="utf-8")
    client = Mock()
    storage = R2Storage(valid_config(), client=client)

    url = storage.upload(
        report,
        "repo/RBA-20/run 1/stakeholder-report.html",
        "text/html; charset=utf-8",
    )

    assert url == "https://reports.example.com/base/repo/RBA-20/run%201/stakeholder-report.html"
    args, kwargs = client.upload_fileobj.call_args
    assert args[1:3] == ("reports", "repo/RBA-20/run 1/stakeholder-report.html")
    assert kwargs["ExtraArgs"] == {"ContentType": "text/html; charset=utf-8"}
