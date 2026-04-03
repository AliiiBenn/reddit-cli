"""Tests for post commands: post, --view, --info, --duplicates."""
import os
import tempfile
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




@pytest.fixture
def sample_post_empty_selftext() -> dict:
    """Sample post response with empty selftext (link post)."""
    return {
        "data": {
            "children": [
                {
                    "kind": "t3",
                    "data": {
                        "id": "xyz789",
                        "title": "Link Post Title",
                        "score": 42,
                        "num_comments": 10,
                        "author": "linkuser",
                        "subreddit": "links",
                        "url": "https://example.com/article",
                        "permalink": "/r/links/comments/xyz789/link_post/",
                        "selftext": "",
                        "created_utc": 1704067200,
                    },
                }
            ]
        }
    }


class TestPost:
    """Test suite for post command."""

    def test_post_invalid_format(self, runner: CliRunner, mock_reddit_base):
        """post with invalid format should exit with code 2."""
        result = runner.invoke(app, ["post", "abc123", "--format", "invalid"])
        assert result.exit_code == 2
        assert "Invalid value 'invalid' for --format" in result.output

    def test_post_display_format_shows_all_fields(
        self, runner: CliRunner, mock_reddit_base, sample_post_response
    ):
        """post display format should show all post fields."""
        mock_reddit_base.get("/by_id/t3_abc123.json").mock(
            return_value=httpx.Response(200, json=sample_post_response)
        )
        result = runner.invoke(app, ["post", "abc123", "--format", "display"])
        assert result.exit_code == 0
        assert "Amazing New Feature Released" in result.output
        assert "1337" in result.output  # score
        assert "256" in result.output  # num_comments
        assert "developer" in result.output
        assert "r/programming" in result.output
        assert "https://github.com/example/repo" in result.output

    def test_post_display_format_empty_selftext(
        self, runner: CliRunner, mock_reddit_base, sample_post_empty_selftext
    ):
        """post display format with empty selftext should not print empty content."""
        mock_reddit_base.get("/by_id/t3_xyz789.json").mock(
            return_value=httpx.Response(200, json=sample_post_empty_selftext)
        )
        result = runner.invoke(app, ["post", "xyz789", "--format", "display"])
        assert result.exit_code == 0
        # Should still show post info but not print empty selftext
        assert "Link Post Title" in result.output

    def test_post_sql_format_to_stdout(
        self, runner: CliRunner, mock_reddit_base, sample_post_response
    ):
        """post sql format should output SQL INSERT to stdout."""
        mock_reddit_base.get("/by_id/t3_abc123.json").mock(
            return_value=httpx.Response(200, json=sample_post_response)
        )
        result = runner.invoke(app, ["post", "abc123", "--format", "sql"])
        assert result.exit_code == 0
        assert "INSERT INTO posts" in result.output
        assert "abc123" in result.output
        assert "Amazing New Feature Released" in result.output

    def test_post_sql_format_to_file(
        self, runner: CliRunner, mock_reddit_base, sample_post_response
    ):
        """post sql format with --output should write to file."""
        mock_reddit_base.get("/by_id/t3_abc123.json").mock(
            return_value=httpx.Response(200, json=sample_post_response)
        )
        with tempfile.NamedTemporaryFile(mode="w", suffix=".sql", delete=False) as f:
            temp_path = f.name
        try:
            result = runner.invoke(app, ["post", "abc123", "--format", "sql", "--output", temp_path])
            assert result.exit_code == 0
            assert f"Exported 1 post to {temp_path}" in result.output
            with open(temp_path, "r") as f:
                file_content = f.read()
            assert "INSERT INTO posts" in file_content
            assert "abc123" in file_content
        finally:
            os.unlink(temp_path)

    def test_post_csv_format_to_stdout(
        self, runner: CliRunner, mock_reddit_base, sample_post_response
    ):
        """post csv format should output CSV to stdout."""
        mock_reddit_base.get("/by_id/t3_abc123.json").mock(
            return_value=httpx.Response(200, json=sample_post_response)
        )
        result = runner.invoke(app, ["post", "abc123", "--format", "csv"])
        assert result.exit_code == 0
        # Should have header and one row
        lines = result.output.strip().split("\n")
        assert len(lines) == 2
        assert "id,title,author" in lines[0]
        assert "abc123" in lines[1]

    def test_post_csv_format_to_file(
        self, runner: CliRunner, mock_reddit_base, sample_post_response
    ):
        """post csv format with --output should write to file."""
        mock_reddit_base.get("/by_id/t3_abc123.json").mock(
            return_value=httpx.Response(200, json=sample_post_response)
        )
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            temp_path = f.name
        try:
            result = runner.invoke(app, ["post", "abc123", "--format", "csv", "--output", temp_path])
            assert result.exit_code == 0
            assert f"Exported 1 post to {temp_path}" in result.output
            with open(temp_path, "r") as f:
                file_content = f.read()
            assert "id,title,author" in file_content
            assert "abc123" in file_content
        finally:
            os.unlink(temp_path)

    def test_post_xlsx_format_with_output(
        self, runner: CliRunner, mock_reddit_base, sample_post_response
    ):
        """post xlsx format with --output should write xlsx file."""
        mock_reddit_base.get("/by_id/t3_abc123.json").mock(
            return_value=httpx.Response(200, json=sample_post_response)
        )
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            temp_path = f.name
        try:
            result = runner.invoke(app, ["post", "abc123", "--format", "xlsx", "--output", temp_path])
            assert result.exit_code == 0
            assert f"Exported 1 post to {temp_path}" in result.output
            # Verify file was created and has content
            assert os.path.getsize(temp_path) > 0
        finally:
            os.unlink(temp_path)

    def test_post_xlsx_format_without_output(
        self, runner: CliRunner, mock_reddit_base, sample_post_response
    ):
        """post xlsx format without --output should exit with code 2."""
        mock_reddit_base.get("/by_id/t3_abc123.json").mock(
            return_value=httpx.Response(200, json=sample_post_response)
        )
        result = runner.invoke(app, ["post", "abc123", "--format", "xlsx"])
        assert result.exit_code == 2
        assert "--output is required for xlsx format" in result.output

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




