"""Tests for subreddit commands: subreddit, subreddits, subreddits search/new/gold/default."""
import pytest
import respx
import httpx
from typer.testing import CliRunner

from reddit_cli import app


@pytest.fixture
def sample_subreddit_response() -> dict:
    """Sample subreddit info response."""
    return {
        "data": {
            "name": "python",
            "display_name": "python",
            "title": "Python Programming",
            "description": "Python programming discussion",
            "subscribers": 1500000,
            "active_users": 25000,
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
                        "name": "python",
                        "display_name": "python",
                        "title": "Python Programming",
                        "subscribers": 1500000,
                        "active_users": 25000,
                    },
                },
                {
                    "kind": "t5",
                    "data": {
                        "name": "programming",
                        "display_name": "programming",
                        "title": "Programming",
                        "subscribers": 1000000,
                        "active_users": 15000,
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


@pytest.fixture
def sample_moderators_response() -> list:
    """Sample moderators response."""
    return [
        {"name": "moderator1"},
        {"name": "moderator2"},
    ]


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
        """subreddit --rules should show rules."""
        mock_reddit_base.get("/r/python/about.json").mock(
            return_value=httpx.Response(200, json=sample_subreddit_response)
        )
        mock_reddit_base.get("/r/python/about/rules.json").mock(
            return_value=httpx.Response(200, json=sample_rules_response)
        )
        result = runner.invoke(app, ["subreddit", "python", "--rules"])
        assert result.exit_code == 0
        assert "Be respectful" in result.output

    def test_subreddit_with_moderators_flag(
        self, runner: CliRunner, mock_reddit_base, sample_subreddit_response, sample_moderators_response
    ):
        """subreddit --moderators should show moderators."""
        mock_reddit_base.get("/r/python/about.json").mock(
            return_value=httpx.Response(200, json=sample_subreddit_response)
        )
        mock_reddit_base.get("/r/python/about/moderators.json").mock(
            return_value=httpx.Response(200, json={"data": {"children": sample_moderators_response}})
        )
        result = runner.invoke(app, ["subreddit", "python", "--moderators"])
        assert result.exit_code == 0

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
        mock_reddit_base.get("/subreddits/popular.json").mock(
            return_value=httpx.Response(200, json=sample_subreddits_list_response)
        )
        result = runner.invoke(app, ["subreddits"])
        assert result.exit_code == 0

    def test_subreddits_output_contains_names(
        self, runner: CliRunner, mock_reddit_base, sample_subreddits_list_response
    ):
        """subreddits output should contain subreddit names."""
        mock_reddit_base.get("/subreddits/popular.json").mock(
            return_value=httpx.Response(200, json=sample_subreddits_list_response)
        )
        result = runner.invoke(app, ["subreddits"])
        assert "r/python" in result.output
        assert "r/programming" in result.output

    def test_subreddits_with_limit(
        self, runner: CliRunner, mock_reddit_base, sample_subreddits_list_response
    ):
        """subreddits should accept --limit option."""
        mock_reddit_base.get("/subreddits/popular.json").mock(
            return_value=httpx.Response(200, json=sample_subreddits_list_response)
        )
        result = runner.invoke(app, ["subreddits", "--limit", "5"])
        assert result.exit_code == 0

    def test_subreddits_with_sort(
        self, runner: CliRunner, mock_reddit_base, sample_subreddits_list_response
    ):
        """subreddits should accept --sort option."""
        mock_reddit_base.get("/subreddits/gilded.json").mock(
            return_value=httpx.Response(200, json=sample_subreddits_list_response)
        )
        result = runner.invoke(app, ["subreddits", "--sort", "gilded"])
        assert result.exit_code == 0


class TestSubredditsSearch:
    """Test suite for subreddits search command."""

    def test_search_exit_code(
        self, runner: CliRunner, mock_reddit_base, sample_subreddits_list_response
    ):
        """subreddits search should exit with code 0."""
        mock_reddit_base.get("/subreddits/search.json").mock(
            return_value=httpx.Response(200, json=sample_subreddits_list_response)
        )
        result = runner.invoke(app, ["subreddits", "search", "python"])
        assert result.exit_code == 0

    def test_search_output_contains_query(
        self, runner: CliRunner, mock_reddit_base, sample_subreddits_list_response
    ):
        """subreddits search output should mention the query."""
        mock_reddit_base.get("/subreddits/search.json").mock(
            return_value=httpx.Response(200, json=sample_subreddits_list_response)
        )
        result = runner.invoke(app, ["subreddits", "search", "programming"])
        assert "programming" in result.output.lower()

    def test_search_missing_query(self, runner: CliRunner):
        """subreddits search should fail without query."""
        result = runner.invoke(app, ["subreddits", "search"])
        assert result.exit_code != 0


class TestSubredditsNew:
    """Test suite for subreddits new command."""

    def test_new_exit_code(
        self, runner: CliRunner, mock_reddit_base, sample_subreddits_list_response
    ):
        """subreddits new should exit with code 0."""
        mock_reddit_base.get("/subreddits/new.json").mock(
            return_value=httpx.Response(200, json=sample_subreddits_list_response)
        )
        result = runner.invoke(app, ["subreddits", "new"])
        assert result.exit_code == 0

    def test_new_with_limit(
        self, runner: CliRunner, mock_reddit_base, sample_subreddits_list_response
    ):
        """subreddits new should accept --limit option."""
        mock_reddit_base.get("/subreddits/new.json").mock(
            return_value=httpx.Response(200, json=sample_subreddits_list_response)
        )
        result = runner.invoke(app, ["subreddits", "new", "--limit", "10"])
        assert result.exit_code == 0


class TestSubredditsGold:
    """Test suite for subreddits gold command."""

    def test_gold_exit_code(
        self, runner: CliRunner, mock_reddit_base, sample_subreddits_list_response
    ):
        """subreddits gold should exit with code 0."""
        mock_reddit_base.get("/subreddits/gilded.json").mock(
            return_value=httpx.Response(200, json=sample_subreddits_list_response)
        )
        result = runner.invoke(app, ["subreddits", "gold"])
        assert result.exit_code == 0


class TestSubredditsDefault:
    """Test suite for subreddits default command."""

    def test_default_exit_code(
        self, runner: CliRunner, mock_reddit_base, sample_subreddits_list_response
    ):
        """subreddits default should exit with code 0."""
        mock_reddit_base.get("/subreddits/default.json").mock(
            return_value=httpx.Response(200, json=sample_subreddits_list_response)
        )
        result = runner.invoke(app, ["subreddits", "default"])
        assert result.exit_code == 0
