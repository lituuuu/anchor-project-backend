from . import db
from bson.objectid import ObjectId
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
from api.custom_errors import CustomErrors
from api.db.user import User

class Gallery(db.Document):
    user_id = db.ReferenceField(User)
    photo_bucket = db.StringField(required=True, unique=True)
    pendent = db.BooleanField(required=True,default=True)

    def insert(self):
        try:
            return self.save()
        except NotUniqueError:
            raise CustomErrors.InternalServer("The image already exists in gallery")
        except ValidationError:
            raise CustomErrors.InternalServer("Needs required fields")

    def confirm(self):
        try:
            rows = Gallery.objects(id=ObjectId(self.id)).update(pendent=False)
            if rows==0:
                raise CustomErrors.NotFound("Nothing happens")
        except ValidationError as e:
            raise CustomErrors.InternalServer("Id image error")

    @staticmethod
    def get_all_photos():
        try:
            return Gallery.objects.filter()
        except DoesNotExist as e:
            raise CustomErrors.NotFound("Don't exists pendent photos")

    @staticmethod
    def get_user_photos(user_id):
        try:
            return Gallery.objects.filter(user_id=user_id)
        except DoesNotExist as e:
            raise CustomErrors.NotFound("Don't exists pendent photos")

    @staticmethod
    def get_photos(status):
        try:
            return Gallery.objects.filter(pendent=status)
        except DoesNotExist as e:
            raise CustomErrors.NotFound("Don't exists pendent photos")

    @staticmethod
    def get_photo(id):
        try:
            return Gallery.objects.filter(_id=id)
        except DoesNotExist as e:
            raise CustomErrors.NotFound("Don't this photo in bucket")