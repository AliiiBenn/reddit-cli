"""Tests for comments commands: comments, comment."""
import pytest
import respx
import httpx
from typer.testing import CliRunner

from reddit_cli import app


@pytest.fixture
def sample_comments_response() -> dict:
    """Sample comments listing response."""
    return {
        "data": {
            "children": [
                {
                    "kind": "t1",
                    "data": {
                        "id": "comment1",
                        "body": "This is a great post!",
                        "author": "commenter1",
                        "score": 42,
                        "created_utc": 1704067200.0,
                        "depth": 0,
                        "parent_id": "t3_abc123",
                        "link_id": "t3_abc123",
                        "replies": [],
                    },
                },
                {
                    "kind": "t1",
                    "data": {
                        "id": "comment2",
                        "body": "I disagree with this.",
                        "author": "commenter2",
                        "score": 10,
                        "created_utc": 1704067201.0,
                        "depth": 0,
                        "parent_id": "t3_abc123",
                        "link_id": "t3_abc123",
                        "replies": [],
                    },
                },
            ]
        }
    }


@pytest.fixture
def sample_comment_thread_response() -> dict:
    """Sample comment thread with replies."""
    return {
        "data": {
            "children": [
                {
                    "kind": "t1",
                    "data": {
                        "id": "comment1",
                        "body": "Main comment",
                        "author": "main_commenter",
                        "score": 100,
                        "created_utc": 1704067200.0,
                        "depth": 0,
                        "parent_id": "t3_abc123",
                        "link_id": "t3_abc123",
                        "replies": {
                            "data": {
                                "children": [
                                    {
                                        "kind": "t1",
                                        "data": {
                                            "id": "reply1",
                                            "body": "This is a reply",
                                            "author": "replier",
                                            "score": 20,
                                            "created_utc": 1704067201.0,
                                            "depth": 1,
                                            "parent_id": "t1_comment1",
                                            "link_id": "t3_abc123",
                                            "replies": "",
                                        },
                                    }
                                ]
                            }
                        },
                    },
                }
            ]
        }
    }


class TestComments:
    """Test suite for comments command."""

    def test_comments_exit_code(
        self, runner: CliRunner, mock_reddit_base, sample_comments_response
    ):
        """comments should exit with code 0."""
        mock_reddit_base.get("/comments/abc123.json?sort=confidence").mock(
            return_value=httpx.Response(
                200, json=[{"data": {"children": []}}, sample_comments_response]
            )
        )
        result = runner.invoke(app, ["comments", "abc123"])
        assert result.exit_code == 0

    def test_comments_output_contains_comment_body(
        self, runner: CliRunner, mock_reddit_base, sample_comments_response
    ):
        """comments output should contain comment body."""
        mock_reddit_base.get("/comments/abc123.json?sort=confidence").mock(
            return_value=httpx.Response(
                200, json=[{"data": {"children": []}}, sample_comments_response]
            )
        )
        result = runner.invoke(app, ["comments", "abc123"])
        assert "This is a great post!" in result.output

    def test_comments_output_contains_author(
        self, runner: CliRunner, mock_reddit_base, sample_comments_response
    ):
        """comments output should contain author name."""
        mock_reddit_base.get("/comments/abc123.json?sort=confidence").mock(
            return_value=httpx.Response(
                200, json=[{"data": {"children": []}}, sample_comments_response]
            )
        )
        result = runner.invoke(app, ["comments", "abc123"])
        assert "commenter1" in result.output

    def test_comments_with_t3_prefix(
        self, runner: CliRunner, mock_reddit_base, sample_comments_response
    ):
        """comments should accept post ID with t3_ prefix."""
        mock_reddit_base.get("/comments/abc123.json?sort=confidence").mock(
            return_value=httpx.Response(
                200, json=[{"data": {"children": []}}, sample_comments_response]
            )
        )
        result = runner.invoke(app, ["comments", "t3_abc123"])
        assert result.exit_code == 0

    def test_comments_with_sort_option(
        self, runner: CliRunner, mock_reddit_base, sample_comments_response
    ):
        """comments should accept --sort option."""
        mock_reddit_base.get("/comments/abc123.json?sort=top").mock(
            return_value=httpx.Response(
                200, json=[{"data": {"children": []}}, sample_comments_response]
            )
        )
        result = runner.invoke(app, ["comments", "abc123", "--sort", "top"])
        assert result.exit_code == 0

    def test_comments_with_depth_option(
        self, runner: CliRunner, mock_reddit_base, sample_comments_response
    ):
        """comments should accept --depth option."""
        mock_reddit_base.get("/comments/abc123.json?sort=confidence").mock(
            return_value=httpx.Response(
                200, json=[{"data": {"children": []}}, sample_comments_response]
            )
        )
        result = runner.invoke(app, ["comments", "abc123", "--depth", "3"])
        assert result.exit_code == 0

    def test_comments_missing_post_id(self, runner: CliRunner):
        """comments should fail without post ID."""
        result = runner.invoke(app, ["comments"])
        assert result.exit_code != 0


