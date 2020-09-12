import json
import uuid
import datetime
import jwt
import sys
from flask import Flask, request, jsonify, make_response
from db import Database
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
db = Database("todoodledb")


def token_required(f):
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


@app.route('/todos', methods=['GET'])
@token_required
def get_todos(current_user):
    print(current_user)
    return db.get_todos(limit=request.args.get('limit'), offset=request.args.get('offset'))


@ app.route('/todo/<int:todo_id>', methods=['GET'])
def get_single_todo(todo_id):
    return db.get_single_todo([todo_id])


@ app.route('/todo/<int:todo_id>', methods=['PUT'])
def edit_single_todo(todo_id):
    title = request.json['title']if 'title' in request.json else None
    completed = request.json['completed']if 'completed' in request.json else None
    return db.edit_todo(todo_id, title, completed)


@ app.route('/todo/<int:todo_id>', methods=["DELETE"])
def delete_single_todo(todo_id):
    return db.delete_todo([todo_id])


@ app.route('/users', methods=['GET'])
def get_users():
    return db.get_users(limit=request.args.get('limit'), offset=request.args.get('offset'))


@ app.route('/user', methods=['POST'])
def create_user():
    hashed_password = generate_password_hash(
        request.json['password'], method='sha256')
    return db.create_user(name=request.json['name'], password=hashed_password)


@ app.route('/user/<int:user_id>', methods=['GET'])
def get_single_user_by_id(user_id):
    return db.get_single_user_by_id([user_id])


@ app.route('/user/<int:user_id>', methods=['PUT'])
def edit_single_user(user_id):
    name = request.json['name']if 'name' in request.json else None
    password = generate_password_hash(
        request.json['password'], method='sha256') if 'password' in request.json else None
    return db.edit_user(user_id, name, password)


@ app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_single_user(user_id):
    return db.delete_user([user_id])


@ app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login requited!"'})
    user = db.get_single_user_by_name(name=[auth.username])
    if check_password_hash(user['password'], auth.password):
        print(datetime.datetime.utcnow() + datetime.timedelta(minutes=30))
        token = jwt.encode(
            {'id': user['id'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'secret')
        return jsonify({'token': token.decode('UTF-8')})
    return {'message': "Eh, wrong password"}


if __name__ == '__main__':
    app.run(debug=True)
