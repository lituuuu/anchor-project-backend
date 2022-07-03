from . import db
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
from api.custom_errors import CustomErrors
import datetime

class User(db.Document):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.BinaryField(required=True)
    admin = db.BooleanField(required=True, default=False)
    created_at = db.DateTimeField(required=True, default=datetime.datetime.now)

    def insert(self):
        try:
            return self.save()
        except NotUniqueError:
            raise CustomErrors.InternalServer("The username and email already exists")
        except ValidationError as e:
            raise CustomErrors.InternalServer(str(e))

    @staticmethod
    def get_by_username(username):
        try:
            return User.objects.get(username=username)
        except DoesNotExist as e:
            raise CustomErrors.NotFound("Wrong username or password")

    @staticmethod
    def get_admin():
        try:
            count = User.objects.filter(admin=True).count()
            if count <= 0:
                raise CustomErrors.NotFound("Not exists admin")
        except Exception as e:
            raise e