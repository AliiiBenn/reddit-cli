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
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "python"])
        assert result.exit_code == 0
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
class TestBrowseValidation:
    """Test suite for browse validation edge cases."""

    def test_browse_invalid_sort_value(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse should reject invalid --sort values."""
        result = runner.invoke(app, ["browse", "python", "--sort", "invalid_sort"])
        assert result.exit_code == 2
        assert "Invalid value" in result.output

    def test_browse_invalid_period_value(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse should reject invalid --period values."""
        mock_reddit_base.get("/r/python/top.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "python", "--sort", "top", "--period", "invalid_period"])
        assert result.exit_code == 2
        assert "Invalid value" in result.output

    def test_browse_limit_zero(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse should reject --limit 0."""
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "python", "--limit", "0"])
        assert result.exit_code == 2
        assert "--limit must be between 1 and 100" in result.output

    def test_browse_limit_negative(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse should reject negative --limit."""
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "python", "--limit", "-1"])
        assert result.exit_code == 2
        assert "--limit must be between 1 and 100" in result.output

    def test_browse_limit_over_100(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse should reject --limit over 100."""
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "python", "--limit", "101"])
        assert result.exit_code == 2
        assert "--limit must be between 1 and 100" in result.output

    def test_browse_limit_100_boundary(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse should accept --limit 100 (boundary)."""
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "python", "--limit", "100"])
        assert result.exit_code == 0

    def test_browse_limit_1_boundary(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse should accept --limit 1 (boundary)."""
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "python", "--limit", "1"])
        assert result.exit_code == 0

    def test_browse_invalid_format_value(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse should reject invalid --format values."""
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "python", "--format", "invalid_format"])
        assert result.exit_code == 2
        assert "Invalid value" in result.output

class TestBrowseFormats:
    """Test suite for browse with different format options."""

    def test_browse_format_display(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse with --format display should work (default)."""
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "python", "--format", "display"])
        assert result.exit_code == 0
        assert "Python Tip of the Day" in result.output

    def test_browse_format_sql(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse with --format sql should output SQL INSERT statements."""
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "python", "--format", "sql"])
        assert result.exit_code == 0
        assert "INSERT INTO posts" in result.output

    def test_browse_format_csv(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse with --format csv should output CSV data."""
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "python", "--format", "csv"])
        assert result.exit_code == 0
        assert "id,title,author,subreddit,score,num_comments,url,permalink,created_utc,selftext" in result.output

    def test_browse_format_xlsx_without_output(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse with --format xlsx without --output should error."""
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "python", "--format", "xlsx"])
        assert result.exit_code == 2
        assert "--output is required for xlsx format" in result.output

    def test_browse_format_xlsx_with_output(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response, tmp_path
    ):
        """browse with --format xlsx and --output should create file."""
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        output_file = tmp_path / "posts.xlsx"
        result = runner.invoke(
            app, ["browse", "python", "--format", "xlsx", "--output", str(output_file)]
        )
        assert result.exit_code == 0
        assert f"Exported 1 posts to {output_file}" in result.output
        assert output_file.exists()

    def test_browse_format_sql_with_output(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response, tmp_path
    ):
        """browse with --format sql and --output should write to file."""
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        output_file = tmp_path / "posts.sql"
        result = runner.invoke(
            app, ["browse", "python", "--format", "sql", "--output", str(output_file)]
        )
        assert result.exit_code == 0
        assert f"Exported 1 posts to {output_file}" in result.output
        assert output_file.exists()

    def test_browse_format_csv_with_output(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response, tmp_path
    ):
        """browse with --format csv and --output should write to file."""
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        output_file = tmp_path / "posts.csv"
        result = runner.invoke(
            app, ["browse", "python", "--format", "csv", "--output", str(output_file)]
        )
        assert result.exit_code == 0
        assert f"Exported 1 posts to {output_file}" in result.output
        assert output_file.exists()
