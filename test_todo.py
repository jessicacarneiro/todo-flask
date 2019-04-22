from todo import app

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