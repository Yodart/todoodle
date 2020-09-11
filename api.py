from flask import Flask,request
from db import Database

app = Flask(__name__)
db = Database("todoodledb")

@app.route('/todo',methods=['GET','POST'])
def todo():
    if request.method == 'GET':
        return db.query_todos()     
    elif request.method == 'POST':
        return db.create_todo()