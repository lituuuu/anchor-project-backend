import os

class Config(object):
    JWT_TOKEN = os.environ.get("JWT_TOKEN", "hey_how_lets_go")
    MONGODB_HOST = os.environ.get("MONGODB_URL","mongodb+srv://carlosanchormongo:sKGs2CWKjJOB6ZZo@cluster0.e11wi.mongodb.net/?retryWrites=true&w=majority")