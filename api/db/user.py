from . import db
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
from api.custom_errors import CustomErrors

class User(db.Document):
    username = db.StringField(required=True, unique=True)
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)

    def insert(self):
        try:
            return self.save()
        except NotUniqueError:
            raise CustomErrors.InternalServer("The username and email already exists")
        except ValidationError:
            raise CustomErrors.InternalServer("Needs required fields")

    @staticmethod
    def get_by_username_and_password(username, password):
        try:
            return User.objects.get(username = username, password = password)
        except DoesNotExist as e:
            raise CustomErrors.NotFound("Wrong username or password")