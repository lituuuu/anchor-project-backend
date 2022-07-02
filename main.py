# Imports
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from api import user, response_status, gallery, aws, validation
from api.db import initialize_db
from api.custom_errors import CustomErrors
import jwt
from functools import wraps
from api.config import Config

app = Flask(__name__)
bcrypt = Bcrypt(app)
CORS(app)
app.config.from_object(Config)
initialize_db(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing !!'}), response_status.STATUS_UNAUTHORIZED

        try:
            data = jwt.decode(token, Config.JWT_TOKEN, algorithms=["HS256"])
            current_user = user.login(data)
        except Exception as e:
            return jsonify({
                'message': str(e)
            }), response_status.STATUS_UNAUTHORIZED
        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/ping')
def ping():
    return 'pong!'

@app.route('/register',methods = ['POST'])
def register():
    try:
        registered_user = user.register(request.json)
        return jsonify(registered_user), response_status.STATUS_CREATED
    except Exception as e:
        return jsonify({"message": e.message}), e.status

@app.route('/login',methods = ['POST'])
def login():
    try:
        user_logged = user.login(request.json)
        return jsonify({"token": user_logged.token.decode('UTF-8')}), response_status.STATUS_OK
    except Exception as e:
        return jsonify({"message": e.message}), e.status

#TODO:  unit test
@app.route('/gallery',methods = ['GET'])
@token_required
def gallery_all_photo(self):
    try:
        current_user = user.get_logged_user(request)
        if current_user.admin:
            photos = gallery.get_all_photos()
        else:
            photos = gallery.get_photos_by_user(current_user)
        return jsonify(photos), response_status.STATUS_OK
    except Exception as e:
        return jsonify({"message": e.message}), e.status

@app.route('/gallery/pendent',methods = ['GET'])
@token_required
def gallery_pendent(self):
    try:
        current_user = user.get_logged_user(request)
        validation.is_user_admin(current_user.admin)
        photos = gallery.photos_pendent()
        return jsonify(photos), response_status.STATUS_OK
    except Exception as e:
        return jsonify({"message": e.message}), e.status

@app.route('/gallery/confirmed',methods = ['GET'])
def photos_confirmed():
    try:
        photos = gallery.photos_confirmed()
        return jsonify(photos), response_status.STATUS_OK
    except Exception as e:
        return jsonify({"message": e.message}), e.status

#TODO: unit test
@app.route('/gallery',methods = ['POST'])
@token_required
def gallery_insert(self):
    try:
        content = {
            "user_id": None,
            "photo_bucket": None,
            "pendent": True
        }
        if (validation.header_has_valid_file(request)):
            photo = request.files["file"]

        current_user = user.get_logged_user(request)
        content["user_id"] = current_user
        photo_bucket = aws.s3_url(photo)
        content["photo_bucket"] = photo_bucket

        if current_user.admin:
            content["pendent"] = False
        photos = gallery.insert(content)
        return jsonify(photos), response_status.STATUS_OK
    except Exception as e:
        return jsonify({"message": e.message}), e.status

#TODO: unit test
@app.route('/gallery/confirm',methods = ['POST'])
@token_required
def gallery_photo_confirm(self):
    try:
        content = request.json
        current_user = user.get_logged_user(request)
        validation.is_user_admin(current_user.admin)
        photos = gallery.confirm(content)
        return jsonify(photos), response_status.STATUS_OK
    except Exception as e:
        return jsonify({"message": e.message}), e.status

@app.route('/validatejwt',methods = ['GET'])
@token_required
def validatejwt(self):
    return jsonify({"status":  "this token is valid!"}), response_status.STATUS_OK

if __name__ == '__main__':
    user.create_if_not_exists_admin()
    app.run()