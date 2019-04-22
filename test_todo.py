from todo import app, tasks
import json

def test_list_tasks_should_return_200():
    app.config['TESTING'] = True
    with app.test_client() as client:
        response = client.get('/tasks')
        assert response.status_code == 200

def test_list_tasks_should_be_json():
    app.config['TESTING'] = True
    with app.test_client() as client:
        response = client.get('/tasks')
        assert response.content_type == 'application/json'

def test_list_tasks_when_empty_should_return_empty_list():
    app.config['TESTING'] = True
    with app.test_client() as client:
        response = client.get('/tasks')
        assert response.json == []

def test_list_tasks_nonempty_returns_content():
    tasks.append({'id': 1, 'title': 'task 1', 'description': 'task number 1', 'status': False})
    app.config['TESTING'] = True
    with app.test_client() as client:
        response = client.get('/tasks')
        assert response.json == [{
            'id': 1,
            'title': 'task 1',
            'description': 'task number 1',
            'status': False
        }]
    tasks.clear()


def test_create_task_with_post():
    with app.test_client() as client:
        response = client.post('/task', data=json.dumps({
        'title': 'task 1',
        'description': 'my first task'}),
        content_type='application/json')
        assert response.status_code != 405


def test_create_task_returns_new_task():
    tasks.clear()
    client = app.test_client()
    response = client.post('/task', data=json.dumps({
        'title': 'task 1',
        'description': 'my first task'}),
        content_type='application/json')
    data = json.loads(response.data.decode('utf-8'))
    assert data['id'] == 1
    assert data['title'] == 'task 1'
    assert data['description'] == 'my first task'
    assert data['status'] is False

def test_create_task_should_return_201():
    with app.test_client() as client:
        response = client.post('/task', data=json.dumps({
            'title': 'task 1',
            'description': 'my first task'}),
            content_type='application/json')
        assert response.status_code == 201


def test_create_task_insert_entry_database():
    tasks.clear()
    client = app.test_client()
    client.post('/task', data=json.dumps({
            'title': 'task 1',
            'description': 'my first task'}),
            content_type='application/json')
    assert len(tasks) > 0