class TestBrowseSearchFormats:
    """Test suite for browse --search with different format options."""

    def test_browse_search_format_display(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse --search with --format display should show search results."""
        mock_reddit_base.get("/r/python/search.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "python", "--search", "django", "--format", "display"])
        assert result.exit_code == 0
        assert "Search results for 'django' in r/python:" in result.output

    def test_browse_search_format_sql(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse --search with --format sql should output SQL INSERT statements."""
        mock_reddit_base.get("/r/python/search.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "python", "--search", "django", "--format", "sql"])
        assert result.exit_code == 0
        assert "INSERT INTO posts" in result.output

    def test_browse_search_format_csv(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse --search with --format csv should output CSV data."""
        mock_reddit_base.get("/r/python/search.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "python", "--search", "django", "--format", "csv"])
        assert result.exit_code == 0
        assert "id,title,author,subreddit,score,num_comments,url,permalink,created_utc,selftext" in result.output

    def test_browse_search_format_xlsx_without_output(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse --search with --format xlsx without --output should error."""
        mock_reddit_base.get("/r/python/search.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "python", "--search", "django", "--format", "xlsx"])
        assert result.exit_code == 2
        assert "--output is required for xlsx format" in result.output

    def test_browse_search_format_xlsx_with_output(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response, tmp_path
    ):
        """browse --search with --format xlsx and --output should create file."""
        mock_reddit_base.get("/r/python/search.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        output_file = tmp_path / "search_results.xlsx"
        result = runner.invoke(
            app, ["browse", "python", "--search", "django", "--format", "xlsx", "--output", str(output_file)]
        )
        assert result.exit_code == 0
        assert f"Exported 1 posts to {output_file}" in result.output
        assert output_file.exists()
class TestBrowseApiErrors:
    """Test suite for browse API error handling."""

    def test_browse_api_404_error(
        self, runner: CliRunner, mock_reddit_base, error_response_404
    ):
        """browse should handle 404 API errors gracefully."""
        mock_reddit_base.get("/r/nonexistent subreddit 123/hot.json").mock(
            return_value=error_response_404
        )
        result = runner.invoke(app, ["browse", "nonexistent subreddit 123"])
        assert result.exit_code == 1
        assert "Error:" in result.output

    def test_browse_api_500_error(
        self, runner: CliRunner, mock_reddit_base, error_response_500
    ):
        """browse should handle 500 API errors gracefully."""
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=error_response_500
        )
        result = runner.invoke(app, ["browse", "python"])
        assert result.exit_code == 1
        assert "Error:" in result.output

    def test_browse_api_429_error(
        self, runner: CliRunner, mock_reddit_base, error_response_429
    ):
        """browse should handle 429 (rate limit) API errors gracefully."""
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=error_response_429
        )
        result = runner.invoke(app, ["browse", "python"])
        assert result.exit_code == 1
        assert "Error:" in result.output

    def test_browse_api_timeout_error(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse should handle timeout errors gracefully."""
        mock_reddit_base.get("/r/python/hot.json").mock(
            side_effect=httpx.TimeoutException("Connection timed out")
        )
        result = runner.invoke(app, ["browse", "python"])
        assert result.exit_code == 1
        assert "Error:" in result.output

    def test_browse_search_api_error(
        self, runner: CliRunner, mock_reddit_base, error_response_404
    ):
        """browse --search should handle API errors gracefully."""
        mock_reddit_base.get("/r/python/search.json").mock(
            return_value=error_response_404
        )
        result = runner.invoke(app, ["browse", "python", "--search", "django"])
        assert result.exit_code == 1
        assert "Error:" in result.output
class TestBrowseGildedSort:
    """Test suite for browse with gilded sort option."""

    def test_browse_gilded_sort(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse should accept --sort gilded."""
        mock_reddit_base.get("/r/python/gilded.json").mock(
            return_value=httpx.Response(200, json=sample_browse_response)
        )
        result = runner.invoke(app, ["browse", "python", "--sort", "gilded"])
        assert result.exit_code == 0

class TestBrowseBeforeOnly:
    """Test suite for browse with only before cursor (no after)."""

    def test_browse_before_cursor_no_after(
        self, runner: CliRunner, mock_reddit_base, sample_browse_response
    ):
        """browse should display Before cursor when only before is present."""
        response_with_before = {
            "data": {
                "children": [
                    {
                        "kind": "t3",
                        "data": {
                            "id": "post1",
                            "title": "Older Post",
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
                "after": None,
                "before": "t3_before1",
            }
        }
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=httpx.Response(200, json=response_with_before)
        )
        result = runner.invoke(app, ["browse", "python"])
        assert result.exit_code == 0
        assert "Before:" in result.output