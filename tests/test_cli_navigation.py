"""Tests for navigation commands: frontpage, home, best."""
import pytest
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


class TestNavigationDisplayFormat:
    """Test display format with cursors."""

    def test_frontpage_display_shows_after_cursor(self, runner, mock_reddit_base, sample_navigation_response):
        sample_navigation_response["data"]["after"] = "t3_after123"
        sample_navigation_response["data"]["before"] = None
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["frontpage"])
        assert result.exit_code == 0
        assert "After: t3_after123" in result.output

    def test_frontpage_display_shows_before_cursor(self, runner, mock_reddit_base, sample_navigation_response):
        sample_navigation_response["data"]["after"] = None
        sample_navigation_response["data"]["before"] = "t3_before456"
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["frontpage"])
        assert result.exit_code == 0
        assert "Before: t3_before456" in result.output

    def test_frontpage_display_shows_both_cursors(self, runner, mock_reddit_base, sample_navigation_response):
        sample_navigation_response["data"]["after"] = "t3_after123"
        sample_navigation_response["data"]["before"] = "t3_before456"
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["frontpage"])
        assert result.exit_code == 0
        assert "After: t3_after123" in result.output
        assert "Before: t3_before456" in result.output


class TestNavigationFormatOptions:
    """Test format options for navigation commands."""

    def test_frontpage_csv_format(self, runner, mock_reddit_base, sample_navigation_response):
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["frontpage", "--format", "csv"])
        assert result.exit_code == 0
        assert "id,title,author,subreddit,score,num_comments,url,permalink,created_utc,selftext" in result.output
        assert "abc123" in result.output

    def test_frontpage_sql_format(self, runner, mock_reddit_base, sample_navigation_response):
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["frontpage", "--format", "sql"])
        assert result.exit_code == 0
        assert "INSERT INTO posts" in result.output
        assert "abc123" in result.output

    def test_home_csv_format(self, runner, mock_reddit_base, sample_navigation_response):
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["home", "--format", "csv"])
        assert result.exit_code == 0
        assert "id,title,author" in result.output

    def test_home_sql_format(self, runner, mock_reddit_base, sample_navigation_response):
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["home", "--format", "sql"])
        assert result.exit_code == 0
        assert "INSERT INTO posts" in result.output

    def test_best_csv_format(self, runner, mock_reddit_base, sample_navigation_response):
        mock_reddit_base.get("/r/reddit/top.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["best", "--format", "csv"])
        assert result.exit_code == 0
        assert "id,title,author" in result.output

    def test_best_sql_format(self, runner, mock_reddit_base, sample_navigation_response):
        mock_reddit_base.get("/r/reddit/top.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["best", "--format", "sql"])
        assert result.exit_code == 0
        assert "INSERT INTO posts" in result.output

class TestNavigationOutputFile:
    """Test output file handling for navigation commands."""

    def test_frontpage_csv_to_file(self, runner, mock_reddit_base, sample_navigation_response, tmp_path):
        output_file = tmp_path / "output.csv"
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["frontpage", "--format", "csv", "--output", str(output_file)])
        assert result.exit_code == 0
        assert output_file.exists()
        content = output_file.read_text(encoding="utf-8")
        assert "abc123" in content

    def test_frontpage_sql_to_file(self, runner, mock_reddit_base, sample_navigation_response, tmp_path):
        output_file = tmp_path / "output.sql"
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["frontpage", "--format", "sql", "--output", str(output_file)])
        assert result.exit_code == 0
        assert output_file.exists()
        content = output_file.read_text(encoding="utf-8")
        assert "INSERT INTO posts" in content

    def test_frontpage_xlsx_requires_output(self, runner, mock_reddit_base, sample_navigation_response):
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["frontpage", "--format", "xlsx"])
        assert result.exit_code == 2
        assert "--output is required for xlsx format" in result.output

    def test_frontpage_xlsx_to_file(self, runner, mock_reddit_base, sample_navigation_response, tmp_path):
        output_file = tmp_path / "output.xlsx"
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["frontpage", "--format", "xlsx", "--output", str(output_file)])
        assert result.exit_code == 0
        assert output_file.exists()
        assert "Exported" in result.output

