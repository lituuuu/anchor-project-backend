from api.db.like import Like

def like_photo(payload):
    try:
        has_like = Like.has_like_by_user_and_galery(payload["user_id"], payload["gallery_id"])
        if has_like:
            Like.remove(payload["user_id"], payload["gallery_id"])
        else:
            Like(**payload).insert()
        return True
    except Exception as e:
        raise e

def get_like(user_id, gallery_id):
    try:
        count = Like.get_like_by_gallery(gallery_id).count()
        has_like = Like.has_like_by_user_and_galery(user_id, gallery_id)
        return { "hasLike" : has_like, "count" : count }
    except Exception as e:
        raise e