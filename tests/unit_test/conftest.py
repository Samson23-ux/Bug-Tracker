import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.services.bugs import bug_service

@pytest.fixture(scope='module')
def test_client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def mock_users_write():
    # path to where the mocked function is invoked
    with patch('app.services.users.write_json') as mock_write:
        yield mock_write

@pytest.fixture
def mock_users_read():
    with patch('app.services.users.read_json') as mock_read:
        yield mock_read

@pytest.fixture
def mock_bugs_write():
    # path to where the mocked function is invoked
    with patch('app.services.bugs.write_json') as mock_write:
        yield mock_write

@pytest.fixture
def mock_bugs_read():
    with patch('app.services.bugs.read_json') as mock_read:
        mock_read.return_value = []
        yield mock_read

@pytest_asyncio.fixture
async def set_bugs():
    fake_data = {
        'title': 'a',
        'description': 'b',
        'severity': 'c',
        'status': 'd'
    }
    bug1 = await bug_service.report_bug(fake_data, 'e')
    bug2 = await bug_service.report_bug(fake_data, 'e')
    return bug1, bug2
