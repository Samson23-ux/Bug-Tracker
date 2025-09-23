import pytest, asyncio

bug_data={
            'title': 'hhh',
            'description': 'aaa',
            'severity': 'sss',
            'status': 'eeee',
            'reporter': 'ggg',
}

@pytest.mark.asyncio
async def test_get_bugs(test_client, bug_create):
    user_sign_in, _ = bug_create

    response = test_client.get(
        '/bugs/',
        headers={'Authorization': user_sign_in.json()['data']['token']}
    )
    assert response.status_code == 200
    assert response.json()['data'][0]['title'] =='hhh'

@pytest.mark.asyncio
async def test_get_reported_bugs(test_client, bug_create):
    user_sign_in, _ = bug_create

    response = test_client.get(
        '/bugs/user/',
        headers={'Authorization': user_sign_in.json()['data']['token']}
    )
    assert response.status_code == 200
    assert response.json()['data'][0]['reporter'] == 'timothy'

@pytest.mark.asyncio
async def test_get_assigned_bugs(test_client, bug_create):
    user, _ = bug_create
    user_sign_in = test_client.post(
        '/auth/sign-in/2/',
        data={
            'username': 'gasmine',
            'password': 'thailand'
        }
    )

    test_client.patch(
        '/bugs/1/assign/',
        json={'assignee': 'timothy'},
        headers={'Authorization': user_sign_in.json()['data']['token']}
    )

    response = test_client.get(
        '/bugs/developer/',
        headers={'Authorization': user.json()['data']['token']}
    )

    assert response.status_code == 200
    assert response.json()['data'][0]['assignee'] == 'timothy'

@pytest.mark.asyncio
async def test_get_bug(test_client, bug_create):
    user_sign_in, _ = bug_create

    response = test_client.get(
        '/bugs/hhh/',
        headers={'Authorization': user_sign_in.json()['data']['token']}
    )
    assert response.status_code == 200
    assert response.json()['data']['title'] == 'hhh'

@pytest.mark.asyncio
async def test_create_bug(test_client, bug_create):
    _, bug = bug_create
    assert bug.status_code == 201
    assert bug.json()['data']['title'] == bug_data['title']

@pytest.mark.asyncio
async def test_assign_bug(test_client, bug_create):
    user_sign_in = test_client.post(
        '/auth/sign-in/2/',
        data={
            'username': 'gasmine',
            'password': 'thailand'
        }
    )

    response = test_client.patch(
        '/bugs/1/assign/',
        json={'assignee': 'timothy'},
        headers={'Authorization': user_sign_in.json()['data']['token']}
    )

    assert response.status_code == 200
    assert response.json()['data']['assignee'] == 'timothy'

@pytest.mark.asyncio
async def test_update_bug(test_client, bug_create):
    user_sign_in, _ = bug_create

    response = test_client.patch(
        '/bugs/1/',
        json={'severity': 'a'},
        headers={'Authorization': user_sign_in.json()['data']['token']}
    )

    assert response.status_code == 200
    assert response.json()['data']['severity'] == 'a'

@pytest.mark.asyncio
async def test_update_bug_status(test_client, bug_create):
    user_sign_in, _ = bug_create

    response = test_client.patch(
        '/bugs/1/status/',
        json={'status': 'aaa'},
        headers={'Authorization': user_sign_in.json()['data']['token']}
    )

    assert response.status_code == 200
    assert response.json()['data']['status'] =='aaa'

@pytest.mark.asyncio
async def test_delete_bug(test_client, bug_create):
    user_sign_in, _ = bug_create

    bugs = response = test_client.get(
        '/bugs/',
        headers={'Authorization': user_sign_in.json()['data']['token']}
    )

    response = test_client.delete(
        '/bugs/1/',
        headers={'Authorization': user_sign_in.json()['data']['token']}
    )

    assert response.status_code == 204
    assert bug_data not in bugs.json()['data']
