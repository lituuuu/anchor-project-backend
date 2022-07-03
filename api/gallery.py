from api.db.gallery import Gallery

def get_all_photos(limit, page):
    try:
        photos = Gallery.get_all_photos(limit, page)
        return photos
    except Exception as e:
        raise e

def get_by_id(gallery_id):
    try:
        return Gallery.get_by_id(gallery_id)
    except Exception as e:
        raise e

def get_photos_by_user(user_id, limit, page):
    try:
        photos = Gallery.get_user_photos(user_id, limit, page)
        return photos
    except Exception as e:
        raise e

def photos_pendent(limit, page):
    try:
        photos = Gallery.get_photos(True, limit, page)
        return photos
    except Exception as e:
        raise e

def photos_confirmed(limit, page):
    try:
        photos = Gallery.get_photos(False, limit, page)
        return photos
    except Exception as e:
        raise e

def insert(payload):
    try:
        photos = Gallery(**payload).insert()
        return photos
    except Exception as e:
        raise e

def confirm(payload):
    try:
        photo = Gallery(**payload)
        photo.confirm()
        photo.pendent = False
        return photo
    except Exception as e:
        raise e

