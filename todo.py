from flask import Flask, jsonify, request, abort
from operator import itemgetter
import json

app = Flask('TodoApp')

tasks = []

@app.route('/tasks')
def list():
    return jsonify(sorted(tasks, key=itemgetter('status')))

@app.route('/task', methods=['POST'])
def add():
    title = request.json.get('title')
    description = request.json.get('description')
    if not title or not description:
        abort(400)
    task = {
        'id': len(tasks) + 1,
        'title': title,
        'description': description,
        'status': False
    }

    tasks.append(task)
    return jsonify(task), 201

@app.route('/task/<int:id_task>', methods=['DELETE'])
def remove(id_task):
    task = [task for task in tasks if task['id'] == id_task]
    if not task:
        abort(404)
    tasks.remove(task[0])
    return '', 204

@app.route('/task/<int:id_task>', methods=['GET'])
def detail(id_task):
    task = [task for task in tasks if task['id'] == id_task]
    if not task:
        abort(404)
    return jsonify(task[0])