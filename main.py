# Imports
from flask import Flask, request, jsonify
from flask_cors import CORS
from api import user, response_status
from api.db import initialize_db
import jwt
from functools import wraps
from api.config import Config


app = Flask(__name__)
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
    content = request.json
    try:
        registered_user = user.register(content)
        return jsonify(registered_user), response_status.STATUS_CREATED
    except Exception as e:
        return jsonify({"message": e.message}), e.status

@app.route('/login',methods = ['POST'])
def login():
    content = request.json
    try:
        user_token = user.login(content)
        return jsonify({"token": user_token.decode('UTF-8')}), response_status.STATUS_OK
    except Exception as e:
        return jsonify({"message": e.message}), e.status


@app.route('/validatejwt',methods = ['GET'])
@token_required
def validatejwt(self):
    return jsonify({"status":  "this token is valid!"}), response_status.STATUS_OK

if __name__ == '__main__':
    app.run()


