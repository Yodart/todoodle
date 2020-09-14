from flask import Blueprint
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from db import Database
from auth_service import require_auth_token
import datetime
import jwt
import json


user_service = Blueprint('user', __name__)
db = Database("todoodledb")


@ user_service.route('/user', methods=['POST'])
def create_user():
    request_json = json.loads(request.data)
    hashed_password = generate_password_hash(
        request_json['password'], method='sha256')
    return db.create_user(name=request_json['name'], password=hashed_password)


@ user_service.route('/user/<int:user_id>', methods=['GET'])
def get_single_user_by_id(user_id):
    return db.get_single_user_by_id([user_id])


@ user_service.route('/user/<int:user_id>', methods=['PUT'])
def edit_single_user(user_id):
    request_json = json.loads(request.data)
    name = request_json['name']if 'name' in request_json else None
    password = generate_password_hash(
        request_json['password'], method='sha256') if 'password' in request_json else None
    return db.edit_user(user_id, name, password)


@ user_service.route('/user/<int:user_id>', methods=['DELETE'])
def delete_single_user(user_id):
    return db.delete_user([user_id])
