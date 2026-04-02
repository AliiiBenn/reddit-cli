"""Tests for browse commands: browse, sticky, random, browse search."""
import pytest
import respx
import httpx
from typer.testing import CliRunner

from reddit_cli import app


@pytest.fixture
def sample_browse_response() -> dict:
    """Sample browse subreddit response."""
    return {
        "data": {
            "children": [
                {
                    "kind": "t3",
                    "data": {
                        "id": "post1",
                        "title": "Python Tip of the Day",
                        "score": 500,
                        "num_comments": 100,
                        "author": "pythonista",
                        "subreddit": "python",
                        "url": "https://example.com/python-tip",
                        "permalink": "/r/python/comments/post1/python_tip/",
                        "selftext": "Use enumerate() instead of range()",
                        "created_utc": 1704067200,
                    },
                }
            ],
            "after": "t3_after1",
            "before": None,
        }
    }


@pytest.fixture
def sample_sticky_response() -> dict:
    """Sample sticky post response."""
    return {
        "data": {
            "children": [
                {
                    "kind": "t3",
                    "data": {
                        "id": "sticky1",
                        "title": "Welcome to r/python!",
                        "score": 1000,
                        "num_comments": 50,
                        "author": "AutoModerator",
                        "subreddit": "python",
                        "url": "https://reddit.com/r/python/welcome",
                        "permalink": "/r/python/comments/sticky1/welcome/",
                        "selftext": "Read the rules before posting",
                        "created_utc": 1704067200,
                        "stickied": True,
                    },
                }
            ],
            "after": None,
            "before": None,
        }
    }


class TestBrowse:
    """Test suite for browse command."""

    def test_browse_exit_code(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse should exit with code 0."""
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "python"])
        assert result.exit_code == 0

    def test_browse_output_contains_title(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse output should contain post title."""
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "python"])
        assert "Python Tip of the Day" in result.output

    def test_browse_with_limit(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse should accept --limit option."""
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "--limit", "10", "python"])
        assert result.exit_code == 0

    def test_browse_with_sort(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse should accept --sort option."""
        mock_reddit_base.get("/r/python/new.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "--sort", "new", "python"])
        assert result.exit_code == 0

    def test_browse_with_period(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse should accept --period option."""
        mock_reddit_base.get("/r/python/top.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "--sort", "top", "--period", "week", "python"])
        assert result.exit_code == 0

    def test_browse_missing_subreddit(self, runner: CliRunner):
        """browse should fail without subreddit argument."""
        result = runner.invoke(app, ["browse"])
        assert result.exit_code != 0


class TestBrowseSticky:
    """Test suite for browse sticky command."""

    def test_sticky_exit_code(
        self, runner: CliRunner, mock_reddit_base, sample_sticky_response
    ):
        """browse sticky should exit with code 0."""
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=httpx.Response(200, json=sample_sticky_response)
        )
        result = runner.invoke(app, ["browse", "sticky", "python"])
        assert result.exit_code == 0

    def test_sticky_output_contains_post(
        self, runner: CliRunner, mock_reddit_base, sample_sticky_response
    ):
        """browse sticky output should contain sticky post."""
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=httpx.Response(200, json=sample_sticky_response)
        )
        result = runner.invoke(app, ["browse", "sticky", "python"])
        assert "Welcome to r/python" in result.output


class TestBrowseRandom:
    """Test suite for browse random command."""

    def test_random_exit_code(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse random should exit with code 0."""
        mock_reddit_base.get("/r/python/random.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "random", "python"])
        assert result.exit_code == 0

    def test_random_output_contains_post(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse random output should contain post."""
        mock_reddit_base.get("/r/python/random.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "random", "python"])
        assert "Python Tip of the Day" in result.output


class TestBrowseSearch:
    """Test suite for browse search command."""

    def test_browse_search_exit_code(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse search should exit with code 0."""
        mock_reddit_base.get("/r/python/search.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "search", "python", "django"])
        assert result.exit_code == 0

    def test_browse_search_output_contains_query(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse search output should mention the query."""
        mock_reddit_base.get("/r/python/search.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "search", "python", "django"])
        assert "django" in result.output.lower()

    def test_browse_search_missing_args(self, runner: CliRunner):
        """browse search should require both subreddit and query."""
        result = runner.invoke(app, ["browse", "search", "python"])
        assert result.exit_code != 0
