import boto3
from bson.objectid import ObjectId
from furl import furl

from api.config import Config

s3_session = boto3.Session()

def s3_bucket():
    s3 = s3_session.resource(
        "s3",
        aws_access_key_id=Config.AWS_ACCESS_KEY,
        aws_secret_access_key=Config.AWS_SECRET_KEY,
    )
    return s3.Bucket(Config.AWS_BUCKET_NAME)

def s3_key(file_name):
    return f"{ObjectId()}-{file_name}"

def s3_url(file):
    bucket = s3_bucket()
    key = s3_key(file.filename)
    bucket.Object(key).put(Body=file.read(),ACL='public-read')
    return furl(f"{Config.AWS_S3_HOST}/{Config.AWS_BUCKET_NAME}/{key}").url