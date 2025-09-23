import pytest, asyncio

@pytest.mark.asyncio
async def test_get_users(test_client, user_create):
    response = test_client.get('/users/')
    assert response.status_code == 200
    assert len(response.json()['data']) >= 1

@pytest.mark.asyncio
async def test_get_filter_users(test_client, user_create):
    response = test_client.get('/users/', params={'role': 'developer'})
    assert response.status_code == 200
    assert len(response.json()['data']) >= 1
    assert user_create.json()['data'] in response.json()['data']

@pytest.mark.asyncio
async def test_get_user(test_client, user_create):
    response = test_client.get('/users/timothy/')
    assert response.status_code == 200
    assert response.json()['data']['username'] == 'timothy'

@pytest.mark.asyncio
async def test_update_account(test_client, user_sign_in):
    response = test_client.patch(
        '/users/1/',
        json={'username': 'titus', 'password': 'thailand'},
        headers={'Authorization': user_sign_in.json()['data']['token']}
    )
    assert response.status_code == 200
    assert response.json()['data']['username'] == 'titus'

@pytest.mark.asyncio
async def test_delete_account(test_client, user_sign_in):
    response = test_client.delete(
        '/users/1/',
        headers={'Authorization': user_sign_in.json()['data']['token']}
    )

    users = test_client.get('/users/')

    assert response.status_code == 204
    assert user_sign_in.json()['data'] not in users.json()['data']
