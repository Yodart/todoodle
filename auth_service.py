from flask import Blueprint
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from db import Database
import datetime
import jwt
import json

auth_service = Blueprint('auth', __name__)
db = Database("todoodledb")


def require_auth_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'error': 'Missing auth token'}), 401
        try:
            data = jwt.decode(token, 'secret')
            current_user = db.get_single_user_by_id(user_id=[data['id']])
        except:
            return jsonify({'error': 'Invalid auth token.'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


@auth_service.route('/login', methods=['POST'])
def login():
    try:
        auth = json.loads(request.data)
        user = db.get_single_user_by_name(name=auth['name'])
        if check_password_hash(user['password'], auth['password']):
            token = jwt.encode(
                {'id': user['id'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'secret')
            return jsonify({'token': token.decode('UTF-8')}), 200
        return {'message': "Eh, wrong password"}, 401
    except:
        return {'error': 'Couldnt find user'}, 401
