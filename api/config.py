import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    JWT_TOKEN = os.getenv('JWT_TOKEN')
    MONGODB_HOST = os.getenv('MONGODB_URL')
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
    AWS_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
    AWS_S3_HOST = os.getenv('AWS_S3_HOST')

    QUERY_LIMIT_DEFAULT = 10
    QUERY_PAGE_DEFAULT = 0


