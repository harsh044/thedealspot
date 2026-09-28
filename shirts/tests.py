import os
from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase

from .storage import upload_product_file


class SupabaseStorageTests(SimpleTestCase):
    @patch.dict(
        os.environ,
        {
            "SUPABASE_URL": "https://project-ref.supabase.co/",
            "SUPABASE_STORAGE_BUCKET": "products",
            "SUPABASE_S3_REGION": "ap-south-1",
            "SUPABASE_S3_ACCESS_KEY_ID": "test-access-key",
            "SUPABASE_S3_SECRET_ACCESS_KEY": "test-secret-key",
        },
        clear=True,
    )
    @patch("shirts.storage.boto3.client")
    def test_upload_returns_public_url_and_streams_file(self, create_client):
        uploaded_file = SimpleUploadedFile("product video.MP4", b"video data")

        url = upload_product_file(uploaded_file, "products/videos")

        self.assertRegex(
            url,
            r"^https://project-ref\.supabase\.co/storage/v1/object/public/"
            r"products/products/videos/[0-9a-f]{32}\.mp4$",
        )
        create_client.return_value.upload_fileobj.assert_called_once()
        call = create_client.return_value.upload_fileobj.call_args
        self.assertIs(call.args[0], uploaded_file)
        self.assertEqual(call.args[1], "products")
        self.assertTrue(url.endswith(f"/{call.args[2]}"))
        self.assertEqual(call.kwargs["ExtraArgs"]["ContentType"], "video/mp4")
        self.assertEqual(create_client.call_args.kwargs["region_name"], "ap-south-1")

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_configuration_is_reported(self):
        with self.assertRaisesMessage(
            ImproperlyConfigured, "SUPABASE_S3_SECRET_ACCESS_KEY"
        ):
            upload_product_file(SimpleUploadedFile("image.png", b"image"))
