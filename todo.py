from flask import Flask

app = Flask('TodoApp')

@app.route('/tasks')
def list():
    return ''