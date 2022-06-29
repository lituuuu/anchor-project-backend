import os

jwt_token = os.environ.get("JWT_TOKEN", "hey_how_lets_go")

mongodb_url = os.environ.get("MONGODB_URL", "mongodb+srv://carlosanchormongo:sKGs2CWKjJOB6ZZo@cluster0.e11wi.mongodb.net/?retryWrites=true&w=majority")