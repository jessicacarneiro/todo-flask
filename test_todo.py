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

def test_create_task_without_description():
    client = app.test_client()
    response = client.post('/task', data=json.dumps({
        'title': 'task 1'}),
        content_type='application/json')
    assert response.status_code == 400

def test_create_task_without_title():
    client = app.test_client()
    response = client.post('/task', data=json.dumps({
        'description': 'my first task'}),
        content_type='application/json')
    assert response.status_code == 400

def test_list_tasks_should_present_unfinished_first():
    tasks.clear()
    tasks.append({
            'id':1,
            'title':'task 1',
            'description':'test 1',
            'status':True})
    tasks.append({'id':2,
                  'title':'task 2',
                  'description':'test 2',
                  'status':False})
    with app.test_client() as client:
        response = client.get('/tasks')
        data = json.loads(response.data.decode('utf-8'))
        first, second = data
        assert first['title'] == 'task 2'
        assert second['title'] == 'task 1'

def test_delete_task_with_delete_verb():
    tasks.clear()
    with app.test_client() as client:
        response = client.delete('/task/1')
        assert response.status_code != 405

def test_delete_existing_task_returns_204():
        tasks.clear()
        tasks.append({
                'id': 1,
                'title': 'task',
                'description': 'task number 1',
                'status': False
        })
        client = app.test_client()
        response = client.delete('/task/1', content_type='application/json')
        assert response.status_code == 204
        assert response.data == b''

def test_delete_existing_test_works():
        tasks.clear()
        tasks.append({
                'id': 1,
                'title': 'task',
                'description': 'task number 1',
                'status': False
        })
        client = app.test_client()
        response = client.delete('/task/1', content_type='application/json')
        assert response.status_code == 204
        assert len(tasks) == 0

def test_detail_existing_task():
        tasks.clear()
        tasks.append({
                'id': 1,
                'title': 'task 1',
                'description': 'my first task',
                'status': False
        })
        client = app.test_client()
        response = client.get('/task/1', content_type='application/json')
        data = json.loads(response.data.decode('utf-8'))
        assert response.status_code == 200
        assert data['id'] == 1
        assert data['title'] == 'task 1'
        assert data['description'] == 'my first task'
        assert data['status'] is False

def test_detail_nonexisting_task():
        tasks.clear()
        client = app.test_client()
        response = client.get('/task/1', content_type='application/json')
        assert response.status_code == 404

def test_updating_exiting_task():
        tasks.clear()
        tasks.append({
                'id': 1,
                'title': 'task 1',
                'description': 'my first task',
                'status': False
        })
        client = app.test_client()
        response = client.put('/task/1', data=json.dumps({
                'title': 'updated title',
                'description': 'updated description',
                'status': True
                }
        ), content_type='application/json')
        data = json.loads(response.data.decode('utf-8'))
        assert response.status_code == 200
        assert data['id'] == 1
        assert data['title'] == 'updated title'
        assert data['description'] == 'updated description'
        assert data['status'] is True

def test_updating_nonexiting_task():
        tasks.clear()
        client = app.test_client()
        response = client.put('/task/1', data=json.dumps({
                'title': 'updated title',
                'description': 'updated description',
                'status': True
                }
        ), content_type='application/json')
        assert response.status_code == 404

def test_update_task_with_invalide_fields():
        tasks.clear()
        tasks.append({
                'id': 1,
                'title': 'task 1',
                'description': 'my first task',
                'status': False
        })
        client = app.test_client()
        # without status
        response = client.put('/task/1', data=json.dumps({
                'title': 'updated title',
                'description': 'updated description'
                }
        ), content_type='application/json')
        assert response.status_code == 400
        # without title
        response = client.put('/task/1', data=json.dumps({
                'description': 'updated description',
                'status': True
                }
        ), content_type='application/json')
        assert response.status_code == 400
        # without description
        response = client.put('/task/1', data=json.dumps({
                'title': 'updated title',
                'status': True
                }
        ), content_type='application/json')
        assert response.status_code == 400
