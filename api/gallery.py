from api.db.gallery import Gallery

def get_all_photos():
    try:
        photos = Gallery.get_all_photos()
        return photos
    except Exception as e:
        raise e

def get_photos_by_user(user_id):
    try:
        photos = Gallery.get_user_photos(user_id)
        return photos
    except Exception as e:
        raise e

def photos_pendent():
    try:
        photos = Gallery.get_photos(True)
        return photos
    except Exception as e:
        raise e

def photos_confirmed():
    try:
        photos = Gallery.get_photos(False)
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
        photo = Gallery(**payload).confirm()
        return photo
    except Exception as e:
        raise e

