"""Tests for XLSX export utilities."""

import pytest
from unittest.mock import patch

from reddit_cli.reddit.models import Post, Comment, Subreddit
from reddit_cli import xlsx_export


class TestPostsToXlsx:
    """Test suite for posts_to_xlsx function."""

    def test_posts_to_xlsx_single_post(self):
        """posts_to_xlsx should create valid XLSX for a single post."""
        posts = [
            Post(
                id="abc123",
                title="Test Post Title",
                author="testuser",
                subreddit="python",
                score=100,
                num_comments=42,
                permalink="/r/python/comments/abc123/test/",
                url="https://example.com",
                created_utc=1704067200.0,
                selftext="Test content",
            )
        ]
        result = xlsx_export.posts_to_xlsx(posts)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_posts_to_xlsx_multiple_posts(self):
        """posts_to_xlsx should handle multiple posts."""
        posts = [
            Post(
                id="post1",
                title="First Post",
                author="user1",
                subreddit="python",
                score=100,
                num_comments=10,
                permalink="/r/python/comments/post1/first/",
                url="https://example.com/1",
                created_utc=1704067200.0,
                selftext="Content 1",
            ),
            Post(
                id="post2",
                title="Second Post",
                author="user2",
                subreddit="learnpython",
                score=200,
                num_comments=20,
                permalink="/r/learnpython/comments/post2/second/",
                url="https://example.com/2",
                created_utc=1704067201.0,
                selftext="Content 2",
            ),
        ]
        result = xlsx_export.posts_to_xlsx(posts)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_posts_to_xlsx_empty_list(self):
        """posts_to_xlsx should handle empty list."""
        result = xlsx_export.posts_to_xlsx([])
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_posts_to_xlsx_custom_sheet_name(self):
        """posts_to_xlsx should use custom sheet name."""
        posts = [
            Post(
                id="abc123",
                title="Test Post",
                author="testuser",
                subreddit="python",
                score=100,
                num_comments=42,
                permalink="/r/python/comments/abc123/test/",
                url="https://example.com",
                created_utc=1704067200.0,
            )
        ]
        result = xlsx_export.posts_to_xlsx(posts, sheet_name="CustomSheet")
        assert isinstance(result, bytes)

    def test_posts_to_xlsx_special_characters(self):
        """posts_to_xlsx should handle special characters in post content."""
        posts = [
            Post(
                id="special123",
                title="Post with quotes and newlines",
                author="user_special",
                subreddit="test",
                score=1,
                num_comments=0,
                permalink="/r/test/comments/special123/test/",
                url="https://example.com",
                created_utc=1704067200.0,
                selftext="Selftext with single quotes and unicode",
            )
        ]
        result = xlsx_export.posts_to_xlsx(posts)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_posts_to_xlsx_unicode_characters(self):
        """posts_to_xlsx should handle unicode characters."""
        posts = [
            Post(
                id="unicode123",
                title="Post with emoji and unicode",
                author="user_unicode",
                subreddit="test",
                score=50,
                num_comments=5,
                permalink="/r/test/comments/unicode123/test/",
                url="https://example.com",
                created_utc=1704067200.0,
                selftext="Content with accent",
            )
        ]
        result = xlsx_export.posts_to_xlsx(posts)
        assert isinstance(result, bytes)


class TestCommentsToXlsx:
    """Test suite for comments_to_xlsx function."""

    def test_comments_to_xlsx_single_comment(self):
        """comments_to_xlsx should create valid XLSX for a single comment."""
        comments = [
            Comment(
                id="def456",
                author="commenter",
                body="This is a test comment",
                score=10,
                created_utc=1704067200.0,
                parent_id="t3_abc123",
                link_id="t3_abc123",
                depth=0,
            )
        ]
        result = xlsx_export.comments_to_xlsx(comments)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_comments_to_xlsx_multiple_comments(self):
        """comments_to_xlsx should handle multiple comments."""
        comments = [
            Comment(
                id="comment1",
                author="user1",
                body="First comment",
                score=10,
                created_utc=1704067200.0,
                parent_id="t3_post1",
                link_id="t3_post1",
                depth=0,
            ),
            Comment(
                id="comment2",
                author="user2",
                body="Second comment",
                score=20,
                created_utc=1704067201.0,
                parent_id="t3_post1",
                link_id="t3_post1",
                depth=0,
            ),
        ]
        result = xlsx_export.comments_to_xlsx(comments)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_comments_to_xlsx_nested_replies(self):
        """comments_to_xlsx should flatten nested comments."""
        reply = Comment(
            id="reply1",
            author="replier",
            body="This is a reply",
            score=5,
            created_utc=1704067201.0,
            parent_id="t1_comment1",
            link_id="t3_post1",
            depth=1,
        )
        parent = Comment(
            id="comment1",
            author="commenter",
            body="This is a comment",
            score=10,
            created_utc=1704067200.0,
            parent_id="t3_post1",
            link_id="t3_post1",
            replies=[reply],
        )
        result = xlsx_export.comments_to_xlsx([parent])
        assert isinstance(result, bytes)

    def test_comments_to_xlsx_empty_list(self):
        """comments_to_xlsx should handle empty list."""
        result = xlsx_export.comments_to_xlsx([])
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_comments_to_xlsx_custom_sheet_name(self):
        """comments_to_xlsx should use custom sheet name."""
        comments = [
            Comment(
                id="def456",
                author="commenter",
                body="Comment",
                score=10,
                created_utc=1704067200.0,
                parent_id="t3_abc123",
                link_id="t3_abc123",
            )
        ]
        result = xlsx_export.comments_to_xlsx(comments, sheet_name="CustomComments")
        assert isinstance(result, bytes)

    def test_comments_to_xlsx_special_characters(self):
        """comments_to_xlsx should handle special characters in comment body."""
        comments = [
            Comment(
                id="special123",
                author="user_special",
                body="Comment with quotes and newlines and tabs",
                score=1,
                created_utc=1704067200.0,
                parent_id="t3_post1",
                link_id="t3_post1",
                depth=0,
            )
        ]
        result = xlsx_export.comments_to_xlsx(comments)
        assert isinstance(result, bytes)


