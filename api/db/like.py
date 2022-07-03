from . import db
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
from api.custom_errors import CustomErrors
from api.db.user import User
from api.db.gallery import Gallery
import datetime

class Like(db.Document):
    user_id = db.ReferenceField(User)
    gallery_id = db.ReferenceField(Gallery)
    created_at = db.DateTimeField(required=True,default=datetime.datetime.now)

    def insert(self):
        try:
            return self.save()
        except ValidationError:
            raise CustomErrors.InternalServer("Needs required fields")

    def remove(self):
        try:
            obj = Like.objects(user_id=self.user_id,gallery_id=self.gallery_id)
            obj.delete()
        except ValidationError:
            raise CustomErrors.InternalServer("Needs required fields")

    def has_like_by_user_and_galery(user_id, gallery_id):
        try:
            Like.objects.get(user_id=user_id,gallery_id=gallery_id)
            return True
        except DoesNotExist as e:
            return False

    @staticmethod
    def get_like_by_gallery(gallery_id):
        try:
            return Like.objects.filter(gallery_id=gallery_id)
        except DoesNotExist as e:
            raise CustomErrors.NotFound("Don't exists like to this gallery")

