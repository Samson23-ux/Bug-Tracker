import pytest, asyncio

@pytest.mark.asyncio
async def test_create_account(user_create):
    assert user_create.status_code == 201
    response_data = user_create.json()
    assert response_data['message'] == 'Account created successfully!'

@pytest.mark.asyncio
async def test_sign_in(test_client, user_sign_in):
    assert user_sign_in.status_code == 201
    assert 'token' in user_sign_in.json()['data']

@pytest.mark.asyncio
async def test_sign_out(test_client, user_sign_in):
    response = test_client.patch(
        '/auth/sign-out/1/'
    )

    assert response.status_code == 200
    assert 'token' not in response.json()['data']
