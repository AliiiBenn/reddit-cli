"""Tests for global search command."""
import os
import tempfile
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
        assert "How to learn Python in 2024" in result.output
        assert "Best Python frameworks comparison" in result.output

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
    # ===== Format option tests =====

    def test_search_format_sql(
        self, runner: CliRunner, mock_reddit_base, sample_search_response
    ):
        """search should output SQL format when --format sql is specified."""
        mock_reddit_base.get("/search.json").mock(
            return_value=httpx.Response(200, json=sample_search_response)
        )
        result = runner.invoke(app, ["search", "python", "--format", "sql"])
        assert result.exit_code == 0
        assert "INSERT INTO posts" in result.output
        assert "search1" in result.output
        assert "search2" in result.output

    def test_search_format_csv(
        self, runner: CliRunner, mock_reddit_base, sample_search_response
    ):
        """search should output CSV format when --format csv is specified."""
        mock_reddit_base.get("/search.json").mock(
            return_value=httpx.Response(200, json=sample_search_response)
        )
        result = runner.invoke(app, ["search", "python", "--format", "csv"])
        assert result.exit_code == 0
        assert "id,title,author,subreddit,score,num_comments,url,permalink,created_utc,selftext" in result.output
        assert "search1" in result.output
        assert "search2" in result.output

    def test_search_format_display(
        self, runner: CliRunner, mock_reddit_base, sample_search_response
    ):
        """search should output display format when --format display is specified."""
        mock_reddit_base.get("/search.json").mock(
            return_value=httpx.Response(200, json=sample_search_response)
        )
        result = runner.invoke(app, ["search", "python", "--format", "display"])
        assert result.exit_code == 0
        assert "500" in result.output
        assert "How to learn Python in 2024" in result.output

    def test_search_format_xlsx_with_output(
        self, runner: CliRunner, mock_reddit_base, sample_search_response
    ):
        """search should write xlsx file when --format xlsx and --output are specified."""
        mock_reddit_base.get("/search.json").mock(
            return_value=httpx.Response(200, json=sample_search_response)
        )
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            output_path = f.name
        try:
            result = runner.invoke(app, ["search", "python", "--format", "xlsx", "--output", output_path])
            assert result.exit_code == 0
            assert os.path.exists(output_path)
            assert os.path.getsize(output_path) > 0
            assert "Exported 2 posts" in result.output
        finally:
            os.unlink(output_path)

    def test_search_format_xlsx_without_output(
        self, runner: CliRunner, mock_reddit_base, sample_search_response
    ):
        """search should fail when --format xlsx is specified without --output."""
        mock_reddit_base.get("/search.json").mock(
            return_value=httpx.Response(200, json=sample_search_response)
        )
        result = runner.invoke(app, ["search", "python", "--format", "xlsx"])
        assert result.exit_code == 2
        assert "--output is required for xlsx format" in result.output

    def test_search_format_sql_with_output(
        self, runner: CliRunner, mock_reddit_base, sample_search_response
    ):
        """search should write SQL to file when --format sql and --output are specified."""
        mock_reddit_base.get("/search.json").mock(
            return_value=httpx.Response(200, json=sample_search_response)
        )
        with tempfile.NamedTemporaryFile(suffix=".sql", delete=False) as f:
            output_path = f.name
        try:
            result = runner.invoke(app, ["search", "python", "--format", "sql", "--output", output_path])
            assert result.exit_code == 0
            assert os.path.exists(output_path)
            with open(output_path, "r") as f:
                content = f.read()
            assert "INSERT INTO posts" in content
            assert "Exported 2 posts" in result.output
        finally:
            os.unlink(output_path)

    def test_search_format_csv_with_output(
        self, runner: CliRunner, mock_reddit_base, sample_search_response
    ):
        """search should write CSV to file when --format csv and --output are specified."""
        mock_reddit_base.get("/search.json").mock(
            return_value=httpx.Response(200, json=sample_search_response)
        )
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
            output_path = f.name
        try:
            result = runner.invoke(app, ["search", "python", "--format", "csv", "--output", output_path])
            assert result.exit_code == 0
            assert os.path.exists(output_path)
            with open(output_path, "r") as f:
                content = f.read()
            assert "id,title,author,subreddit,score,num_comments,url,permalink,created_utc,selftext" in content
            assert "Exported 2 posts" in result.output
        finally:
            os.unlink(output_path)

    def test_search_invalid_format(self, runner: CliRunner, mock_reddit_base):
        """search should fail with invalid format value."""
        result = runner.invoke(app, ["search", "python", "--format", "invalid_format"])
        assert result.exit_code == 2
        assert "Invalid value 'invalid_format' for --format" in result.output
    # ===== Limit validation tests =====

    def test_search_limit_zero(self, runner: CliRunner, mock_reddit_base):
        """search should fail when --limit is 0."""
        result = runner.invoke(app, ["search", "python", "--limit", "0"])
        assert result.exit_code == 2
        assert "--limit must be between 1 and 100" in result.output

    def test_search_limit_negative(self, runner: CliRunner, mock_reddit_base):
        """search should fail when --limit is negative."""
        result = runner.invoke(app, ["search", "python", "--limit", "-5"])
        assert result.exit_code == 2
        assert "--limit must be between 1 and 100" in result.output

    def test_search_limit_above_100(self, runner: CliRunner, mock_reddit_base):
        """search should fail when --limit is above 100."""
        result = runner.invoke(app, ["search", "python", "--limit", "101"])
        assert result.exit_code == 2
        assert "--limit must be between 1 and 100" in result.output

    # ===== Sort validation tests =====

    def test_search_invalid_sort(self, runner: CliRunner, mock_reddit_base):
        """search should fail with invalid sort value."""
        result = runner.invoke(app, ["search", "python", "--sort", "invalid_sort"])
        assert result.exit_code == 2
        assert "Invalid value 'invalid_sort' for --sort" in result.output

    # ===== Period validation tests =====

    def test_search_invalid_period(self, runner: CliRunner, mock_reddit_base):
        """search should fail with invalid period value."""
        result = runner.invoke(app, ["search", "python", "--period", "invalid_period"])
        assert result.exit_code == 2
        assert "Invalid value 'invalid_period' for --period" in result.output

    # ===== Cursor display tests =====

    def test_search_with_after_cursor(
        self, runner: CliRunner, mock_reddit_base, sample_search_response
    ):
        """search should display after cursor when present."""
        sample_search_response["data"]["after"] = "t3_after123"
        sample_search_response["data"]["before"] = None
        mock_reddit_base.get("/search.json").mock(
            return_value=httpx.Response(200, json=sample_search_response)
        )
        result = runner.invoke(app, ["search", "python"])
        assert result.exit_code == 0
        assert "After: t3_after123" in result.output

    def test_search_with_before_cursor(
        self, runner: CliRunner, mock_reddit_base, sample_search_response
    ):
        """search should display before cursor when present."""
        sample_search_response["data"]["after"] = None
        sample_search_response["data"]["before"] = "t3_before456"
        mock_reddit_base.get("/search.json").mock(
            return_value=httpx.Response(200, json=sample_search_response)
        )
        result = runner.invoke(app, ["search", "python"])
        assert result.exit_code == 0
        assert "Before: t3_before456" in result.output

    def test_search_with_both_cursors(
        self, runner: CliRunner, mock_reddit_base, sample_search_response
    ):
        """search should display both after and before cursors when both present."""
        sample_search_response["data"]["after"] = "t3_after123"
        sample_search_response["data"]["before"] = "t3_before456"
        mock_reddit_base.get("/search.json").mock(
            return_value=httpx.Response(200, json=sample_search_response)
        )
        result = runner.invoke(app, ["search", "python"])
        assert result.exit_code == 0
        assert "After: t3_after123" in result.output
        assert "Before: t3_before456" in result.output
    # ===== Error handling tests =====

    def test_search_api_error_404(self, runner: CliRunner, mock_reddit_base, error_response_404):
        """search should handle 404 API errors gracefully."""
        mock_reddit_base.get("/search.json").mock(
            return_value=error_response_404
        )
        result = runner.invoke(app, ["search", "python"])
        assert result.exit_code == 1
        assert "Resource not found" in result.output

    def test_search_api_error_429(self, runner: CliRunner, mock_reddit_base, error_response_429):
        """search should handle 429 rate limit errors gracefully."""
        mock_reddit_base.get("/search.json").mock(
            return_value=error_response_429
        )
        result = runner.invoke(app, ["search", "python"])
        assert result.exit_code == 1
        assert "Rate limited" in result.output

    def test_search_api_error_500(self, runner: CliRunner, mock_reddit_base, error_response_500):
        """search should handle 500 server errors gracefully."""
        mock_reddit_base.get("/search.json").mock(
            return_value=error_response_500
        )
        result = runner.invoke(app, ["search", "python"])
        assert result.exit_code == 1
        assert "server error" in result.output

    def test_search_api_error_403(self, runner: CliRunner, mock_reddit_base, error_response_403):
        """search should handle 403 authentication errors gracefully."""
        mock_reddit_base.get("/search.json").mock(
            return_value=error_response_403
        )
        result = runner.invoke(app, ["search", "python"])
        assert result.exit_code == 1
        assert "Authentication required" in result.output

    # ===== Combined parameter tests =====

    def test_search_all_params_combined(
        self, runner: CliRunner, mock_reddit_base, sample_search_response
    ):
        """search should accept all parameters combined."""
        mock_reddit_base.get("/search.json").mock(
            return_value=httpx.Response(200, json=sample_search_response)
        )
        result = runner.invoke(app, [
            "search", "python",
            "--sort", "top",
            "--limit", "10",
            "--period", "week",
            "--format", "display"
        ])
        assert result.exit_code == 0

    def test_search_format_csv_combined_with_period(
        self, runner: CliRunner, mock_reddit_base, sample_search_response
    ):
        """search should work with csv format and period option."""
        mock_reddit_base.get("/search.json").mock(
            return_value=httpx.Response(200, json=sample_search_response)
        )
        result = runner.invoke(app, [
            "search", "python",
            "--format", "csv",
            "--period", "month"
        ])
        assert result.exit_code == 0
        assert "id,title,author,subreddit" in result.output