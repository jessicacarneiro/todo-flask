from flask import Flask, jsonify, request, abort, render_template
from operator import itemgetter
import json

app = Flask('TodoApp')
tasks = []

@app.route('/')
def main():
    return render_template('base.html')

@app.route('/tasks')
def list():
    return render_template('display.html', tasks=tasks)

@app.route('/tasks', methods=['POST'])
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

@app.route('/tasks/<int:id_task>', methods=['DELETE'])
def remove(id_task):
    task = [task for task in tasks if task['id'] == id_task]
    if not task:
        abort(404)
    tasks.remove(task[0])
    return '', 204

@app.route('/tasks/<int:id_task>', methods=['GET'])
def detail(id_task):
    task = [task for task in tasks if task['id'] == id_task]
    if not task:
        abort(404)
    return jsonify(task[0])

@app.route('/tasks/<int:id_task>', methods=['PUT'])
def update(id_task):
    task = [task for task in tasks if task['id'] == id_task]
    if not task:
        abort(404)
    title = request.json.get('title')
    description = request.json.get('description')
    status = request.json.get('status')
    if not description or not title or status is None:
        abort(400)
    task_to_update = task[0]
    task_to_update['title'] = title or task_to_update['title']
    task_to_update['description'] = description or task_to_update['description']
    task_to_update['status'] = status or task_to_update['status']
    return jsonify(task_to_update)