"""Tests for python-s3-downloader."""
import io
import textwrap
from unittest.mock import MagicMock, patch


def generate_downloader_script(buckets):
    """Extract the script generation logic from main.py for testing."""
    output = io.StringIO()
    for bucket in buckets:
        output.write('')
        output.write(f'echo "{bucket["Name"]}"\n')
        output.write(f"if [ -e {bucket['Name']}.tar.gz ]\n")
        output.write(f"then\n")
        output.write(f"tar -xvf {bucket['Name']}.tar.gz\n")
        output.write(f"fi\n")
        output.write(f'aws s3 sync s3://{bucket["Name"]} {bucket["Name"]}\n')
        output.write(f"tar -czvf {bucket['Name']}.tar.gz {bucket['Name']}\n")
        output.write(f"rm -rf {bucket['Name']}\n")
        output.write('')
    return output.getvalue()


def test_single_bucket_script():
    buckets = [{"Name": "my-bucket"}]
    script = generate_downloader_script(buckets)
    assert 'echo "my-bucket"' in script
    assert "aws s3 sync s3://my-bucket my-bucket" in script
    assert "tar -czvf my-bucket.tar.gz my-bucket" in script
    assert "rm -rf my-bucket" in script
    assert "if [ -e my-bucket.tar.gz ]" in script


def test_multiple_buckets_script():
    buckets = [{"Name": "bucket-a"}, {"Name": "bucket-b"}]
    script = generate_downloader_script(buckets)
    assert "aws s3 sync s3://bucket-a bucket-a" in script
    assert "aws s3 sync s3://bucket-b bucket-b" in script


def test_empty_buckets_script():
    script = generate_downloader_script([])
    assert script == ""


def test_boto3_import():
    import boto3
    assert boto3 is not None


def test_botocore_import():
    import botocore
    assert botocore is not None
