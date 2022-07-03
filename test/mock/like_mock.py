from api.gallery import Gallery
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

def confirmed_gallery():
    return [{
        "_id": {
            "$oid": "62bf31d1fae611754b187c8c"
        },
        "pendent": "false",
        "photo_bucket": "confirmed",
        "user_id": {
            "$oid": "62bee943d330b93cb604317d"
        }
    }]

def confirmed_gallery():
    return [{
        "_id": {
            "$oid": "62bf31d1fae611754b187c8c"
        },
        "pendent": "false",
        "photo_bucket": "confirmed",
        "user_id": {
            "$oid": "62bee943d330b93cb604317d"
        }
    }]

def all_gallery():
    return [{
        "_id": {
            "$oid": "62bf31d1fae611754b187c8c"
        },
        "pendent": "true",
        "photo_bucket": "confirmed",
        "user_id": {
            "$oid": "62bee943d330b93cb604317d"
        }
    },{
        "_id": {
            "$oid": "62bf31d1fae611754b187c89"
        },
        "pendent": "false",
        "photo_bucket": "pendent",
        "user_id": {
            "$oid": "62bee943d330b93cb604317f"
        }
    }]

def gallery_mock_insert(payload):
    return Gallery(**payload)

def gallery_mock_confirm(payload):
    return Gallery(**payload)

def internal_server_error():
    raise CustomErrors.InternalServer("INTERNAL_SERVER_TEST")

def not_found_error():
    raise CustomErrors.NotFound("NOT_FOUND_TEST")
