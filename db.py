import psycopg2
import random
from random_word import RandomWords

rw = RandomWords()

class Database:
    def __init__(self, db):
        self.db = db
        self.conn = psycopg2.connect(database=self.db)
        self.cur = self.conn.cursor()
    def query_todos(self):
        self.cur.execute("SELECT id, title, completed,created_at FROM todos ORDER BY created_at LIMIT 5")
        rows = self.cur.fetchall()
        return {'todos':[{'id':x[0],'title':x[1],'completed':x[2]} for x in rows]}

    def create_todo(self,title):
         self.cur.execute("INSERT INTO todos (title,completed) values(%s,%s)",(title,'false'))
         self.conn.commit()
         return {'response':'new todo created'}, 200
    def create_random_todo(self):
         self.create_todo(rw.get_random_word())
         return {'response':'new todo created'}, 200

       