import os

class Config(object):
    JWT_TOKEN = os.environ.get("JWT_TOKEN", "hey_how_lets_go")
    MONGODB_HOST = os.environ.get("MONGODB_URL","mongodb+srv://carlosanchormongo:sKGs2CWKjJOB6ZZo@cluster0.e11wi.mongodb.net/?retryWrites=true&w=majority")
    AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY", "AKIA6AWHAFNGR7JOVPHO")
    AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY", "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")
    AWS_BUCKET_NAME = os.environ.get("AWS_S3_BUCKET_NAME", "anchorproject")
    AWS_S3_HOST = os.environ.get("AWS_S3_HOST", "https://s3.amazonaws.com")


