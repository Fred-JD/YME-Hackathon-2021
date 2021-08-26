import os
import boto3
from botocore.exceptions import ClientError
import logging

access_key = ''
access_secret = ''
bucket_name = 'yme-flask-2021-webapp'


def aws_upload_file(file_name, bucket=bucket_name, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # object_name = os.path.join('/static', file_name)

    # Upload the file
    s3_client = boto3.client('s3',
                                aws_access_key_id = access_key,
                                aws_secret_access_key = access_secret
                            )
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

if __name__ == "__main__":
    aws_upload_file('Screenshot_1.png')
