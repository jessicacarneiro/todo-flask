from flask import Flask, jsonify

app = Flask('TodoApp')

@app.route('/tasks')
def list():
    return jsonify([])