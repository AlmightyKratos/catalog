import logging

import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client("s3")

BUCKET_NAME = "foodme1-staging"


def list_buckets() -> set[str]:
    response = s3_client.list_buckets()
    return {
        bucket_name
        for bucket in response["Buckets"]
        if (bucket_name := bucket.get("Name")) is not None
    }


def upload_file(local_file_name: str, object_name: str) -> bool:
    try:
        s3_client.upload_file(local_file_name, BUCKET_NAME, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_file(object_name: str) -> None:
    with open("FILE_NAME", "wb") as f:
        s3_client.download_fileobj(BUCKET_NAME, object_name, f)


if __name__ == "__main__":
    download_file("first.txt")
