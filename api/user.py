import jwt
from api import config
from api.model import user_model

def register(payload):
    user_model.insert(payload["login"], payload["email"], payload["password"])
    return True

def login(payload):
    temp = user_model.get(payload["login"], payload["password"])
    if (temp == None) : return None
    token = jwt.encode(
        payload=payload,
        key=config.jwt_token
    )
    return token