from todo import app, tasks

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
