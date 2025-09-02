import pytest
from backend.app.services.storage import upload_file, ensure_bucket

def test_upload_file(tmp_path):
    bucket = "test-bucket"
    ensure_bucket(bucket)
    f = tmp_path / "test.txt"
    f.write_text("hello")
    uri = upload_file(str(f), bucket, "test.txt")
    assert uri.startswith("s3://")