class TestComment:
    """Test suite for comment (single comment) command."""

    def test_comment_exit_code(
        self, runner: CliRunner, mock_reddit_base, sample_comment_thread_response
    ):
        """comment should exit with code 0."""
        mock_reddit_base.get("/comments/abc123.json?sort=confidence").mock(
            return_value=httpx.Response(
                200, json=[{"data": {"children": []}}, sample_comment_thread_response]
            )
        )
        result = runner.invoke(app, ["comment", "abc123", "comment1"])
        assert result.exit_code == 0

    def test_comment_output_contains_body(
        self, runner: CliRunner, mock_reddit_base, sample_comment_thread_response
    ):
        """comment output should contain comment body."""
        mock_reddit_base.get("/comments/abc123.json?sort=confidence").mock(
            return_value=httpx.Response(
                200, json=[{"data": {"children": []}}, sample_comment_thread_response]
            )
        )
        result = runner.invoke(app, ["comment", "abc123", "comment1"])
        assert "Main comment" in result.output

    def test_comment_output_contains_id(
        self, runner: CliRunner, mock_reddit_base, sample_comment_thread_response
    ):
        """comment output should contain comment ID."""
        mock_reddit_base.get("/comments/abc123.json?sort=confidence").mock(
            return_value=httpx.Response(
                200, json=[{"data": {"children": []}}, sample_comment_thread_response]
            )
        )
        result = runner.invoke(app, ["comment", "abc123", "comment1"])
        assert "comment1" in result.output

    def test_comment_with_replies_flag(
        self, runner: CliRunner, mock_reddit_base, sample_comment_thread_response
    ):
        """comment with --replies should show replies."""
        mock_reddit_base.get("/comments/abc123.json?sort=confidence").mock(
            return_value=httpx.Response(
                200, json=[{"data": {"children": []}}, sample_comment_thread_response]
            )
        )
        result = runner.invoke(app, ["comment", "abc123", "comment1", "--replies"])
        assert result.exit_code == 0
        assert "reply" in result.output.lower()

    def test_comment_not_found(
        self, runner: CliRunner, mock_reddit_base, sample_comment_thread_response
    ):
        """comment should handle not found gracefully."""
        mock_reddit_base.get("/comments/abc123.json?sort=confidence").mock(
            return_value=httpx.Response(
                200, json=[{"data": {"children": []}}, sample_comment_thread_response]
            )
        )
        result = runner.invoke(app, ["comment", "abc123", "nonexistent"])
        assert result.exit_code == 0
        assert "not found" in result.output.lower()

    def test_comment_missing_args(self, runner: CliRunner):
        """comment should fail without post_id and comment_id."""
        result = runner.invoke(app, ["comment"])
        assert result.exit_code != 0

    def test_comment_missing_comment_id(self, runner: CliRunner):
        """comment should fail without comment_id."""
        result = runner.invoke(app, ["comment", "abc123"])
        assert result.exit_code != 0
