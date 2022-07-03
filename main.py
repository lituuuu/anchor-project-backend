# Imports
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from api import user, response_status, gallery, aws, validation, comment, like
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
                'message': 'Invalid Token'
            }), response_status.STATUS_UNAUTHORIZED
        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/ping')
def ping():
    return 'pong!'

@app.route('/register',methods = ['POST'])
def register():
    try:
        content = request.json
        validation.valid_field(content, "username")
        validation.valid_field(content, "password")
        registered_user = user.register(content)
        return jsonify(registered_user), response_status.STATUS_CREATED
    except Exception as e:
        return jsonify({"message": e.message}), e.status

@app.route('/login',methods = ['POST'])
def login():
    try:
        content = request.json
        validation.valid_field(content, "username")
        validation.valid_field(content, "password")
        user_logged = user.login(content)
        return jsonify({"token": user_logged.token.decode('UTF-8')}), response_status.STATUS_OK
    except Exception as e:
        return jsonify({"message": e.message}), e.status

@app.route('/gallery',methods = ['GET'])
@token_required
def gallery_all_photo(self):
    limit = Config.QUERY_LIMIT_DEFAULT
    page = Config.QUERY_PAGE_DEFAULT
    try:
        if request.args.get("limit"):
            limit = int(request.args["limit"])
        if request.args.get("page"):
            page = int(request.args["page"])
    except Exception as e:
        return CustomErrors.InternalServer("Conversion error")

    try:
        current_user = user.get_logged_user(request)
        if current_user.admin:
            photos = gallery.get_all_photos(limit, page)
        else:
            photos = gallery.get_photos_by_user(current_user, limit, page)
            print(photos)
        return jsonify(photos), response_status.STATUS_OK
    except Exception as e:
        return jsonify({"message": e.message}), e.status

@app.route('/gallery/pendent',methods = ['GET'])
@token_required
def gallery_pendent(self):
    limit = Config.QUERY_LIMIT_DEFAULT
    page = Config.QUERY_PAGE_DEFAULT
    try:
        if request.args.get("limit"):
            limit = int(request.args["limit"])
        if request.args.get("page"):
            page = int(request.args["page"])
    except Exception as e:
        return CustomErrors.InternalServer("Conversion error")

    try:
        current_user = user.get_logged_user(request)
        validation.is_user_admin(current_user.admin)
        photos = gallery.photos_pendent(limit, page)
        return jsonify(photos), response_status.STATUS_OK
    except Exception as e:
        return jsonify({"message": e.message}), e.status

@app.route('/gallery/confirmed',methods = ['GET'])
def photos_confirmed():
    limit = Config.QUERY_LIMIT_DEFAULT
    page = Config.QUERY_PAGE_DEFAULT
    try:
        if request.args.get("limit"):
            limit = int(request.args["limit"])
        if request.args.get("page"):
            page = int(request.args["page"])
    except Exception as e:
        return CustomErrors.InternalServer("Conversion error")

    try:
        photos = gallery.photos_confirmed(limit, page)
        return jsonify(photos), response_status.STATUS_OK
    except Exception as e:
        return jsonify({"message": e.message}), e.status

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

@app.route('/gallery/confirm',methods = ['POST'])
@token_required
def gallery_photo_confirm(self):
    try:
        current_user = user.get_logged_user(request)
        validation.is_user_admin(current_user.admin)
        photos = gallery.confirm(request.json)
        return jsonify(photos), response_status.STATUS_OK
    except Exception as e:
        return jsonify({"message": e.message}), e.status

@app.route('/comment/<id>', methods=['GET'])
def get_comment(id):
    limit = Config.QUERY_LIMIT_DEFAULT
    page = Config.QUERY_PAGE_DEFAULT
    try:
        if request.args.get("limit"):
            limit = int(request.args["limit"])
        if request.args.get("page"):
                page = int(request.args["page"])
    except Exception as e:
        return CustomErrors.InternalServer("Conversion error")

    try:
        validation.valid_objectid(id)
        gallery_id = gallery.get_by_id(id)
        comments = comment.get_comment_by_gallery(gallery_id, limit, page)
        return jsonify(comments), response_status.STATUS_OK
    except Exception as e:
        return jsonify({"message": e.message}), e.status

@app.route('/comment', methods=['POST'])
@token_required
def post_comment(self):
    try:
        content = request.json
        validation.valid_field(content, "gallery_id")
        gallery.get_by_id(content["gallery_id"])
        content["user_id"] = user.get_logged_user(request)
        comments = comment.insert(content)
        return jsonify(comments), response_status.STATUS_OK
    except Exception as e:
        return jsonify({"message": e.message}), e.status

@app.route('/like/<id>', methods=['GET'])
def get_like(id):
    user_id = None
    try:
        user_id = user.get_logged_user(request)
    except Exception:
        user_id = None

    try:
        validation.valid_objectid(id)
        gallery_id = gallery.get_by_id(id)
        likes = like.get_like(user_id, gallery_id)
        return jsonify(likes), response_status.STATUS_OK
    except Exception as e:
        return jsonify({"message": e.message}), e.status

@app.route('/like', methods=['POST'])
@token_required
def post_like(self):
    try:
        content = request.json
        validation.valid_field(content, "gallery_id")
        content["user_id"] = user.get_logged_user(request)
        likes = like.like_photo(content["user_id"], content["gallery_id"])
        return jsonify(likes), response_status.STATUS_OK
    except Exception as e:
        return jsonify({"message": e.message}), e.status


@app.route('/gallery/<id>', methods=['GET'])
def get_gallery_by_id(id):
    user_id = None
    try:
        user_id = user.get_logged_user(request)
    except Exception:
        user_id = None

    limit = Config.QUERY_LIMIT_DEFAULT
    page = Config.QUERY_PAGE_DEFAULT
    try:
        if request.args.get("limit"):
            limit = int(request.args["limit"])
        if request.args.get("page"):
            page = int(request.args["page"])
    except Exception as e:
        return CustomErrors.InternalServer("Conversion error")

    try:
        validation.valid_objectid(id)
        gallery_id = gallery.get_by_id(id)
        if (not user_id or not user_id.admin) and gallery_id.pendent:
            raise CustomErrors.Unauthorized()
        likes = like.get_like(user_id, gallery_id)
        comments = comment.get_comment_by_gallery(gallery_id, limit, page)
        return jsonify({
            "gallery" : gallery_id,
            "likes": likes,
            "comments": comments
        }), response_status.STATUS_OK
    except Exception as e:
        return jsonify({"message": e.message}), e.status

#@app.route('/validatejwt',methods = ['GET'])
@token_required
def validatejwt(self):
    return jsonify({"status":  "this token is valid!"}), response_status.STATUS_OK

if __name__ == '__main__':
    user.create_if_not_exists_admin()
    app.run()