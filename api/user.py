import jwt
from api.config import Config
from api.db.user import User
import main
from api.custom_errors import CustomErrors

def register(payload):
    try:
        user = User(**payload)
        user.password = main.bcrypt.generate_password_hash(user.password)
        user.insert()
        user.password = None
        return user
    except Exception as e:
        raise e

def login(payload):
    try:
        user = User(**payload)
        user_login = User.get_by_username(user.username)
        if user_login and main.bcrypt.check_password_hash(user_login.password, payload["password"]):
            user_login.token = jwt.encode(
                payload=payload,
                key=Config.JWT_TOKEN
            )
            return user_login
        raise CustomErrors.NotFound("Wrong username or password")
    except Exception as e:
        raise e

def get_logged_user(request):
    token = request.headers['x-access-token']
    data = jwt.decode(token, Config.JWT_TOKEN, algorithms=["HS256"])
    current_user = login(data)
    return current_user

#Method to first time running application
def create_if_not_exists_admin():
    try:
        User.get_admin()
        return True
    except Exception as e:
        User(username="admin", password=main.bcrypt.generate_password_hash("admin"), admin=True, email="admin@admin.com").insert()