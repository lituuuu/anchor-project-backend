from . import db
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
from api.custom_errors import CustomErrors

class User(db.Document):
    username = db.StringField(required=True, unique=True)
    email = db.StringField(required=True, unique=True)
    password = db.BinaryField(required=True)
    admin = db.BooleanField(required=True, default=False)

    def insert(self):
        try:
            return self.save()
        except NotUniqueError:
            raise CustomErrors.InternalServer("The username and email already exists")
        except ValidationError:
            raise CustomErrors.InternalServer("Needs required fields")

    @staticmethod
    def get_by_username(username):
        try:
            return User.objects.get(username=username)
        except DoesNotExist as e:
            raise CustomErrors.NotFound("Wrong username or password")

    @staticmethod
    def get_admin():
        try:
            return User.objects.get(admin=True)
        except DoesNotExist as e:
            raise CustomErrors.NotFound("Not exists admin")