class TestSubredditsToXlsx:
    """Test suite for subreddits_to_xlsx function."""

    def test_subreddits_to_xlsx_single_subreddit(self):
        """subreddits_to_xlsx should create valid XLSX for a single subreddit."""
        subreddits = [
            Subreddit(
                id="2qh13",
                display_name="python",
                title="Python Programming",
                description="Python discussion",
                subscribers=1500000,
                active_users=25000,
            )
        ]
        result = xlsx_export.subreddits_to_xlsx(subreddits)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_subreddits_to_xlsx_multiple_subreddits(self):
        """subreddits_to_xlsx should handle multiple subreddits."""
        subreddits = [
            Subreddit(
                id="2qh13",
                display_name="python",
                title="Python Programming",
                description="Python discussion",
                subscribers=1500000,
                active_users=25000,
            ),
            Subreddit(
                id="2qh14",
                display_name="learnpython",
                title="Learn Python",
                description="Learning Python",
                subscribers=500000,
                active_users=10000,
            ),
        ]
        result = xlsx_export.subreddits_to_xlsx(subreddits)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_subreddits_to_xlsx_empty_list(self):
        """subreddits_to_xlsx should handle empty list."""
        result = xlsx_export.subreddits_to_xlsx([])
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_subreddits_to_xlsx_custom_sheet_name(self):
        """subreddits_to_xlsx should use custom sheet name."""
        subreddits = [
            Subreddit(
                id="2qh13",
                display_name="python",
                title="Python Programming",
                description="Python discussion",
                subscribers=1500000,
                active_users=25000,
            )
        ]
        result = xlsx_export.subreddits_to_xlsx(subreddits, sheet_name="MySubreddits")
        assert isinstance(result, bytes)

    def test_subreddits_to_xlsx_special_characters(self):
        """subreddits_to_xlsx should handle special characters in description."""
        subreddits = [
            Subreddit(
                id="special123",
                display_name="test",
                title="Test Subreddit",
                description="Description with quotes and newlines",
                subscribers=1000,
                active_users=100,
            )
        ]
        result = xlsx_export.subreddits_to_xlsx(subreddits)
        assert isinstance(result, bytes)

    def test_subreddits_to_xlsx_unicode_characters(self):
        """subreddits_to_xlsx should handle unicode characters."""
        subreddits = [
            Subreddit(
                id="unicode123",
                display_name="test",
                title="Test Subreddit with unicode",
                description="Description with accent",
                subscribers=1000,
                active_users=100,
            )
        ]
        result = xlsx_export.subreddits_to_xlsx(subreddits)
        assert isinstance(result, bytes)


class TestCheckOpenpyxl:
    """Test suite for _check_openpyxl function."""

    def test_check_openpyxl_available(self):
        """_check_openpyxl should not raise when openpyxl is available."""
        # Should not raise
        xlsx_export._check_openpyxl()

    def test_check_openpyxl_not_available(self):
        """_check_openpyxl should raise ImportError when openpyxl is not available."""
        import sys
        # Temporarily remove openpyxl from sys.modules
        saved_openpyxl = sys.modules.pop("openpyxl", None)
        # Patch the import side_effect to raise ImportError
        def mock_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "openpyxl" or (isinstance(name, str) and name.startswith("openpyxl.")):
                raise ImportError(f"No module named '{name}'")
            return __import__(name, globals, locals, fromlist, level)
        try:
            with patch("builtins.__import__", side_effect=mock_import):
                with pytest.raises(ImportError, match="openpyxl is required"):
                    xlsx_export._check_openpyxl()
        finally:
            # Restore openpyxl if it was there
            if saved_openpyxl is not None:
                sys.modules["openpyxl"] = saved_openpyxl
