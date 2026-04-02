"""Tests for subreddit commands: subreddit, subreddits, subreddits --search/--new/--gold/--default."""
import pytest
import httpx
from typer.testing import CliRunner

from reddit_cli import app


@pytest.fixture
def sample_subreddit_response() -> dict:
    """Sample subreddit info response."""
    return {
        "data": {
            "id": "2qh13",
            "name": "t5_python",
            "display_name": "python",
            "title": "Python Programming",
            "description": "Python programming discussion",
            "subscribers": 1500000,
            "accounts_active": 25000,
            "over_18": False,
        }
    }


@pytest.fixture
def sample_subreddits_list_response() -> dict:
    """Sample subreddits list response."""
    return {
        "data": {
            "children": [
                {
                    "kind": "t5",
                    "data": {
                        "id": "2qh13",
                        "name": "t5_python",
                        "display_name": "python",
                        "title": "Python Programming",
                        "description": "Python programming discussion",
                        "subscribers": 1500000,
                        "accounts_active": 25000,
                    },
                },
                {
                    "kind": "t5",
                    "data": {
                        "id": "2qh16",
                        "name": "t5_programming",
                        "display_name": "programming",
                        "title": "Programming",
                        "description": "Programming discussions",
                        "subscribers": 1000000,
                        "accounts_active": 15000,
                    },
                },
            ]
        }
    }


@pytest.fixture
def sample_rules_response() -> dict:
    """Sample subreddit rules response."""
    return {
        "rules": [
            {"short_name": "Be respectful", "description": "Treat others with respect"},
            {"short_name": "No spam", "description": "Don't spam"},
        ]
    }


class TestSubreddit:
    """Test suite for subreddit command."""

    def test_subreddit_exit_code(
        self, runner: CliRunner, mock_reddit_base, sample_subreddit_response
    ):
        """subreddit should exit with code 0."""
        mock_reddit_base.get("/r/python/about.json").mock(
            return_value=httpx.Response(200, json=sample_subreddit_response)
        )
        result = runner.invoke(app, ["subreddit", "python"])
        assert result.exit_code == 0

    def test_subreddit_output_contains_title(
        self, runner: CliRunner, mock_reddit_base, sample_subreddit_response
    ):
        """subreddit output should contain subreddit title."""
        mock_reddit_base.get("/r/python/about.json").mock(
            return_value=httpx.Response(200, json=sample_subreddit_response)
        )
        result = runner.invoke(app, ["subreddit", "python"])
        assert "Python Programming" in result.output

    def test_subreddit_output_contains_name(
        self, runner: CliRunner, mock_reddit_base, sample_subreddit_response
    ):
        """subreddit output should contain subreddit name."""
        mock_reddit_base.get("/r/python/about.json").mock(
            return_value=httpx.Response(200, json=sample_subreddit_response)
        )
        result = runner.invoke(app, ["subreddit", "python"])
        assert "r/python" in result.output

    def test_subreddit_with_rules_flag(
        self, runner: CliRunner, mock_reddit_base, sample_subreddit_response, sample_rules_response
    ):
        """subreddit python --rules should show rules."""
        mock_reddit_base.get("/r/python/about.json").mock(
            return_value=httpx.Response(200, json=sample_subreddit_response)
        )
        mock_reddit_base.get("/r/python/about/rules.json").mock(
            return_value=httpx.Response(200, json=sample_rules_response)
        )
        result = runner.invoke(app, ["subreddit", "python", "--rules"])
        assert result.exit_code == 0
        assert "Be respectful" in result.output

    def test_subreddit_missing_name(self, runner: CliRunner):
        """subreddit should fail without name."""
        result = runner.invoke(app, ["subreddit"])
        assert result.exit_code != 0

    def test_subreddit_with_r_prefix(self, runner: CliRunner, mock_reddit_base, sample_subreddit_response):
        """subreddit should accept name with r/ prefix."""
        mock_reddit_base.get("/r/python/about.json").mock(
            return_value=httpx.Response(200, json=sample_subreddit_response)
        )
        result = runner.invoke(app, ["subreddit", "r/python"])
        assert result.exit_code == 0

class TestSubreddits:
    """Test suite for subreddits command."""

    def test_subreddits_exit_code(
        self, runner: CliRunner, mock_reddit_base, sample_subreddits_list_response
    ):
        """subreddits should exit with code 0."""
        mock_reddit_base.get(url="/subreddits.json", params={"limit": 25, "sort": "subscribers"}).mock(
            return_value=httpx.Response(200, json=sample_subreddits_list_response)
        )
        result = runner.invoke(app, ["subreddits"])
        assert result.exit_code == 0

    def test_subreddits_output_contains_names(
        self, runner: CliRunner, mock_reddit_base, sample_subreddits_list_response
    ):
        """subreddits output should contain subreddit names."""
        mock_reddit_base.get(url="/subreddits.json", params={"limit": 25, "sort": "subscribers"}).mock(
            return_value=httpx.Response(200, json=sample_subreddits_list_response)
        )
        result = runner.invoke(app, ["subreddits"])
        assert "r/python" in result.output
        assert "r/programming" in result.output

    def test_subreddits_with_limit(
        self, runner: CliRunner, mock_reddit_base, sample_subreddits_list_response
    ):
        """subreddits should accept --limit option."""
        mock_reddit_base.get(url="/subreddits.json", params={"limit": 5, "sort": "subscribers"}).mock(
            return_value=httpx.Response(200, json=sample_subreddits_list_response)
        )
        result = runner.invoke(app, ["subreddits", "--limit", "5"])
        assert result.exit_code == 0

    def test_subreddits_with_sort(
        self, runner: CliRunner, mock_reddit_base, sample_subreddits_list_response
    ):
        """subreddits should accept --sort option."""
        mock_reddit_base.get(url="/subreddits.json", params={"limit": 25, "sort": "gilded"}).mock(
            return_value=httpx.Response(200, json=sample_subreddits_list_response)
        )
        result = runner.invoke(app, ["subreddits", "--sort", "gilded"])
        assert result.exit_code == 0

    def test_subreddits_empty_results(
        self, runner: CliRunner, mock_reddit_base, empty_posts_response
    ):
        """subreddits should handle empty results gracefully."""
        mock_reddit_base.get(url="/subreddits.json", params={"limit": 25, "sort": "subscribers"}).mock(
            return_value=httpx.Response(200, json=empty_posts_response)
        )
        result = runner.invoke(app, ["subreddits"])
        assert result.exit_code == 0


