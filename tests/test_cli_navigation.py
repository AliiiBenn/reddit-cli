"""Tests for navigation commands: frontpage, home, best."""
import pytest
import respx
import httpx
from typer.testing import CliRunner

from reddit_cli import app


class TestFrontpage:
    """Test suite for frontpage command."""

    def test_frontpage_exit_code(self, runner: CliRunner, mock_reddit_base, sample_navigation_response):
        """frontpage should exit with code 0."""
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["frontpage"])
        assert result.exit_code == 0

    def test_frontpage_output_contains_post(
        self, runner: CliRunner, mock_reddit_base, sample_navigation_response
    ):
        """frontpage output should contain post title."""
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["frontpage"])
        assert "Test Post" in result.output

    def test_frontpage_with_limit(self, runner: CliRunner, mock_reddit_base, sample_navigation_response):
        """frontpage should accept --limit option."""
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["frontpage", "--limit", "5"])
        assert result.exit_code == 0

    def test_frontpage_with_sort(self, runner: CliRunner, mock_reddit_base, sample_navigation_response):
        """frontpage should accept --sort option."""
        mock_reddit_base.get("/r/reddit/new.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["frontpage", "--sort", "new"])
        assert result.exit_code == 0


class TestHome:
    """Test suite for home command."""

    def test_home_exit_code(self, runner: CliRunner, mock_reddit_base, sample_navigation_response):
        """home should exit with code 0."""
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["home"])
        assert result.exit_code == 0

    def test_home_is_alias_for_frontpage(self, runner: CliRunner, mock_reddit_base, sample_navigation_response):
        """home should produce similar output to frontpage."""
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["home"])
        assert "Test Post" in result.output


class TestBest:
    """Test suite for best command."""

    def test_best_exit_code(self, runner: CliRunner, mock_reddit_base, sample_navigation_response):
        """best should exit with code 0."""
        mock_reddit_base.get("/r/reddit/top.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["best"])
        assert result.exit_code == 0

    def test_best_output_contains_post(self, runner: CliRunner, mock_reddit_base, sample_navigation_response):
        """best output should contain post title."""
        mock_reddit_base.get("/r/reddit/top.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["best"])
        assert "Test Post" in result.output

    def test_best_with_period(self, runner: CliRunner, mock_reddit_base, sample_navigation_response):
        """best should accept --period option."""
        mock_reddit_base.get("/r/reddit/top.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["best", "--period", "month"])
        assert result.exit_code == 0


class TestNavigationPagination:
    """Test suite for navigation pagination (--after/--before)."""

    def test_frontpage_with_after_cursor(
        self, runner: CliRunner, mock_reddit_base, sample_navigation_response
    ):
        """frontpage should accept --after option."""
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["frontpage", "--after", "t3_previous"])
        assert result.exit_code == 0

    def test_frontpage_with_before_cursor(
        self, runner: CliRunner, mock_reddit_base, sample_navigation_response
    ):
        """frontpage should accept --before option."""
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["frontpage", "--before", "t3_next"])
        assert result.exit_code == 0

    def test_best_with_after_cursor(
        self, runner: CliRunner, mock_reddit_base, sample_navigation_response
    ):
        """best should accept --after option."""
        mock_reddit_base.get("/r/reddit/top.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["best", "--after", "t3_previous"])
        assert result.exit_code == 0
