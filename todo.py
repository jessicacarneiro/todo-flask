from flask import Flask, jsonify

app = Flask('TodoApp')

tasks = []

@app.route('/tasks')
def list():
    return jsonify(tasks)