class TestSubredditsSearch:
    """Test suite for subreddits --search command."""

    def test_search_exit_code(
        self, runner: CliRunner, mock_reddit_base, sample_subreddits_list_response
    ):
        """subreddits --search should exit with code 0."""
        mock_reddit_base.get(url="/subreddits/search.json", params={"q": "python", "limit": 25}).mock(
            return_value=httpx.Response(200, json=sample_subreddits_list_response)
        )
        result = runner.invoke(app, ["subreddits", "--search", "python"])
        assert result.exit_code == 0

    def test_search_output_contains_query(
        self, runner: CliRunner, mock_reddit_base, sample_subreddits_list_response
    ):
        """subreddits --search output should mention the query."""
        mock_reddit_base.get(url="/subreddits/search.json", params={"q": "programming", "limit": 25}).mock(
            return_value=httpx.Response(200, json=sample_subreddits_list_response)
        )
        result = runner.invoke(app, ["subreddits", "--search", "programming"])
        assert "programming" in result.output.lower()

    def test_search_missing_query(self, runner: CliRunner):
        """subreddits --search should fail without query."""
        result = runner.invoke(app, ["subreddits", "--search"])
        assert result.exit_code != 0

    def test_search_no_results(self, runner: CliRunner, mock_reddit_base, empty_posts_response):
        """subreddits --search should handle empty results."""
        mock_reddit_base.get(url="/subreddits/search.json", params={"q": "nonexistent123xyz", "limit": 25}).mock(
            return_value=httpx.Response(200, json=empty_posts_response)
        )
        result = runner.invoke(app, ["subreddits", "--search", "nonexistent123xyz"])
        assert result.exit_code == 0
        assert "No subreddits found" in result.output


class TestSubredditsNew:
    """Test suite for subreddits --new command."""

    def test_new_exit_code(
        self, runner: CliRunner, mock_reddit_base, sample_subreddits_list_response
    ):
        """subreddits --new should exit with code 0."""
        mock_reddit_base.get(url="/subreddits/new.json", params={"limit": 25}).mock(
            return_value=httpx.Response(200, json=sample_subreddits_list_response)
        )
        result = runner.invoke(app, ["subreddits", "--new"])
        assert result.exit_code == 0

    def test_new_with_limit(
        self, runner: CliRunner, mock_reddit_base, sample_subreddits_list_response
    ):
        """subreddits --new should accept --limit option."""
        mock_reddit_base.get(url="/subreddits/new.json", params={"limit": 10}).mock(
            return_value=httpx.Response(200, json=sample_subreddits_list_response)
        )
        result = runner.invoke(app, ["subreddits", "--new", "--limit", "10"])
        assert result.exit_code == 0


class TestSubredditsGold:
    """Test suite for subreddits --gold command."""

    def test_gold_exit_code(
        self, runner: CliRunner, mock_reddit_base, sample_subreddits_list_response
    ):
        """subreddits --gold should exit with code 0."""
        mock_reddit_base.get(url="/subreddits/gold.json", params={"limit": 25}).mock(
            return_value=httpx.Response(200, json=sample_subreddits_list_response)
        )
        result = runner.invoke(app, ["subreddits", "--gold"])
        assert result.exit_code == 0

    def test_gold_output_contains_subreddits(
        self, runner: CliRunner, mock_reddit_base, sample_subreddits_list_response
    ):
        """subreddits --gold output should contain subreddit names."""
        mock_reddit_base.get(url="/subreddits/gold.json", params={"limit": 25}).mock(
            return_value=httpx.Response(200, json=sample_subreddits_list_response)
        )
        result = runner.invoke(app, ["subreddits", "--gold"])
        assert "python" in result.output


class TestSubredditsDefault:
    """Test suite for subreddits --default command."""

    def test_default_exit_code(
        self, runner: CliRunner, mock_reddit_base, sample_subreddits_list_response
    ):
        """subreddits --default should exit with code 0."""
        mock_reddit_base.get(url="/subreddits/default.json", params={"limit": 25}).mock(
            return_value=httpx.Response(200, json=sample_subreddits_list_response)
        )
        result = runner.invoke(app, ["subreddits", "--default"])
        assert result.exit_code == 0

    def test_default_output_contains_subreddits(
        self, runner: CliRunner, mock_reddit_base, sample_subreddits_list_response
    ):
        """subreddits --default output should contain subreddit names."""
        mock_reddit_base.get(url="/subreddits/default.json", params={"limit": 25}).mock(
            return_value=httpx.Response(200, json=sample_subreddits_list_response)
        )
        result = runner.invoke(app, ["subreddits", "--default"])
        assert "python" in result.output
