import pytest
import asyncio
from app.services.users import user_service
from app.core.utils import hash_password
from app.services.errors import UserExistError, UserNotFoundError
from app.services.errors import UsernameError, PasswordError

@pytest.mark.asyncio
async def test_create_user(mock_users_write, mock_users_read):
    mock_users_read.return_value = []
    fake_data = {'username': 'aaa', 'password': 'bbb', 'role': 'ccc'}
    response = await user_service.create_user(fake_data)

    assert response['username'] == fake_data['username']
    assert 'id' in response

    # test with existing username to check if error is raised
    with pytest.raises(UserExistError) as exc:
        await user_service.create_user(fake_data)
    assert 'Username already exist!' == str(exc.value)

    mock_users_write.assert_called_once_with('users.json', [response])  # write_json call

@pytest.mark.asyncio
async def test_get_user(mock_users_write, mock_users_read):
    mock_users_read.return_value = []
    fake_data = {'username': 'aaa', 'password': 'bbb', 'role': 'ccc'}
    await user_service.create_user(fake_data)

    response = await user_service.get_user(fake_data['username'])

    with pytest.raises(UserNotFoundError) as exc:
        await user_service.get_user('bbb')

    assert 'User not found!' == str(exc.value)
    assert response['username'] == 'aaa'

    mock_users_write.assert_called_once_with('users.json', [response])

@pytest.mark.asyncio
async def test_get_users(mock_users_write, mock_users_read):
    mock_users_read.return_value = []
    fake_data1 = {'username': 'aaa', 'password': 'bbb', 'role': 'ccc'}
    fake_data2 = {'username': 'eee', 'password': 'fff', 'role': 'zzz'}
    fake_data3 = {'username': 'rrr', 'password': 'fff', 'role': 'zzz'}
    res1 = await user_service.create_user(fake_data1)
    res2 = await user_service.create_user(fake_data2)
    res3 = await user_service.create_user(fake_data3)

    users = await user_service.get_users()
    assert res3 in users

    filter_users = await user_service.get_users('zzz')
    assert res2 in filter_users

    mock_users_write.assert_called_with('users.json', [res1,res2,res3])

@pytest.mark.asyncio
async def test_sign_user_in(mock_users_write, mock_users_read):
    mock_users_read.return_value = []
    fake_data = {'username': 'aaa', 'password': 'bbb', 'role': 'ccc'}
    await user_service.create_user(fake_data)

    response = await user_service.sign_user_in('1', fake_data['username'],
                                               fake_data['password'])
    assert 'token' in response

    with pytest.raises((UsernameError, PasswordError)) as exc:
        await user_service.sign_user_in('1', 'bbc', fake_data['password'])
    assert 'Invalid username!' == str(exc.value)

    with pytest.raises((UsernameError, PasswordError)) as exc:
        await user_service.sign_user_in('1', fake_data['username'], 'zzz')
    assert 'Invalid password!' == str(exc.value)

    mock_users_write.assert_called_with('users.json', [response])

@pytest.mark.asyncio
async def test_sign_user_out(mock_users_write, mock_users_read):
    mock_users_read.return_value = []
    fake_data = {'username': 'aaa', 'password': 'bbb', 'role': 'ccc'}
    await user_service.create_user(fake_data)
    await user_service.sign_user_in('1', fake_data['username'], fake_data['password'])

    response = await user_service.sign_user_out('1')
    assert 'token' not in response

    mock_users_write.assert_called_with('users.json', [response])

@pytest.mark.asyncio
async def test_update_account(mock_users_write, mock_users_read):
    mock_users_read.return_value = []
    fake_data = {'username': 'aaa', 'password': 'bbb', 'role': 'ccc'}
    res = await user_service.create_user(fake_data)

    response = await user_service.update_account('1', {'role': 'zze'}, fake_data['password'])
    assert res['role'] == 'zze'

    with pytest.raises((UserNotFoundError, PasswordError)) as exc:
        await user_service.update_account('2', {'role': 'aaa'},
                                          fake_data['password'])
    assert 'User not found!' == str(exc.value)

    with pytest.raises((UserNotFoundError, PasswordError)) as exc:
        await user_service.update_account('1', {'role': 'aaa'}, 'bbB')
    assert 'Invalid password!' == str(exc.value)

    mock_users_write.assert_called_with('users.json', [response])

@pytest.mark.asyncio
async def test_update_password(mock_users_write, mock_users_read):
    mock_users_read.return_value = []
    fake_data = {'username': 'aaa', 'password': 'bbb', 'role': 'ccc'}
    res = await user_service.create_user(fake_data)

    await user_service.update_password('1', fake_data['password'], 'bbt')
    assert res['password'] == hash_password('bbt')

    with pytest.raises((UserNotFoundError, PasswordError)) as exc:
        await user_service.update_password('2', fake_data['password'], 'ttt')
    assert 'User not found!' == str(exc.value)

    with pytest.raises((UserNotFoundError, PasswordError)) as exc:
        await user_service.update_password('1', 'bbB', 'pbp')
    assert 'Invalid password!' == str(exc.value)

    mock_users_write.assert_called_with('users.json', [res])

@pytest.mark.asyncio
async def test_delete_account(mock_users_write, mock_users_read):
    mock_users_read.return_value = []
    fake_data = {'username': 'aaa', 'password': 'bbb', 'role': 'ccc'}
    response = await user_service.create_user(fake_data)

    await user_service.delete_account('1')
    assert fake_data not in mock_users_read.return_value

    with pytest.raises((UserNotFoundError, PasswordError)) as exc:
        await user_service.delete_account('2')
    assert 'User not found!' == str(exc.value)

    mock_users_write.assert_called_with('users.json', [])
