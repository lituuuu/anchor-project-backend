from api.db.comment import Comment

def insert(payload):
    try:
        comment = Comment(**payload).insert()
        return comment
    except Exception as e:
        raise e

def get_comment_by_gallery(gallery_id, limit, page):
    try:
        comments = Comment.get_comment_by_gallery(gallery_id, limit, page)
        return comments
    except Exception as e:
        raise e