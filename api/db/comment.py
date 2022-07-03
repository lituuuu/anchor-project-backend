from . import db
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
from api.custom_errors import CustomErrors
from api.db.user import User
from api.db.gallery import Gallery
import datetime

class Comment(db.Document):
    user_id = db.ReferenceField(User,required=True)
    gallery_id = db.ReferenceField(Gallery,required=True)
    message = db.StringField(required=True)
    created_at = db.DateTimeField(required=True,default=datetime.datetime.now)

    def insert(self):
        try:
            return self.save()
        except ValidationError:
            raise CustomErrors.InternalServer("Needs required fields")

    @staticmethod
    def get_comment_by_gallery(gallery_id, limit, page):
        try:
            return Comment.objects.filter(gallery_id=gallery_id).limit(limit).skip(page*limit).order_by('-created_at')
        except DoesNotExist as e:
            raise CustomErrors.NotFound("Don't exists comments")