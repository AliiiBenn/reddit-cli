"""Tests for global search command."""
import pytest
import respx
import httpx
from typer.testing import CliRunner

from reddit_cli import app


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


class TestSearch:
    """Test suite for global search command."""

    def test_search_exit_code(self, runner: CliRunner, mock_reddit_base, sample_search_response):
        """search should exit with code 0."""
        mock_reddit_base.get("/search.json").mock(
            return_value=httpx.Response(200, json=sample_search_response)
        )
        result = runner.invoke(app, ["search", "python"])
        assert result.exit_code == 0

    def test_search_output_contains_results(
        self, runner: CliRunner, mock_reddit_base, sample_search_response
    ):
        """search output should contain results."""
        mock_reddit_base.get("/search.json").mock(
            return_value=httpx.Response(200, json=sample_search_response)
        )
        result = runner.invoke(app, ["search", "python"])
        assert "How to learn Python" in result.output
        assert "Best Python frameworks" in result.output

    def test_search_output_contains_subreddits(
        self, runner: CliRunner, mock_reddit_base, sample_search_response
    ):
        """search output should contain subreddit names."""
        mock_reddit_base.get("/search.json").mock(
            return_value=httpx.Response(200, json=sample_search_response)
        )
        result = runner.invoke(app, ["search", "python"])
        assert "learnprogramming" in result.output
        assert "python" in result.output

    def test_search_missing_query(self, runner: CliRunner):
        """search should fail without query."""
        result = runner.invoke(app, ["search"])
        assert result.exit_code != 0

    def test_search_with_sort(self, runner: CliRunner, mock_reddit_base, sample_search_response):
        """search should accept --sort option."""
        mock_reddit_base.get("/search.json").mock(
            return_value=httpx.Response(200, json=sample_search_response)
        )
        result = runner.invoke(app, ["search", "python", "--sort", "new"])
        assert result.exit_code == 0

    def test_search_with_limit(self, runner: CliRunner, mock_reddit_base, sample_search_response):
        """search should accept --limit option."""
        mock_reddit_base.get("/search.json").mock(
            return_value=httpx.Response(200, json=sample_search_response)
        )
        result = runner.invoke(app, ["search", "python", "--limit", "10"])
        assert result.exit_code == 0

    def test_search_with_period(self, runner: CliRunner, mock_reddit_base, sample_search_response):
        """search should accept --period option."""
        mock_reddit_base.get("/search.json").mock(
            return_value=httpx.Response(200, json=sample_search_response)
        )
        result = runner.invoke(app, ["search", "python", "--period", "week"])
        assert result.exit_code == 0

    def test_search_no_results(self, runner: CliRunner, mock_reddit_base):
        """search should handle no results gracefully."""
        empty_response = {"data": {"children": [], "after": None, "before": None}}
        mock_reddit_base.get("/search.json").mock(
            return_value=httpx.Response(200, json=empty_response)
        )
        result = runner.invoke(app, ["search", "xyzzynonexistentquery12345"])
        assert result.exit_code == 0
        assert "No posts found" in result.output
