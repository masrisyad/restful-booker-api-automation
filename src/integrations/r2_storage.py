from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

import boto3


@dataclass(frozen=True)
class R2Config:
    account_id: str = ""
    access_key_id: str = ""
    secret_access_key: str = ""
    bucket_name: str = ""
    public_base_url: str = ""

    @property
    def values(self):
        return {
            "R2_ACCOUNT_ID": self.account_id,
            "R2_ACCESS_KEY_ID": self.access_key_id,
            "R2_SECRET_ACCESS_KEY": self.secret_access_key,
            "R2_BUCKET_NAME": self.bucket_name,
            "R2_PUBLIC_BASE_URL": self.public_base_url,
        }

    def validate(self):
        configured = [name for name, value in self.values.items() if value]
        if not configured:
            return False
        missing = [name for name, value in self.values.items() if not value]
        if missing:
            raise RuntimeError("Konfigurasi R2 belum lengkap: " + ", ".join(missing))
        return True


class R2Storage:

    def __init__(self, config, client=None):
        if not config.validate():
            raise RuntimeError("Konfigurasi R2 belum tersedia")
        self.config = config
        self.client = client or boto3.client(
            "s3",
            endpoint_url=f"https://{config.account_id}.r2.cloudflarestorage.com",
            aws_access_key_id=config.access_key_id,
            aws_secret_access_key=config.secret_access_key,
            region_name="auto",
        )

    def public_url(self, object_key):
        encoded_key = quote(object_key, safe="/")
        return f"{self.config.public_base_url.rstrip('/')}/{encoded_key}"

    def upload(self, file_path, object_key, content_type):
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"Report tidak ditemukan: {path.name}")
        with path.open("rb") as report_file:
            self.client.upload_fileobj(
                report_file,
                self.config.bucket_name,
                object_key,
                ExtraArgs={"ContentType": content_type},
            )
        return self.public_url(object_key)
