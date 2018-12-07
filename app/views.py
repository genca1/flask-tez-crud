#!flask/bin/python

from flask import Flask, jsonify, abort, make_response, request
from flask_restful import Api, Resource, reqparse, fields
from flask_httpauth import HTTPBasicAuth
from flask_pymongo import PyMongo
from app import app
from app import features

api = Api(app)
auth = HTTPBasicAuth()

app.config['MONGO_DBNAME'] = "tasks"
app.config['MONGO_URI'] = "mongodb://localhost:27017/flasker"

mongo = PyMongo(app)



@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
  tasks = mongo.db.tasks
  output = []
  for t in tasks.find():
    output.append({'title' : t['title'], 'description' : t['description']})
  return jsonify({'tasks' : output})

@app.route('/tasks/<title>', methods=['GET'])
def get_one_task(title):
  tasks = mongo.db.tasks
  t = tasks.find_one_or_404({"title" : title})
  if t:
    output = {'title' : t['title'], 'description' : t['description'],'done' : t['done']}
  else:
    output = "No such name"
  return jsonify({'tasks' : output})

@app.route('/tasks/<title>',methods=['PUT'])
def update_task(title):
    data = request.get_json()
    tasks  = mongo.db.tasks
    output = tasks.update({'title':title}, {'$set':data})
    return jsonify({'tasks':output})

@app.route('/tasks/<title>',methods=['DELETE'])
def delete_task(title):
    tasks = mongo.db.tasks
    output = tasks.remove({'title': title})
    return jsonify({'tasks':output})

@app.route('/tasks', methods=['POST'])
def add_task():
  tasks = mongo.db.tasks
  title = request.json['title']
  description = request.json['description']
  done = request.json['done']
  task_id = tasks.insert({'title': title, 'done':done, 'description': description})
  new_task = tasks.find_one({'_id': task_id})
  output = {'title' : new_task['title'], 'done':new_task['done'], 'description' : new_task['description']}
  return jsonify({'tasks' : output})

@app.route('/tasks/forecast/<city>', methods=['GET'])
def get_forecast(city):
  arr = features.forecast.findSehir(city)
  return arr

@app.route('/tasks/currency/<curr>', methods=['GET'])
def get_currency(curr):
  arr = features.currency.findCurrency(curr)
  return arr

@app.route('/tasks/news/<number>', methods=['GET'])
def get_news(number):
  arr = features.news.getNews(int(number))
  return arr