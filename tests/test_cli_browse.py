"""Tests for browse commands: browse, --sticky, --random, --search."""
import pytest
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
        result = runner.invoke(app, ["browse", "python", "--limit", "10"])
        assert result.exit_code == 0

    @pytest.mark.parametrize("sort_option", ["hot", "new", "top", "rising", "controversial"])
    def test_browse_with_sort_option(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response, sort_option
    ):
        """browse should accept various --sort options."""
        mock_reddit_base.get(f"/r/python/{sort_option}.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "python", "--sort", sort_option])
        assert result.exit_code == 0

    @pytest.mark.parametrize("period_option", ["day", "week", "month", "year", "all"])
    def test_browse_with_period_option(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response, period_option
    ):
        """browse should accept various --period options with top sort."""
        mock_reddit_base.get("/r/python/top.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "python", "--sort", "top", "--period", period_option])
        assert result.exit_code == 0

    def test_browse_missing_subreddit(self, runner: CliRunner):
        """browse should fail without subreddit argument."""
        result = runner.invoke(app, ["browse"])
        assert result.exit_code != 0


class TestBrowseSearch:
    """Test suite for browse --search command."""

    def test_browse_search_exit_code(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse python --search should exit with code 0."""
        mock_reddit_base.get("/r/python/search.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "python", "--search", "django"])
        assert result.exit_code == 0

    def test_browse_search_output_contains_query(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse python --search output should mention the query."""
        mock_reddit_base.get("/r/python/search.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "python", "--search", "django"])
        assert "django" in result.output.lower()

    def test_browse_search_missing_query(self, runner: CliRunner):
        """browse python --search should require query."""
        result = runner.invoke(app, ["browse", "python", "--search"])
        assert result.exit_code != 0


class TestBrowsePagination:
    """Test suite for browse pagination (--after/--before)."""

    def test_browse_with_after_cursor(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse should accept --after option for pagination."""
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "python", "--after", "t3_previous"])
        assert result.exit_code == 0
        assert "Python Tip of the Day" in result.output

    def test_browse_with_before_cursor(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse should accept --before option for pagination."""
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "python", "--before", "t3_next"])
        assert result.exit_code == 0
        assert "Python Tip of the Day" in result.output

    def test_browse_with_both_cursors(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse with both --after and --before should work."""
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(
            app, ["browse", "python", "--after", "t3_after1", "--before", "t3_before1"]
        )
        assert result.exit_code == 0

    def test_browse_pagination_output_shows_cursors(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse should display pagination cursors when available."""
        # Response has after="t3_after1" in fixture
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "python"])
        assert result.exit_code == 0
        # The sample_browse_response has after="t3_after1"
        assert "After:" in result.output


class TestBrowseErrorHandling:
    """Test suite for browse error handling."""

    def test_browse_search_no_results(
        self, runner: CliRunner, mock_reddit_base, empty_posts_response
    ):
        """browse --search should handle empty results."""
        mock_reddit_base.get("/r/python/search.json").mock(
            return_value=httpx.Response(200, json=empty_posts_response)
        )
        result = runner.invoke(app, ["browse", "python", "--search", "nonexistent"])
        assert result.exit_code == 0
        assert "No posts found" in result.output
