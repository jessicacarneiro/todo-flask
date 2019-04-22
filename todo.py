from flask import Flask, jsonify, request
import json

app = Flask('TodoApp')

tasks = []

@app.route('/tasks')
def list():
    return jsonify(tasks)

@app.route('/task', methods=['POST'])
def add():
    title = request.json.get('title')
    description = request.json.get('description')
    task = {
        'id': len(tasks) + 1,
        'title': title,
        'description': description,
        'status': False
    }

    tasks.append(task)
    return jsonify(task), 201