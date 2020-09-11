from flask import Flask,request
from db import Database

app = Flask(__name__)
db = Database("todoodledb")

@app.route('/todos',methods=['GET'])
def get_todos():
    if request.method == 'GET':
        return db.get_todos(limit=15,offset=5)     
    
@app.route('/create_random',methods=['GET'])
def create_random():
    if request.method == 'GET':
        return db.create_random_todo()  

@app.route('/todo/<int:todo_id>',methods=['GET','POST'])
def get_single_todo(todo_id):
    if request.method == 'GET':
        return db.get_single_todo([todo_id])     