import mimetypes
import os
from pathlib import Path
from urllib.parse import quote, urlsplit
from uuid import uuid4

import boto3
from botocore.config import Config
from django.core.exceptions import ImproperlyConfigured


def _storage_settings():
    environment_names = {
        "SUPABASE_URL": "url",
        "SUPABASE_STORAGE_BUCKET": "bucket",
        "SUPABASE_S3_REGION": "region",
        "SUPABASE_S3_ACCESS_KEY_ID": "access_key_id",
        "SUPABASE_S3_SECRET_ACCESS_KEY": "secret_access_key",
    }
    values = {
        key: os.environ.get(name, "")
        for name, key in environment_names.items()
    }
    values["url"] = values["url"].rstrip("/")
    missing = [name for name, key in environment_names.items() if not values[key]]
    if missing:
        raise ImproperlyConfigured(
            "Supabase Storage is not configured. Set: " + ", ".join(missing)
        )
    if urlsplit(values["url"]).scheme != "https":
        raise ImproperlyConfigured("SUPABASE_URL must use HTTPS.")
    return values


def upload_product_file(uploaded_file, folder="products"):
    config = _storage_settings()
    endpoint_url = f'{config["url"]}/storage/v1/s3'
    client = boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=config["access_key_id"],
        aws_secret_access_key=config["secret_access_key"],
        region_name=config["region"],
        config=Config(signature_version="s3v4"),
    )

    extension = Path(uploaded_file.name).suffix.lower()
    object_key = f"{folder}/{uuid4().hex}{extension}"
    content_type = mimetypes.guess_type(uploaded_file.name)[0]
    client.upload_fileobj(
        uploaded_file,
        config["bucket"],
        object_key,
        ExtraArgs={"ContentType": content_type or "application/octet-stream"},
    )

    bucket = quote(config["bucket"], safe="")
    key = quote(object_key, safe="/")
    return f'{config["url"]}/storage/v1/object/public/{bucket}/{key}'
