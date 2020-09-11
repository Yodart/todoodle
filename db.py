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

    def get_todos(self,limit = 5,offset = 0):
        self.cur.execute("SELECT id, title, completed,created_at FROM todos ORDER BY created_at LIMIT %s OFFSET %s",(limit,offset))
        return jsonify([{'id':x[0],'title':x[1],'completed':x[2],'created_at':x[3]} for x in self.cur.fetchall()])
    
    def get_single_todo(self,todo_id):
        self.cur.execute("SELECT id, title, completed,created_at FROM todos WHERE id=%s ",(todo_id))
        response = self.cur.fetchall()[0]
        return {'id':response[0],'title':response[1],'completed':response[2],'created_at':response[3]}

    def create_todo(self,title):
         self.cur.execute("INSERT INTO todos (title,completed) values(%s,%s)",(title,'false'))
         self.conn.commit()
         return {'response':'new todo created'}, 200

    def create_random_todo(self):
         self.create_todo(rw.get_random_word())
         return {'response':'new todo created'}, 200


       