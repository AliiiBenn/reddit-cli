"""Tests for subreddit commands."""
import os
import tempfile
import pytest
import httpx
from typer.testing import CliRunner
from reddit_cli import app

@pytest.fixture
def sample_subreddit_response() -> dict:
    return {
        "data": {
            "id": "2qh13", "name": "t5_python", "display_name": "python",
            "title": "Python Programming", "description": "Python programming discussion",
            "subscribers": 1500000, "accounts_active": 25000, "over_18": False,
        }
    }

@pytest.fixture
def sample_subreddits_list_response() -> dict:
    return {
        "data": {
            "children": [
                {"kind": "t5", "data": {"id": "2qh13", "name": "t5_python", "display_name": "python",
                 "title": "Python Programming", "description": "Python programming discussion",
                 "subscribers": 1500000, "accounts_active": 25000}},
                {"kind": "t5", "data": {"id": "2qh16", "name": "t5_programming", "display_name": "programming",
                 "title": "Programming", "description": "Programming discussions",
                 "subscribers": 1000000, "accounts_active": 15000}},
            ]
        }
    }

@pytest.fixture
def sample_rules_response() -> dict:
    return {"rules": [
        {"short_name": "Be respectful", "description": "Treat others with respect"},
        {"short_name": "No spam", "description": "Don't spam"},
    ]}

class TestSubreddit:
    def test_subreddit_exit_code(self, runner, mock_reddit_base, sample_subreddit_response):
        mock_reddit_base.get("/r/python/about.json").mock(httpx.Response(200, json=sample_subreddit_response))
        result = runner.invoke(app, ["subreddit", "python"])
        assert result.exit_code == 0

    def test_subreddit_output_contains_title(self, runner, mock_reddit_base, sample_subreddit_response):
        mock_reddit_base.get("/r/python/about.json").mock(httpx.Response(200, json=sample_subreddit_response))
        result = runner.invoke(app, ["subreddit", "python"])
        assert "Python Programming" in result.output

    def test_subreddit_output_contains_name(self, runner, mock_reddit_base, sample_subreddit_response):
        mock_reddit_base.get("/r/python/about.json").mock(httpx.Response(200, json=sample_subreddit_response))
        result = runner.invoke(app, ["subreddit", "python"])
        assert "r/python" in result.output

    def test_subreddit_with_rules_flag(self, runner, mock_reddit_base, sample_subreddit_response, sample_rules_response):
        mock_reddit_base.get("/r/python/about.json").mock(httpx.Response(200, json=sample_subreddit_response))
        mock_reddit_base.get("/r/python/about/rules.json").mock(httpx.Response(200, json=sample_rules_response))
        result = runner.invoke(app, ["subreddits", "rules", "python"])
        assert result.exit_code == 0
        assert "Be respectful" in result.output

    def test_subreddit_missing_name(self, runner):
        result = runner.invoke(app, ["subreddit"])
        assert result.exit_code != 0

    def test_subreddit_with_r_prefix(self, runner, mock_reddit_base, sample_subreddit_response):
        mock_reddit_base.get("/r/python/about.json").mock(httpx.Response(200, json=sample_subreddit_response))
        result = runner.invoke(app, ["subreddit", "r/python"])
        assert result.exit_code == 0

    def test_subreddit_invalid_format(self, runner, mock_reddit_base, sample_subreddit_response):
        mock_reddit_base.get("/r/python/about.json").mock(httpx.Response(200, json=sample_subreddit_response))
        result = runner.invoke(app, ["subreddit", "python", "--format", "invalid"])
        assert result.exit_code != 0

    def test_subreddit_format_sql(self, runner, mock_reddit_base, sample_subreddit_response):
        mock_reddit_base.get("/r/python/about.json").mock(httpx.Response(200, json=sample_subreddit_response))
        result = runner.invoke(app, ["subreddit", "python", "--format", "sql"])
        assert result.exit_code == 0
        assert "INSERT INTO subreddits" in result.output

    def test_subreddit_format_csv(self, runner, mock_reddit_base, sample_subreddit_response):
        mock_reddit_base.get("/r/python/about.json").mock(httpx.Response(200, json=sample_subreddit_response))
        result = runner.invoke(app, ["subreddit", "python", "--format", "csv"])
        assert result.exit_code == 0
        assert "display_name,title,description" in result.output

    def test_subreddit_format_xlsx_requires_output(self, runner, mock_reddit_base, sample_subreddit_response):
        mock_reddit_base.get("/r/python/about.json").mock(httpx.Response(200, json=sample_subreddit_response))
        result = runner.invoke(app, ["subreddit", "python", "--format", "xlsx"])
        assert result.exit_code == 2
        assert "output is required" in result.output.lower()

    def test_subreddit_format_xlsx_with_output(self, runner, mock_reddit_base, sample_subreddit_response):
        mock_reddit_base.get("/r/python/about.json").mock(httpx.Response(200, json=sample_subreddit_response))
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            output_path = f.name
        try:
            result = runner.invoke(app, ["subreddit", "python", "--format", "xlsx", "--output", output_path])
            assert result.exit_code == 0
            assert os.path.exists(output_path)
            assert "Exported" in result.output
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_subreddit_api_error(self, runner, mock_reddit_base):
        mock_reddit_base.get("/r/python/about.json").mock(httpx.Response(404, json={"error": "Not found"}))
        result = runner.invoke(app, ["subreddit", "python"])
        assert result.exit_code != 0


