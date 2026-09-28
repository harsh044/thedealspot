import os
from io import BytesIO

from django.conf import settings
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.utils.deconstruct import deconstructible

from supabase import create_client
import uuid
import os

@deconstructible
class SupabaseStorage(Storage):

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name

        self.supabase_url = settings.SUPABASE_URL
        self.supabase_key = (
            settings.SUPABASE_SERVICE_ROLE_KEY
        )

        self.client = create_client(
            self.supabase_url,
            self.supabase_key,
        )

    def _save(self, name, content):

        if hasattr(content, "seek"):
            content.seek(0)

        extension = os.path.splitext(name)[1]

        unique_name = (
            f"{os.path.splitext(name)[0]}_"
            f"{uuid.uuid4().hex[:12]}"
            f"{extension}"
        )

        name = unique_name

        file_data = content.read()

        content_type = getattr(
            content,
            "content_type",
            None
        ) or "application/octet-stream"

        self.client.storage \
            .from_(self.bucket_name) \
            .upload(
                path=name,
                file=file_data,
                file_options={
                    "content-type": content_type,
                    "cache-control": "3600",
                    "upsert": "false",
                },
            )

        return name

    def delete(self, name):
        """
        Delete file from Supabase Storage.
        """

        if not name:
            return

        self.client.storage \
            .from_(self.bucket_name) \
            .remove([name])

    def exists(self, name):
        """
        Check whether a file exists.

        We return False so Django can generate a
        unique name rather than attempting to overwrite
        an existing Storage object.
        """

        return False

    def url(self, name):
        """
        Return public URL for the file.
        """

        if not name:
            return ""

        return (
            self.client.storage
            .from_(self.bucket_name)
            .get_public_url(name)
        )

    def size(self, name):
        """
        Return file size.

        Supabase Storage doesn't need this for the
        normal Django Admin upload workflow.
        """

        return 0

    def _open(self, name, mode="rb"):
        """
        Download file from Supabase Storage.

        This is useful if Django needs to open the
        uploaded file later.
        """

        response = (
            self.client.storage
            .from_(self.bucket_name)
            .download(name)
        )

        return ContentFile(response, name=name)