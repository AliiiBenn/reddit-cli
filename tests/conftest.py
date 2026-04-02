"""Shared fixtures for CLI tests."""
import pytest
import respx
from typer.testing import CliRunner

from reddit_cli import app


@pytest.fixture
def runner() -> CliRunner:
    """Create a CliRunner instance for testing."""
    return CliRunner()


@pytest.fixture
def mock_reddit_base():
    """Create a respx mock for Reddit API."""
    with respx.mock(base_url="https://www.reddit.com", assert_all_called=False) as respx_mock:
        yield respx_mock


@pytest.fixture
def sample_post_json() -> dict:
    """Sample post JSON from Reddit API."""
    return {
        "data": {
            "id": "abc123",
            "title": "Test Post Title",
            "score": 100,
            "num_comments": 42,
            "author": "testuser",
            "subreddit": "python",
            "url": "https://example.com",
            "permalink": "/r/python/comments/abc123/test_post_title/",
            "selftext": "This is test content.",
            "created_utc": 1704067200,
        }
    }


@pytest.fixture
def sample_posts_response(sample_post_json) -> dict:
    """Sample posts listing response."""
    return {
        "data": {
            "children": [{"kind": "t3", "data": sample_post_json["data"]}],
            "after": "t3_next",
            "before": None,
        }
    }


@pytest.fixture
def sample_comment_json() -> dict:
    """Sample comment JSON."""
    return {
        "data": {
            "id": "def456",
            "body": "This is a test comment",
            "author": "commenter",
            "score": 10,
            "depth": 0,
            "replies": [],
        }
    }


@pytest.fixture
def sample_subreddit_json() -> dict:
    """Sample subreddit JSON."""
    return {
        "data": {
            "name": "python",
            "title": "Python Programming",
            "description": "Subreddit for Python discussion",
            "subscribers": 1000000,
            "active_users": 5000,
        }
    }
