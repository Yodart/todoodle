from flask import Flask, request
from db import Database
import json
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
db = Database("todoodledb")


@app.route('/todos', methods=['GET'])
def get_todos():
    return db.get_todos(limit=request.args.get('limit'), offset=request.args.get('offset'))


@app.route('/todo/<int:todo_id>', methods=['GET'])
def get_single_todo(todo_id):
    return db.get_single_todo([todo_id])


@app.route('/todo/<int:todo_id>', methods=['PUT'])
def edit_single_todo(todo_id):
    title = request.json['title']if 'title' in request.json else None
    completed = request.json['completed']if 'completed' in request.json else None
    return db.edit_todo(todo_id, title, completed)


@app.route('/todo/<int:todo_id>', methods=["DELETE"])
def delete_single_todo(todo_id):
    return db.delete_todo([todo_id])


@app.route('/users', methods=['GET'])
def get_users():
    return db.get_users(limit=request.args.get('limit'), offset=request.args.get('offset'))


@app.route('/user', methods=['POST'])
def create_user():
    hashed_password = generate_password_hash(
        request.json['password'], method='sha256')
    return db.create_user(name=request.json['name'], password=hashed_password)


@app.route('/user/<int:user_id>', methods=['GET'])
def get_single_user():
    return {}


@app.route('/user/<int:user_id>', methods=['PUT'])
def edit_single_user():
    return {}


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delte_single_user():
    return {}
