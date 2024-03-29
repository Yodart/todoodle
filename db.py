import psycopg2
import random
import sys
import json
from datetime import datetime
from models import todo
from flask import jsonify
from random_word import RandomWords
from models.todo import Todo

rw = RandomWords()


class Database:
    def __init__(self, db):
        self.db = db
        self.conn = psycopg2.connect(database=self.db)
        self.cur = self.conn.cursor()

    def get_todos(self, limit=5, offset=0):
        try:
            self.cur.execute(
                "SELECT id, title, completed,created_at FROM todos ORDER BY created_at LIMIT %s OFFSET %s", (limit, offset))
            return jsonify([{'id': x[0], 'title':x[1], 'completed':x[2], 'created_at':x[3]} for x in self.cur.fetchall()])
        except:
            return {'error': "Unable to fetch /todos", "traceback": str(sys.exc_info())}, 404

    def get_single_todo(self, todo_id):
        try:
            self.cur.execute(
                "SELECT id, title, completed,created_at FROM todos WHERE id=%s ", (todo_id))
            response = self.cur.fetchall()[0]
            return {'id': response[0], 'title': response[1], 'completed': response[2], 'created_at': response[3]}
        except:
            return {'error': "Unable to fetch /todo/<id>", "traceback": str(sys.exc_info())}

    def create_todo(self, title):
        try:
            self.cur.execute(
                "INSERT INTO todos (title,completed) values(%s,%s)", (title, 'false'))
            self.conn.commit()
            return {'response': 'New todo created'}, 200
        except:
            return {'error': "Unable to create todo", "traceback": str(sys.exc_info())}

    def delete_todo(self, id):
        try:
            self.cur.execute(
                "DELETE FROM todos WHERE id = %s", (id))
            self.conn.commit()
            return {'response': 'todo deleted'}, 200
        except:
            return {'error': "Unable to delete todo", "traceback": str(sys.exc_info())}

    def edit_todo(self, id, title, completed):
        try:
            if title is None and completed is None:
                return {'response': 'todo was edited, put the provided data was the same as the current one.'}, 200
            else:
                if title is not None and completed is None:
                    self.cur.execute(
                        "UPDATE todos SET title = %s WHERE id = %s", (title, id))
                elif title is None and completed is not None:
                    self.cur.execute(
                        "UPDATE todos SET completed = %s WHERE id = %s", (completed, id))
                else:
                    self.cur.execute(
                        "UPDATE todos SET title = %s , completed = %s WHERE id = %s", (title, completed, id))
                    self.conn.commit()
                    return {'response': 'todo was edited'}, 200
        except:
            return {'error': "Unable to edit todo", "traceback": str(sys.exc_info())}

    def get_users(self, limit=5, offset=0):
        try:
            self.cur.execute(
                "SELECT id,name,password,created_at FROM users ORDER BY created_at LIMIT %s OFFSET %s", (limit, offset))
            return jsonify([{'id': x[0], 'name':x[1], 'password':x[2], 'created_at':x[3]} for x in self.cur.fetchall()])
        except:
            return {'error': "Unable to fetch all users", "traceback": str(sys.exc_info())}

    def get_single_user_by_id(self, user_id):
        try:
            self.cur.execute(
                "SELECT id,name,password,created_at FROM users WHERE id=%s ", (user_id))
            response = self.cur.fetchall()[0]
            return {'id': response[0], 'name': response[1], 'password': response[2], 'created_at': response[3]}
        except:
            return {'error': "Unable to fetch /user/<id>", "traceback": str(sys.exc_info())}

    def get_single_user_by_name(self, name):
        try:
            self.cur.execute(
                "SELECT id,name,password,created_at FROM users WHERE name=%s ", ([name]))
            response = self.cur.fetchall()[0]
            return {'id': response[0], 'name': response[1], 'password': response[2], 'created_at': response[3]}
        except:
            return {'error': "Unable to fetch /user/<id>", "traceback": str(sys.exc_info())}

    def create_user(self, name, password):
        try:
            self.cur.execute(
                "INSERT INTO users (name,password) values(%s,%s)", (name, password))
            self.conn.commit()
            return {'response': 'new user created'}, 200
        except:
            return {'error': "Unable to delete todo", "traceback": str(sys.exc_info())}

    def edit_user(self, id, name, password):
        try:
            if name is None and password is None:
                return {'response': 'User was edited, put the provided data was the same as the previous one.'}, 200
            else:
                if name is not None and password is None:
                    self.cur.execute(
                        "UPDATE users SET name = %s WHERE id = %s", (name, id))
                elif name is None and password is not None:
                    self.cur.execute(
                        "UPDATE users SET password = %s WHERE id = %s", (password, id))
                else:
                    self.cur.execute(
                        "UPDATE users SET name = %s , password = %s WHERE id = %s", (name, password, id))
                    self.conn.commit()
                return {'response': 'User was edited'}, 200
        except:
            return {'error': "Unable to edit user", "traceback": str(sys.exc_info())}

    def delete_user(self, id):
        try:
            self.cur.execute(
                "DELETE FROM users WHERE id = %s", (id))
            self.conn.commit()
            return {'response': 'User deleted'}, 200
        except:
            return {'error': "Unable to delete user", "traceback": str(sys.exc_info())}
