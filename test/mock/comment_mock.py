from api.comment import Comment
from api.custom_errors import CustomErrors

def list_of_comments():
    return [
        {
            "_id": {
                "$oid": "62c0f7360a13b350aaeb7978"
            },
            "created_at": {
                "$date": "2022-07-02T22:56:06.754Z"
            },
            "gallery_id": {
                "$oid": "62c0634858ffd07aecc4178c"
            },
            "message": "test_comment_2",
            "user_id": {
                "$oid": "62c05c17a10c56097d006979"
            }
        },
        {
            "_id": {
                "$oid": "62c0f7360a13b350aaeb7978"
            },
            "created_at": {
                "$date": "2022-07-02T22:56:06.754Z"
            },
            "gallery_id": {
                "$oid": "62c0634858ffd07aecc4178c"
            },
            "message": "test_comment_2",
            "user_id": {
                "$oid": "62c05c17a10c56097d006979"
            }
        }
    ]

def comment_mock_insert(payload):
    return Comment(**payload)

def internal_server_error():
    raise CustomErrors.InternalServer("INTERNAL_SERVER_TEST")

def not_found_error():
    raise CustomErrors.NotFound("NOT_FOUND_TEST")