class TestPostErrors:
    """Test suite for post command error handling."""

    def test_post_api_error_404(
        self, runner: CliRunner, mock_reddit_base, error_response_404
    ):
        """post with 404 API error should exit with code 1."""
        mock_reddit_base.get("/by_id/t3_notfound.json").mock(
            return_value=error_response_404
        )
        result = runner.invoke(app, ["post", "notfound"])
        assert result.exit_code == 1
        assert "Resource not found" in result.output

    def test_post_api_error_403(
        self, runner: CliRunner, mock_reddit_base, error_response_403
    ):
        """post with 403 API error should exit with code 1."""
        mock_reddit_base.get("/by_id/t3_forbidden.json").mock(
            return_value=error_response_403
        )
        result = runner.invoke(app, ["post", "forbidden"])
        assert result.exit_code == 1
        assert "Authentication required" in result.output

    def test_post_api_error_429(
        self, runner: CliRunner, mock_reddit_base, error_response_429
    ):
        """post with 429 API error should exit with code 1."""
        mock_reddit_base.get("/by_id/t3_ratelimit.json").mock(
            return_value=error_response_429
        )
        result = runner.invoke(app, ["post", "ratelimit"])
        assert result.exit_code == 1
        assert "Rate limited" in result.output

    def test_post_api_error_500(
        self, runner: CliRunner, mock_reddit_base, error_response_500
    ):
        """post with 500 API error should exit with code 1."""
        mock_reddit_base.get("/by_id/t3_servererror.json").mock(
            return_value=error_response_500
        )
        result = runner.invoke(app, ["post", "servererror"])
        assert result.exit_code == 1
        assert "Reddit server error" in result.output

    def test_post_api_error_timeout(self, runner: CliRunner, mock_reddit_base):
        """post with timeout error should exit with code 1."""
        mock_reddit_base.get("/by_id/t3_timeout.json").mock(
            side_effect=httpx.TimeoutException("Connection timed out")
        )
        result = runner.invoke(app, ["post", "timeout"])
        assert result.exit_code == 1
        assert "Connection timed out" in result.output

    def test_post_api_error_connect(self, runner: CliRunner, mock_reddit_base):
        """post with connection error should exit with code 1."""
        mock_reddit_base.get("/by_id/t3_connect.json").mock(
            side_effect=httpx.ConnectError("Could not connect")
        )
        result = runner.invoke(app, ["post", "connect"])
        assert result.exit_code == 1
        assert "Could not connect to Reddit" in result.output
