import pytest
import asyncio
from app.services.bugs import bug_service
from app.services.errors import BugNotFoundError

@pytest.mark.asyncio
async def test_create_bug(mock_bugs_write, mock_bugs_read, set_bugs):
    bug1, bug2 = set_bugs

    assert bug1 in mock_bugs_read.return_value
    assert bug1['reporter'] == 'e'
    assert 'id' in bug1

    mock_bugs_write.assert_called_with('bugs.json', [bug1, bug2])

@pytest.mark.asyncio
async def test_get_bugs(mock_bugs_write, mock_bugs_read, set_bugs):
    bug1, bug2 = set_bugs

    bugs = await bug_service.get_bugs()
    assert bug1 in bugs

    with pytest.raises(BugNotFoundError) as exc:
        mock_bugs_read.return_value = []
        await bug_service.get_bugs()
    assert 'Bug not found' == str(exc.value)

    mock_bugs_write.assert_called_with('bugs.json', [bug1,bug2])

@pytest.mark.asyncio
async def test_get_reported_bugs(mock_bugs_write, mock_bugs_read, set_bugs):
    bug1, bug2 = set_bugs

    bugs = await bug_service.get_reported_bugs('e')
    assert bug2 in bugs

    with pytest.raises(BugNotFoundError) as exc:
        await bug_service.get_reported_bugs('tt')
    assert 'Bug not found' == str(exc.value)

    mock_bugs_write.assert_called_with('bugs.json', [bug1,bug2])

@pytest.mark.asyncio
async def test_get_assigned_bugs(mock_bugs_write, mock_bugs_read, set_bugs):
    bug1, bug2 = set_bugs

    await bug_service.update_bug('1', {'assignee': 'e'})
    bugs = await bug_service.get_assigned_bugs('e')
    assert bug1 in bugs

    with pytest.raises(BugNotFoundError) as exc:
        await bug_service.get_assigned_bugs('tt')
    assert 'Bug not found' == str(exc.value)

    mock_bugs_write.assert_called_with('bugs.json', [bug1,bug2])

@pytest.mark.asyncio
async def test_get_bug(mock_bugs_write, mock_bugs_read, set_bugs):
    bug1, bug2 = set_bugs

    bug = await bug_service.get_bug('a')
    assert bug1 == bug

    with pytest.raises(BugNotFoundError) as exc:
        await bug_service.get_bug('tt')
    assert 'Bug not found' == str(exc.value)

    mock_bugs_write.assert_called_with('bugs.json', [bug1, bug2])

@pytest.mark.asyncio
async def test_update_bug(mock_bugs_write, mock_bugs_read, set_bugs):
    bug1, bug2 = set_bugs

    bug = await bug_service.update_bug('1', {'severity': 'a'})
    assert bug1['severity'] == bug['severity']

    with pytest.raises(BugNotFoundError) as exc:
        await bug_service.update_bug('3', {'title': 'z'})
    assert 'Bug not found' == str(exc.value)

    mock_bugs_write.assert_called_with('bugs.json', [bug1, bug2])

@pytest.mark.asyncio
async def test_delete_bug(mock_bugs_write, mock_bugs_read, set_bugs):
    bug1, bug2 = set_bugs

    await bug_service.delete_bug('1')
    assert bug1 not in mock_bugs_read.return_value

    with pytest.raises(BugNotFoundError) as exc:
        await bug_service.delete_bug('1')
    assert 'Bug not found' == str(exc.value)

    mock_bugs_write.assert_called_with('bugs.json', [bug2])
