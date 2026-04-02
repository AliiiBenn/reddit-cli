"""Tests for global search command."""
import pytest
import httpx
from typer.testing import CliRunner

from reddit_cli import app


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

    @pytest.mark.parametrize("sort_option", ["relevance", "hot", "top", "new", "comments"])
    def test_search_with_sort_option(
        self, runner: CliRunner, mock_reddit_base, sample_search_response, sort_option
    ):
        """search should accept various --sort options."""
        mock_reddit_base.get("/search.json").mock(
            return_value=httpx.Response(200, json=sample_search_response)
        )
        result = runner.invoke(app, ["search", "python", "--sort", sort_option])
        assert result.exit_code == 0

    @pytest.mark.parametrize("limit_value", [5, 10, 25, 50])
    def test_search_with_limit_option(
        self, runner: CliRunner, mock_reddit_base, sample_search_response, limit_value
    ):
        """search should accept various --limit options."""
        mock_reddit_base.get("/search.json").mock(
            return_value=httpx.Response(200, json=sample_search_response)
        )
        result = runner.invoke(app, ["search", "python", "--limit", str(limit_value)])
        assert result.exit_code == 0

    @pytest.mark.parametrize("period_option", ["hour", "day", "week", "month", "year", "all"])
    def test_search_with_period_option(
        self, runner: CliRunner, mock_reddit_base, sample_search_response, period_option
    ):
        """search should accept various --period options."""
        mock_reddit_base.get("/search.json").mock(
            return_value=httpx.Response(200, json=sample_search_response)
        )
        result = runner.invoke(app, ["search", "python", "--period", period_option])
        assert result.exit_code == 0

    def test_search_no_results(self, runner: CliRunner, mock_reddit_base, empty_posts_response):
        """search should handle no results gracefully."""
        mock_reddit_base.get("/search.json").mock(
            return_value=httpx.Response(200, json=empty_posts_response)
        )
        result = runner.invoke(app, ["search", "xyzzynonexistentquery12345"])
        assert result.exit_code == 0
        assert "No posts found" in result.output
