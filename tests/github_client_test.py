import pytest
import pytest_asyncio
import json
from unittest.mock import AsyncMock, patch
from github.github_client import GithubClient


@pytest_asyncio.fixture
async def client():
    """Create a GithubClient instance and manage session lifecycle."""
    client = GithubClient()
    await client.start_session()
    yield client
    await client.close_session()


@pytest.mark.asyncio
async def test_start_session(client):
    assert client.session is not None


@pytest.mark.asyncio
async def test_close_session(client):
    await client.close_session()
    assert client.session.closed


@pytest.mark.asyncio
@patch('aiohttp.ClientSession.get')
async def test_get_latest_commits_success(mock_get, client):
    mock_response = AsyncMock(status=200)
    mock_response.text.return_value = json.dumps([{'sha': 'abc123'}])
    mock_get.return_value.__aenter__.return_value = mock_response

    from_date = {'since': '2023-01-01T00:00:00Z'}
    results = await client.get_latest_commits(from_date)
    assert results == ['abc123']


@pytest.mark.asyncio
@patch('aiohttp.ClientSession.get')
async def test_get_latest_commits_failure(mock_get, client):
    mock_response = AsyncMock(status=404)
    mock_get.return_value.__aenter__.return_value = mock_response

    from_date = {'since': '2023-01-01T00:00:00Z'}
    results = await client.get_latest_commits(from_date)
    assert results == []


@pytest.mark.asyncio
@patch('aiohttp.ClientSession.get')
async def test_get_commit_info_success(mock_get, client):
    mock_response = AsyncMock(status=200)
    mock_response.text.return_value = json.dumps({
        'commit': {'message': 'Initial commit'},
        'files': [{
            'filename': 'test.py',
            'additions': 10,
            'deletions': 2,
            'changes': 12,
            'patch': 'Some patch data'
        }]
    })
    mock_get.return_value.__aenter__.return_value = mock_response

    commit_sha = 'abc123'

    content = await client.get_commit_info(commit_sha)
    assert "Initial commit" in content
    assert "test.py" in content
    assert "Some patch data" in content
