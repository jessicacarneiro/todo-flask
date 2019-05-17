from flask import Flask, jsonify, request, abort, render_template,\
    redirect, session, flash, url_for
from operator import itemgetter
import json
import sys

app = Flask('TodoApp')
app.config.from_pyfile('config_file.cfg')
tasks = []
logins = {
    'jessicacarneiro': '123456',
    'adalovelace': '123456'
}

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/tasks')
def list():
    return render_template('display.html', tasks=tasks)

@app.route('/add')
def add_page():
    return render_template('add.html')

@app.route('/tasks', methods=['POST'])
def add():
    if request.content_type == 'application/json':
        title = request.json.get('title')
        description = request.json.get('description')
        task = {
        'id': len(tasks) + 1,
        'title': title,
        'description': description,
        'status': False
        }
        if not title or not description:
            abort(400)
        tasks.append(task)
        return jsonify(task), 201
    else:
        title = request.form['title']
        description = request.form['description']
        task = {
        'id': len(tasks) + 1,
        'title': title,
        'description': description,
        'status': False
        }
        if not title or not description:
            abort(400)
        tasks.append(task)
        return redirect(url_for('list'))

@app.route('/remove_page')
def remove_page():
    return render_template('delete.html', tasks=tasks)

@app.route('/remove', methods=['POST'])
def remove():
    task_id = int(request.form['task'].partition(':')[0])
    task = [task for task in tasks if task['id'] == task_id]
    if not task:
        abort(404)
    tasks.remove(task[0])
    return redirect(url_for('index'))

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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    login = request.form['login']
    if login in logins:
        session['logged_user'] = login
        flash('{} logged in successfully!'.format(login))
        return redirect(url_for('index'))
    else:
        flash('{} does not exist!'.format(login))
        return redirect(url_for('login'))