class TestNavigationValidation:
    """Test validation errors for navigation commands."""

    def test_frontpage_invalid_sort(self, runner, mock_reddit_base, sample_navigation_response):
        result = runner.invoke(app, ["frontpage", "--sort", "invalid_sort"])
        assert result.exit_code == 2
        assert "Invalid value 'invalid_sort'" in result.output
        assert "hot" in result.output

    def test_frontpage_invalid_period(self, runner, mock_reddit_base, sample_navigation_response):
        mock_reddit_base.get("/r/reddit/top.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["frontpage", "--sort", "top", "--period", "invalid_period"])
        assert result.exit_code == 2
        assert "Invalid value 'invalid_period'" in result.output
        assert "day" in result.output

    def test_frontpage_limit_zero(self, runner, mock_reddit_base, sample_navigation_response):
        result = runner.invoke(app, ["frontpage", "--limit", "0"])
        assert result.exit_code == 2
        assert "--limit must be between 1 and 100" in result.output

    def test_frontpage_limit_negative(self, runner, mock_reddit_base, sample_navigation_response):
        result = runner.invoke(app, ["frontpage", "--limit", "-5"])
        assert result.exit_code == 2
        assert "--limit must be between 1 and 100" in result.output

    def test_frontpage_limit_over_100(self, runner, mock_reddit_base, sample_navigation_response):
        result = runner.invoke(app, ["frontpage", "--limit", "101"])
        assert result.exit_code == 2
        assert "--limit must be between 1 and 100" in result.output

    def test_best_invalid_period(self, runner, mock_reddit_base, sample_navigation_response):
        mock_reddit_base.get("/r/reddit/top.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["best", "--period", "invalid"])
        assert result.exit_code == 2
        assert "Invalid value 'invalid'" in result.output

    def test_home_invalid_sort(self, runner, mock_reddit_base, sample_navigation_response):
        result = runner.invoke(app, ["home", "--sort", "bad_sort"])
        assert result.exit_code == 2
        assert "Invalid value 'bad_sort'" in result.output

class TestNavigationAllSortValues:
    """Test all valid sort values for frontpage/home."""

    @pytest.mark.parametrize("sort_value", ["hot", "new", "top", "rising", "controversial", "gilded"])
    def test_frontpage_all_sort_values(self, runner, mock_reddit_base, sample_navigation_response, sort_value):
        mock_reddit_base.get(f"/r/reddit/{sort_value}.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["frontpage", "--sort", sort_value])
        assert result.exit_code == 0


class TestNavigationAllPeriodValues:
    """Test all valid period values."""

    @pytest.mark.parametrize("period_value", ["day", "week", "month", "year", "all"])
    def test_best_all_period_values(self, runner, mock_reddit_base, sample_navigation_response, period_value):
        mock_reddit_base.get("/r/reddit/top.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["best", "--period", period_value])
        assert result.exit_code == 0

class TestNavigationEmptyResults:
    """Test navigation commands with empty results."""

    def test_frontpage_empty_results(self, runner, mock_reddit_base, empty_posts_response):
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=empty_posts_response)
        )
        result = runner.invoke(app, ["frontpage"])
        assert result.exit_code == 0

    def test_frontpage_empty_csv_output(self, runner, mock_reddit_base, empty_posts_response):
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=empty_posts_response)
        )
        result = runner.invoke(app, ["frontpage", "--format", "csv"])
        assert result.exit_code == 0
        assert "id,title,author,subreddit,score,num_comments,url,permalink,created_utc,selftext" in result.output

    def test_frontpage_empty_sql_output(self, runner, mock_reddit_base, empty_posts_response):
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=empty_posts_response)
        )
        result = runner.invoke(app, ["frontpage", "--format", "sql"])
        assert result.exit_code == 0

class TestNavigationErrors:
    """Test error handling for navigation commands."""

    def test_frontpage_404_error(self, runner, mock_reddit_base, error_response_404):
        mock_reddit_base.get("/r/reddit/hot.json").mock(return_value=error_response_404)
        result = runner.invoke(app, ["frontpage"])
        assert result.exit_code == 1
        assert "Not Found" in result.output or "Resource not found" in result.output

    def test_frontpage_500_error(self, runner, mock_reddit_base, error_response_500):
        mock_reddit_base.get("/r/reddit/hot.json").mock(return_value=error_response_500)
        result = runner.invoke(app, ["frontpage"])
        assert result.exit_code == 1
        assert "server error" in result.output.lower() or "Internal Server Error" in result.output

    def test_frontpage_403_error(self, runner, mock_reddit_base, error_response_403):
        mock_reddit_base.get("/r/reddit/hot.json").mock(return_value=error_response_403)
        result = runner.invoke(app, ["frontpage"])
        assert result.exit_code == 1
        assert "Authentication" in result.output or "Forbidden" in result.output

    def test_frontpage_429_error(self, runner, mock_reddit_base, error_response_429):
        mock_reddit_base.get("/r/reddit/hot.json").mock(return_value=error_response_429)
        result = runner.invoke(app, ["frontpage"])
        assert result.exit_code == 1
        assert "Rate limit" in result.output or "Too Many Requests" in result.output

    def test_home_404_error(self, runner, mock_reddit_base, error_response_404):
        mock_reddit_base.get("/r/reddit/hot.json").mock(return_value=error_response_404)
        result = runner.invoke(app, ["home"])
        assert result.exit_code == 1

    def test_best_404_error(self, runner, mock_reddit_base, error_response_404):
        mock_reddit_base.get("/r/reddit/top.json").mock(return_value=error_response_404)
        result = runner.invoke(app, ["best"])
        assert result.exit_code == 1

class TestNavigationInvalidFormat:
    """Test invalid format values."""

    def test_frontpage_invalid_format(self, runner, mock_reddit_base, sample_navigation_response):
        mock_reddit_base.get("/r/reddit/hot.json").mock(
            return_value=httpx.Response(200, json=sample_navigation_response)
        )
        result = runner.invoke(app, ["frontpage", "--format", "invalid_format"])
        assert result.exit_code == 2
        assert "Invalid value 'invalid_format'" in result.output
        assert "display" in result.output
