import jwt
from api.config import Config
from api.db.user import User

def register(payload):
    try:
        user = User(**payload).insert()
        user.password = "-"
        return user
    except Exception as e:
        raise e

def login(payload):
    try:
        user = User(**payload)
        user_login = User.get_by_username_and_password(user.username, user.password)
        if user_login:
            return jwt.encode(
                payload=payload,
                key=Config.JWT_TOKEN
            )
    except Exception as e:
        raise e