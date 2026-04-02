"""Shared fixtures for CLI tests."""
import pytest
import respx
import httpx
from typer.testing import CliRunner



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


@pytest.fixture
def sample_navigation_response() -> dict:
    """Sample navigation (frontpage/home/best) response.

    This fixture was extracted from TestFrontpage._sample_response() to avoid
    coupling between test classes.
    """
    return {
        "data": {
            "children": [
                {
                    "kind": "t3",
                    "data": {
                        "id": "abc123",
                        "title": "Test Post Title",
                        "score": 100,
                        "num_comments": 42,
                        "author": "testuser",
                        "subreddit": "reddit",
                        "url": "https://example.com",
                        "permalink": "/r/reddit/comments/abc123/test/",
                        "selftext": "",
                        "created_utc": 1704067200,
                    },
                }
            ],
            "after": None,
            "before": None,
        }
    }


@pytest.fixture
def sample_search_response() -> dict:
    """Sample search results response."""
    return {
        "data": {
            "children": [
                {
                    "kind": "t3",
                    "data": {
                        "id": "search1",
                        "title": "How to learn Python in 2024",
                        "score": 500,
                        "num_comments": 100,
                        "author": "python_learner",
                        "subreddit": "learnprogramming",
                        "url": "https://example.com/python-guide",
                        "permalink": "/r/learnprogramming/comments/search1/python_guide/",
                        "selftext": "I'm looking for resources to learn Python",
                        "created_utc": 1704067200,
                    },
                },
                {
                    "kind": "t3",
                    "data": {
                        "id": "search2",
                        "title": "Best Python frameworks comparison",
                        "score": 300,
                        "num_comments": 75,
                        "author": "framework_dev",
                        "subreddit": "python",
                        "url": "https://example.com/frameworks",
                        "permalink": "/r/python/comments/search2/frameworks/",
                        "selftext": "Django vs Flask vs FastAPI",
                        "created_utc": 1704067200,
                    },
                },
            ],
            "after": "t3_after2",
            "before": None,
        }
    }


@pytest.fixture
def empty_posts_response() -> dict:
    """Empty posts response for testing no results."""
    return {
        "data": {
            "children": [],
            "after": None,
            "before": None,
        }
    }


@pytest.fixture
def error_response_404() -> httpx.Response:
    """HTTP 404 error response."""
    return httpx.Response(404, json={"error": 404, "message": "Not Found"})


@pytest.fixture
def error_response_500() -> httpx.Response:
    """HTTP 500 error response."""
    return httpx.Response(500, json={"error": 500, "message": "Internal Server Error"})


@pytest.fixture
def error_response_403() -> httpx.Response:
    """HTTP 403 error response (for moderator privacy)."""
    return httpx.Response(403, json={"error": 403, "message": "Forbidden"})


@pytest.fixture
def error_response_429() -> httpx.Response:
    """HTTP 429 error response (rate limiting)."""
    return httpx.Response(429, json={"error": 429, "message": "Too Many Requests"})
