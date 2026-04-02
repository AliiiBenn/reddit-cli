"""Tests for post commands: post, --view, --info, --duplicates."""
import pytest
import httpx
from typer.testing import CliRunner

from reddit_cli import app


@pytest.fixture
def sample_post_response() -> dict:
    """Sample single post response from /by_id endpoint."""
    return {
        "data": {
            "children": [
                {
                    "kind": "t3",
                    "data": {
                        "id": "abc123",
                        "title": "Amazing New Feature Released",
                        "score": 1337,
                        "num_comments": 256,
                        "author": "developer",
                        "subreddit": "programming",
                        "url": "https://github.com/example/repo",
                        "permalink": "/r/programming/comments/abc123/amazing_new_feature/",
                        "selftext": "Check out this awesome new feature we shipped!",
                        "created_utc": 1704067200,
                    },
                }
            ]
        }
    }


class TestPost:
    """Test suite for post command."""

    def test_post_exit_code(self, runner: CliRunner, mock_reddit_base, sample_post_response):
        """post should exit with code 0."""
        mock_reddit_base.get("/by_id/t3_abc123.json").mock(
            return_value=httpx.Response(200, json=sample_post_response)
        )
        result = runner.invoke(app, ["post", "abc123"])
        assert result.exit_code == 0

    def test_post_output_contains_title(
        self, runner: CliRunner, mock_reddit_base, sample_post_response
    ):
        """post output should contain post title."""
        mock_reddit_base.get("/by_id/t3_abc123.json").mock(
            return_value=httpx.Response(200, json=sample_post_response)
        )
        result = runner.invoke(app, ["post", "abc123"])
        assert "Amazing New Feature Released" in result.output

    def test_post_output_contains_author(
        self, runner: CliRunner, mock_reddit_base, sample_post_response
    ):
        """post output should contain author name."""
        mock_reddit_base.get("/by_id/t3_abc123.json").mock(
            return_value=httpx.Response(200, json=sample_post_response)
        )
        result = runner.invoke(app, ["post", "abc123"])
        assert "developer" in result.output

    def test_post_with_t3_prefix(self, runner: CliRunner, mock_reddit_base, sample_post_response):
        """post should accept post ID with t3_ prefix."""
        mock_reddit_base.get("/by_id/t3_abc123.json").mock(
            return_value=httpx.Response(200, json=sample_post_response)
        )
        result = runner.invoke(app, ["post", "t3_abc123"])
        assert result.exit_code == 0

    def test_post_missing_id(self, runner: CliRunner):
        """post should fail without post ID."""
        result = runner.invoke(app, ["post"])
        assert result.exit_code != 0


class TestPostView:
    """Test suite for post --view command."""

    def test_view_exit_code(self, runner: CliRunner, mock_reddit_base, sample_post_response):
        """post abc123 --view should exit with code 0."""
        mock_reddit_base.get("/by_id/t3_abc123.json").mock(
            return_value=httpx.Response(200, json=sample_post_response)
        )
        result = runner.invoke(app, ["post", "abc123", "--view"])
        assert result.exit_code == 0

    def test_view_output_contains_title(
        self, runner: CliRunner, mock_reddit_base, sample_post_response
    ):
        """post abc123 --view output should contain post title."""
        mock_reddit_base.get("/by_id/t3_abc123.json").mock(
            return_value=httpx.Response(200, json=sample_post_response)
        )
        result = runner.invoke(app, ["post", "abc123", "--view"])
        assert "Amazing New Feature Released" in result.output


class TestPostInfo:
    """Test suite for post --info command."""

    def test_info_exit_code(self, runner: CliRunner, mock_reddit_base, sample_post_response):
        """post abc123 --info should exit with code 0."""
        mock_reddit_base.get("/by_id/t3_abc123.json").mock(
            return_value=httpx.Response(200, json=sample_post_response)
        )
        result = runner.invoke(app, ["post", "abc123", "--info"])
        assert result.exit_code == 0

    def test_info_output_contains_title(
        self, runner: CliRunner, mock_reddit_base, sample_post_response
    ):
        """post abc123 --info output should contain post title."""
        mock_reddit_base.get("/by_id/t3_abc123.json").mock(
            return_value=httpx.Response(200, json=sample_post_response)
        )
        result = runner.invoke(app, ["post", "abc123", "--info"])
        assert "Amazing New Feature Released" in result.output


