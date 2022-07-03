from api.like import Like
from api.custom_errors import CustomErrors

def list_of_likes():
    return [{
        "_id": {
            "$oid": "62bf31d1fae611754b187c8c"
        },
        "pendent": "true",
        "photo_bucket": "pendent",
        "user_id": {
            "$oid": "62bee943d330b93cb604317d"
        }
    },{
        "_id": {
            "$oid": "62bf31d1fae611754b187c8c"
        },
        "pendent": "true",
        "photo_bucket": "pendent",
        "user_id": {
            "$oid": "62bee943d330b93cb604317d"
        }
    }]

def like_mock_insert(payload):
    return Like(**payload)

def internal_server_error():
    raise CustomErrors.InternalServer("INTERNAL_SERVER_TEST")

def not_found_error():
    raise CustomErrors.NotFound("NOT_FOUND_TEST")
