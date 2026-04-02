"""Tests for navigation commands: frontpage, home, best."""
import pytest
import respx
import httpx
from typer.testing import CliRunner

from reddit_cli import app


class TestFrontpage:
    """Test suite for frontpage command."""

    def test_frontpage_exit_code(self, runner: CliRunner, mock_reddit_base):
        """frontpage should exit with code 0."""
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=self._sample_response())
        )
        result = runner.invoke(app, ["frontpage"])
        assert result.exit_code == 0

    def test_frontpage_output_contains_post(
        self, runner: CliRunner, mock_reddit_base
    ):
        """frontpage output should contain post title."""
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=self._sample_response())
        )
        result = runner.invoke(app, ["frontpage"])
        assert "Test Post" in result.output

    def test_frontpage_with_limit(self, runner: CliRunner, mock_reddit_base):
        """frontpage should accept --limit option."""
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=self._sample_response())
        )
        result = runner.invoke(app, ["frontpage", "--limit", "5"])
        assert result.exit_code == 0

    def test_frontpage_with_sort(self, runner: CliRunner, mock_reddit_base):
        """frontpage should accept --sort option."""
        mock_reddit_base.get("/r/reddit/new.json").mock(
            return_value=httpx.Response(200, json=self._sample_response())
        )
        result = runner.invoke(app, ["frontpage", "--sort", "new"])
        assert result.exit_code == 0

    @staticmethod
    def _sample_response() -> dict:
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


class TestHome:
    """Test suite for home command."""

    def test_home_exit_code(self, runner: CliRunner, mock_reddit_base):
        """home should exit with code 0."""
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=TestFrontpage._sample_response())
        )
        result = runner.invoke(app, ["home"])
        assert result.exit_code == 0

    def test_home_is_alias_for_frontpage(self, runner: CliRunner, mock_reddit_base):
        """home should produce similar output to frontpage."""
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=TestFrontpage._sample_response())
        )
        result = runner.invoke(app, ["home"])
        assert "Test Post" in result.output


class TestBest:
    """Test suite for best command."""

    def test_best_exit_code(self, runner: CliRunner, mock_reddit_base):
        """best should exit with code 0."""
        mock_reddit_base.get("/r/reddit/top.json").mock(
            return_value=httpx.Response(200, json=TestFrontpage._sample_response())
        )
        result = runner.invoke(app, ["best"])
        assert result.exit_code == 0

    def test_best_output_contains_post(self, runner: CliRunner, mock_reddit_base):
        """best output should contain post title."""
        mock_reddit_base.get("/r/reddit/top.json").mock(
            return_value=httpx.Response(200, json=TestFrontpage._sample_response())
        )
        result = runner.invoke(app, ["best"])
        assert "Test Post" in result.output

    def test_best_with_period(self, runner: CliRunner, mock_reddit_base):
        """best should accept --period option."""
        mock_reddit_base.get("/r/reddit/top.json").mock(
            return_value=httpx.Response(200, json=TestFrontpage._sample_response())
        )
        result = runner.invoke(app, ["best", "--period", "month"])
        assert result.exit_code == 0
