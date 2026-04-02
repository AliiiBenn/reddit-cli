"""Tests for API error handling: 404, 500, network failures, rate limiting."""
from typer.testing import CliRunner

from reddit_cli import app


class TestBrowseErrors:
    """Test suite for browse command error handling."""

    def test_browse_404_error(
        self, runner: CliRunner, mock_reddit_base, error_response_404
    ):
        """browse should handle 404 errors gracefully."""
        mock_reddit_base.get("/r/nonexistent subreddit/hot.json").mock(
            return_value=error_response_404
        )
        result = runner.invoke(app, ["browse", "nonexistent subreddit"])
        assert result.exit_code != 0

    def test_browse_500_error(
        self, runner: CliRunner, mock_reddit_base, error_response_500
    ):
        """browse should handle 500 server errors."""
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=error_response_500
        )
        result = runner.invoke(app, ["browse", "python"])
        assert result.exit_code != 0

    def test_browse_rate_limit_error(
        self, runner: CliRunner, mock_reddit_base, error_response_429
    ):
        """browse should handle rate limiting (429) errors."""
        mock_reddit_base.get("/r/python/hot.json").mock(
            return_value=error_response_429
        )
        result = runner.invoke(app, ["browse", "python"])
        assert result.exit_code != 0


class TestSubredditErrors:
    """Test suite for subreddit command error handling."""

    def test_subreddit_404_error(
        self, runner: CliRunner, mock_reddit_base, error_response_404
    ):
        """subreddit should handle 404 errors gracefully."""
        mock_reddit_base.get("/r/nonexistent/about.json").mock(
            return_value=error_response_404
        )
        result = runner.invoke(app, ["subreddit", "nonexistent"])
        assert result.exit_code != 0

    def test_subreddit_500_error(
        self, runner: CliRunner, mock_reddit_base, error_response_500
    ):
        """subreddit should handle 500 server errors."""
        mock_reddit_base.get("/r/python/about.json").mock(
            return_value=error_response_500
        )
        result = runner.invoke(app, ["subreddit", "python"])
        assert result.exit_code != 0


class TestCommentsErrors:
    """Test suite for comments command error handling."""

    def test_comments_404_error(
        self, runner: CliRunner, mock_reddit_base, error_response_404
    ):
        """comments should handle 404 errors gracefully."""
        mock_reddit_base.get("/comments/nonexistent.json").mock(
            return_value=error_response_404
        )
        result = runner.invoke(app, ["comments", "nonexistent"])
        assert result.exit_code != 0

    def test_comments_500_error(
        self, runner: CliRunner, mock_reddit_base, error_response_500
    ):
        """comments should handle 500 server errors."""
        mock_reddit_base.get("/comments/abc123.json").mock(
            return_value=error_response_500
        )
        result = runner.invoke(app, ["comments", "abc123"])
        assert result.exit_code != 0


class TestSearchErrors:
    """Test suite for search command error handling."""

    def test_search_500_error(
        self, runner: CliRunner, mock_reddit_base, error_response_500
    ):
        """search should handle 500 server errors."""
        mock_reddit_base.get("/search.json").mock(
            return_value=error_response_500
        )
        result = runner.invoke(app, ["search", "python"])
        assert result.exit_code != 0

    def test_search_rate_limit_error(
        self, runner: CliRunner, mock_reddit_base, error_response_429
    ):
        """search should handle rate limiting errors."""
        mock_reddit_base.get("/search.json").mock(
            return_value=error_response_429
        )
        result = runner.invoke(app, ["search", "python"])
        assert result.exit_code != 0


class TestPostErrors:
    """Test suite for post command error handling."""

    def test_post_404_error(
        self, runner: CliRunner, mock_reddit_base, error_response_404
    ):
        """post should handle 404 errors gracefully."""
        mock_reddit_base.get("/by_id/t3_nonexistent.json").mock(
            return_value=error_response_404
        )
        result = runner.invoke(app, ["post", "nonexistent"])
        assert result.exit_code != 0

    def test_post_500_error(
        self, runner: CliRunner, mock_reddit_base, error_response_500
    ):
        """post should handle 500 server errors."""
        mock_reddit_base.get("/by_id/t3_abc123.json").mock(
            return_value=error_response_500
        )
        result = runner.invoke(app, ["post", "abc123"])
        assert result.exit_code != 0


class TestSubredditsErrors:
    """Test suite for subreddits command error handling."""

    def test_subreddits_500_error(
        self, runner: CliRunner, mock_reddit_base, error_response_500
    ):
        """subreddits should handle 500 server errors."""
        mock_reddit_base.get(url="/subreddits.json").mock(
            return_value=error_response_500
        )
        result = runner.invoke(app, ["subreddits"])
        assert result.exit_code != 0

    def test_subreddits_search_404(
        self, runner: CliRunner, mock_reddit_base, error_response_404
    ):
        """subreddits --search should handle 404 errors."""
        mock_reddit_base.get(url="/subreddits/search.json").mock(
            return_value=error_response_404
        )
        result = runner.invoke(app, ["subreddits", "--search", "nonexistent"])
        assert result.exit_code != 0
