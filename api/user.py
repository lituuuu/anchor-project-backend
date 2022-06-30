import jwt
from api import config
from api.model import user_model

def register(payload):
    try:
        return user_model.insert(payload["login"], payload["email"], payload["password"])
    except Exception as e:
        # Some Log, in this case i'll use only print to log in my console
        print (e)
        return False

def login(payload):
    try:
        user = user_model.get(payload["login"], payload["password"])
        if (user != None):
            return jwt.encode(
                payload=payload,
                key=config.jwt_token
            )
    except Exception as e:
        # Some Log, in this case i'll use only print to log in my console
        print (e)
    return None