import psycopg2
import random
from models import todo
from flask import jsonify
from random_word import RandomWords

rw = RandomWords()


class Database:
    def __init__(self, db):
        self.db = db
        self.conn = psycopg2.connect(database=self.db)
        self.cur = self.conn.cursor()

    def get_todos(self, limit=5, offset=0):
        self.cur.execute(
            "SELECT id, title, completed,created_at FROM todos ORDER BY created_at LIMIT %s OFFSET %s", (limit, offset))
        return jsonify([{'id': x[0], 'title':x[1], 'completed':x[2], 'created_at':x[3]} for x in self.cur.fetchall()])

    def get_single_todo(self, todo_id):
        self.cur.execute(
            "SELECT id, title, completed,created_at FROM todos WHERE id=%s ", (todo_id))
        response = self.cur.fetchall()[0]
        return {'id': response[0], 'title': response[1], 'completed': response[2], 'created_at': response[3]}

    def create_todo(self, title):
        self.cur.execute(
            "INSERT INTO todos (title,completed) values(%s,%s)", (title, 'false'))
        self.conn.commit()
        return {'response': 'new todo created'}, 200

    def edit_todo(self, id, title, completed):
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
