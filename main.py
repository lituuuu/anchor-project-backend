# Imports
from flask import Flask, redirect, url_for, request, jsonify
from flask_cors import CORS, cross_origin
from api import config, user
import jwt
from functools import wraps

app = Flask(__name__)
CORS(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            data = jwt.decode(token, config.jwt_token, algorithms=["HS256"])
            current_user = None#User.query \
                #.filter_by(public_id=data['public_id']) \
                #.first()
        except Exception as e:
            return jsonify({
                'message': e
            }), 401
        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/ping')
def ping():
    return 'pong!'

@app.route('/register',methods = ['POST'])
def register():
    content = request.json
    if user.register(content):
        return jsonify({"name": "ok"})

    return "Registration failed", 500

@app.route('/login',methods = ['POST'])
def login():
    content = request.json
    response = user.login(content)
    if not response : return "Login:Password not fount", 404
    return response

@app.route('/validatejwt',methods = ['GET'])
@token_required
def validatejwt(self):
    return "", 200

if __name__ == '__main__':
    app.run()


