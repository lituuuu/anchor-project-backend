from api.user import User
from api.custom_errors import CustomErrors

def user_mock_insert(payload):
    return User(**payload)

def user_mock_get(payload):
    return User(**payload)

def internal_server_error():
    raise CustomErrors.InternalServer("INTERNAL_SERVER_TEST")

def not_found_error(payload):
    raise CustomErrors.NotFound("NOT_FOUND_TEST")

user_encode_jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im15X3Rlc3QiLCJlbWFpbCI6Im15X3Rlc3QiLCJwYXNzd29yZCI6Im15X3Rlc3QifQ.U6wX3u8uuKaW4XRQk8TdXDRcvYp-Da1lJ-cGVP6ytOI"