class TestSubreddits:
    def test_subreddits_exit_code(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits.json", params={"limit": 25, "sort": "subscribers"}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "popular"])
        assert result.exit_code == 0

    def test_subreddits_output_contains_names(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits.json", params={"limit": 25, "sort": "subscribers"}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "popular"])
        assert "r/python" in result.output
        assert "r/programming" in result.output

    def test_subreddits_with_limit(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits.json", params={"limit": 5, "sort": "subscribers"}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "popular", "--limit", "5"])
        assert result.exit_code == 0

    def test_subreddits_with_sort(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits.json", params={"limit": 25, "sort": "gilded"}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "popular", "--sort", "gilded"])
        assert result.exit_code == 0

    def test_subreddits_empty_results(self, runner, mock_reddit_base, empty_posts_response):
        mock_reddit_base.get(url="/subreddits.json", params={"limit": 25, "sort": "subscribers"}).mock(
            httpx.Response(200, json=empty_posts_response))
        result = runner.invoke(app, ["subreddits", "popular"])
        assert result.exit_code == 0

    def test_subreddits_invalid_sort(self, runner):
        result = runner.invoke(app, ["subreddits", "popular", "--sort", "invalid_sort"])
        assert result.exit_code != 0

    def test_subreddits_invalid_limit_zero(self, runner):
        result = runner.invoke(app, ["subreddits", "popular", "--limit", "0"])
        assert result.exit_code == 2

    def test_subreddits_invalid_limit_too_high(self, runner):
        result = runner.invoke(app, ["subreddits", "popular", "--limit", "101"])
        assert result.exit_code == 2

    def test_subreddits_invalid_format(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits.json", params={"limit": 25, "sort": "subscribers"}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "popular", "--format", "invalid"])
        assert result.exit_code != 0

    def test_subreddits_popular_format_sql(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits.json", params={"limit": 25, "sort": "subscribers"}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "popular", "--format", "sql"])
        assert result.exit_code == 0
        assert "INSERT INTO subreddits" in result.output

    def test_subreddits_popular_format_csv(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits.json", params={"limit": 25, "sort": "subscribers"}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "popular", "--format", "csv"])
        assert result.exit_code == 0
        assert "display_name,title,description" in result.output

    def test_subreddits_popular_format_xlsx_with_output(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits.json", params={"limit": 25, "sort": "subscribers"}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            output_path = f.name
        try:
            result = runner.invoke(app, ["subreddits", "popular", "--format", "xlsx", "--output", output_path])
            assert result.exit_code == 0
            assert os.path.exists(output_path)
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_subreddits_popular_api_error(self, runner, mock_reddit_base):
        mock_reddit_base.get(url="/subreddits.json", params={"limit": 25, "sort": "subscribers"}).mock(
            httpx.Response(500, json={"error": "Internal Server Error"}))
        result = runner.invoke(app, ["subreddits", "popular"])
        assert result.exit_code != 0


class TestSubredditsSearch:
    def test_search_exit_code(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits/search.json", params={"q": "python", "limit": 25}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "search", "python"])
        assert result.exit_code == 0

    def test_search_output_contains_query(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits/search.json", params={"q": "programming", "limit": 25}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "search", "programming"])
        assert "programming" in result.output.lower()

    def test_search_missing_query(self, runner):
        result = runner.invoke(app, ["subreddits", "search"])
        assert result.exit_code != 0

    def test_search_no_results(self, runner, mock_reddit_base, empty_posts_response):
        mock_reddit_base.get(url="/subreddits/search.json", params={"q": "nonexistent123xyz", "limit": 25}).mock(
            httpx.Response(200, json=empty_posts_response))
        result = runner.invoke(app, ["subreddits", "search", "nonexistent123xyz"])
        assert result.exit_code == 0
        assert "No subreddits found" in result.output

    def test_search_invalid_format(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits/search.json", params={"q": "python", "limit": 25}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "search", "python", "--format", "invalid"])
        assert result.exit_code != 0

    def test_search_format_sql(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits/search.json", params={"q": "python", "limit": 25}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "search", "python", "--format", "sql"])
        assert result.exit_code == 0
        assert "INSERT INTO subreddits" in result.output

    def test_search_format_csv(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits/search.json", params={"q": "python", "limit": 25}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "search", "python", "--format", "csv"])
        assert result.exit_code == 0
        assert "display_name,title,description" in result.output

    def test_search_format_xlsx_with_output(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits/search.json", params={"q": "python", "limit": 25}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            output_path = f.name
        try:
            result = runner.invoke(app, ["subreddits", "search", "python", "--format", "xlsx", "--output", output_path])
            assert result.exit_code == 0
            assert os.path.exists(output_path)
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_search_api_error(self, runner, mock_reddit_base):
        mock_reddit_base.get(url="/subreddits/search.json", params={"q": "python", "limit": 25}).mock(
            httpx.Response(500, json={"error": "Internal Server Error"}))
        result = runner.invoke(app, ["subreddits", "search", "python"])
        assert result.exit_code != 0


class TestSubredditsNew:
    def test_new_exit_code(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits/new.json", params={"limit": 25}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "new"])
        assert result.exit_code == 0

    def test_new_with_limit(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits/new.json", params={"limit": 10}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "new", "--limit", "10"])
        assert result.exit_code == 0

    def test_new_invalid_format(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits/new.json", params={"limit": 25}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "new", "--format", "invalid"])
        assert result.exit_code != 0

    def test_new_format_sql(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits/new.json", params={"limit": 25}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "new", "--format", "sql"])
        assert result.exit_code == 0
        assert "INSERT INTO subreddits" in result.output

    def test_new_format_csv(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits/new.json", params={"limit": 25}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "new", "--format", "csv"])
        assert result.exit_code == 0
        assert "display_name,title,description" in result.output

    def test_new_format_xlsx_with_output(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits/new.json", params={"limit": 25}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            output_path = f.name
        try:
            result = runner.invoke(app, ["subreddits", "new", "--format", "xlsx", "--output", output_path])
            assert result.exit_code == 0
            assert os.path.exists(output_path)
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_new_api_error(self, runner, mock_reddit_base):
        mock_reddit_base.get(url="/subreddits/new.json", params={"limit": 25}).mock(
            httpx.Response(500, json={"error": "Internal Server Error"}))
        result = runner.invoke(app, ["subreddits", "new"])
        assert result.exit_code != 0


class TestSubredditsGold:
    def test_gold_exit_code(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits/gold.json", params={"limit": 25}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "gold"])
        assert result.exit_code == 0

    def test_gold_output_contains_subreddits(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits/gold.json", params={"limit": 25}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "gold"])
        assert "python" in result.output

    def test_gold_invalid_format(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits/gold.json", params={"limit": 25}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "gold", "--format", "invalid"])
        assert result.exit_code != 0

    def test_gold_format_sql(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits/gold.json", params={"limit": 25}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "gold", "--format", "sql"])
        assert result.exit_code == 0
        assert "INSERT INTO subreddits" in result.output

    def test_gold_format_csv(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits/gold.json", params={"limit": 25}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "gold", "--format", "csv"])
        assert result.exit_code == 0
        assert "display_name,title,description" in result.output

    def test_gold_format_xlsx_with_output(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits/gold.json", params={"limit": 25}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            output_path = f.name
        try:
            result = runner.invoke(app, ["subreddits", "gold", "--format", "xlsx", "--output", output_path])
            assert result.exit_code == 0
            assert os.path.exists(output_path)
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_gold_api_error(self, runner, mock_reddit_base):
        mock_reddit_base.get(url="/subreddits/gold.json", params={"limit": 25}).mock(
            httpx.Response(500, json={"error": "Internal Server Error"}))
        result = runner.invoke(app, ["subreddits", "gold"])
        assert result.exit_code != 0


class TestSubredditsDefault:
    def test_default_exit_code(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits/default.json", params={"limit": 25}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "default"])
        assert result.exit_code == 0

    def test_default_output_contains_subreddits(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits/default.json", params={"limit": 25}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "default"])
        assert "python" in result.output

    def test_default_invalid_format(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits/default.json", params={"limit": 25}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "default", "--format", "invalid"])
        assert result.exit_code != 0

    def test_default_format_sql(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits/default.json", params={"limit": 25}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "default", "--format", "sql"])
        assert result.exit_code == 0
        assert "INSERT INTO subreddits" in result.output

    def test_default_format_csv(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits/default.json", params={"limit": 25}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        result = runner.invoke(app, ["subreddits", "default", "--format", "csv"])
        assert result.exit_code == 0
        assert "display_name,title,description" in result.output

    def test_default_format_xlsx_with_output(self, runner, mock_reddit_base, sample_subreddits_list_response):
        mock_reddit_base.get(url="/subreddits/default.json", params={"limit": 25}).mock(
            httpx.Response(200, json=sample_subreddits_list_response))
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            output_path = f.name
        try:
            result = runner.invoke(app, ["subreddits", "default", "--format", "xlsx", "--output", output_path])
            assert result.exit_code == 0
            assert os.path.exists(output_path)
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_default_api_error(self, runner, mock_reddit_base):
        mock_reddit_base.get(url="/subreddits/default.json", params={"limit": 25}).mock(
            httpx.Response(500, json={"error": "Internal Server Error"}))
        result = runner.invoke(app, ["subreddits", "default"])
        assert result.exit_code != 0


class TestSubredditsRules:
    def test_rules_exit_code(self, runner, mock_reddit_base, sample_rules_response):
        mock_reddit_base.get("/r/python/about/rules.json").mock(
            httpx.Response(200, json=sample_rules_response))
        result = runner.invoke(app, ["subreddits", "rules", "python"])
        assert result.exit_code == 0

    def test_rules_output_contains_rule_names(self, runner, mock_reddit_base, sample_rules_response):
        mock_reddit_base.get("/r/python/about/rules.json").mock(
            httpx.Response(200, json=sample_rules_response))
        result = runner.invoke(app, ["subreddits", "rules", "python"])
        assert "Be respectful" in result.output
        assert "No spam" in result.output

    def test_rules_api_error(self, runner, mock_reddit_base):
        mock_reddit_base.get("/r/python/about/rules.json").mock(
            httpx.Response(500, json={"error": "Internal Server Error"}))
        result = runner.invoke(app, ["subreddits", "rules", "python"])
        assert result.exit_code != 0
