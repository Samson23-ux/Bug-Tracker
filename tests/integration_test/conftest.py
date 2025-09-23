import pytest, json
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

path = Path('app')

@pytest.fixture(scope='module')
def test_client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def user_create(test_client):
    response = test_client.post(
        '/auth/sign-up/',
        json={
            'username': 'timothy',
            'password': 'thailand',
            'role': 'developer'
        }
    )

    test_client.post(
        '/auth/sign-up/',
        json={
            'username': 'gasmine',
            'password': 'thailand',
            'role': 'admin'
        }
    )
    return response

@pytest.fixture
def user_sign_in(test_client, user_create):
    response = test_client.post(
        '/auth/sign-in/1/',
        data={
            'username': 'timothy',
            'password': 'thailand'
        }
    )
    return response

@pytest.fixture
def bug_create(test_client, user_sign_in):
    bug_data={
            'title': 'hhh',
            'description': 'aaa',
            'severity': 'sss',
            'status': 'eeee'
    }
    response = test_client.post(
        '/bugs/',
        json=bug_data,
        headers={'Authorization': user_sign_in.json()['data']['token']}
    )
    return user_sign_in, response

@pytest.fixture(autouse=True)
def reset_files():
    (path/'data\\users.json').write_text(json.dumps([]))
    (path/'data\\bugs.json').write_text(json.dumps([]))
    yield
    (path/'data\\users.json').write_text(json.dumps([]))
    (path/'data\\bugs.json').write_text(json.dumps([]))
