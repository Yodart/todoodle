from flask import Flask, request
from db import Database
import json

app = Flask(__name__)
db = Database("todoodledb")


@app.route('/todos', methods=['GET'])
def get_todos():
    if request.method == 'GET':
        return db.get_todos(limit=15, offset=5)


@app.route('/todo/<int:todo_id>', methods=['GET', 'PUT'])
def get_single_todo(todo_id):
    if request.method == 'GET':
        return db.get_single_todo([todo_id])
    if request.method == 'PUT':
        title = request.json['title']if 'title' in request.json else None
        completed = request.json['completed']if 'completed' in request.json else None
        return db.edit_todo(todo_id, title, completed)
