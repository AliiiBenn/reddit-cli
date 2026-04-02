"""Unit tests for Pydantic models: Post, Subreddit, Comment."""
import pytest
from pydantic import ValidationError

from reddit_cli.reddit.models import Post, Subreddit, Comment


class TestPostModel:
    """Test suite for Post model validation."""

    def test_post_valid_creation(self):
        """Post model should accept valid data."""
        post = Post(
            id="abc123",
            title="Test Post",
            author="testuser",
            subreddit="python",
            score=100,
            num_comments=42,
            permalink="/r/python/comments/abc123/test/",
            url="https://example.com",
            created_utc=1704067200.0,
            selftext="Test content",
        )
        assert post.id == "abc123"
        assert post.title == "Test Post"
        assert post.author == "testuser"
        assert post.score == 100
        assert post.num_comments == 42
        assert post.selftext == "Test content"

    def test_post_optional_selftext_defaults_to_empty(self):
        """Post selftext should default to empty string."""
        post = Post(
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
        assert post.selftext == ""

    def test_post_short_id_property(self):
        """Post short_id property should return the post ID."""
        post = Post(
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
        assert post.short_id == "abc123"

    def test_post_missing_required_field_raises_error(self):
        """Post model should raise ValidationError for missing required fields."""
        with pytest.raises(ValidationError):
            Post(
                id="abc123",
                title="Test Post",
                # missing author
                subreddit="python",
                score=100,
                num_comments=42,
                permalink="/r/python/comments/abc123/test/",
                url="https://example.com",
                created_utc=1704067200.0,
            )

    def test_post_invalid_field_type_raises_error(self):
        """Post model should raise ValidationError for invalid field types."""
        with pytest.raises(ValidationError):
            Post(
                id="abc123",
                title="Test Post",
                author="testuser",
                subreddit="python",
                score="not an integer",  # should be int
                num_comments=42,
                permalink="/r/python/comments/abc123/test/",
                url="https://example.com",
                created_utc=1704067200.0,
            )


class TestSubredditModel:
    """Test suite for Subreddit model validation."""

    def test_subreddit_valid_creation(self):
        """Subreddit model should accept valid data."""
        sub = Subreddit(
            id="2qh13",
            display_name="python",
            title="Python Programming",
            description="Python discussion",
            subscribers=1500000,
            accounts_active=25000,
        )
        assert sub.id == "2qh13"
        assert sub.display_name == "python"
        assert sub.title == "Python Programming"
        assert sub.subscribers == 1500000
        assert sub.active_users == 25000  # Note: model uses active_users with accounts_active alias

    def test_subreddit_active_users_defaults_to_zero(self):
        """Subreddit active_users should default to 0 when accounts_active not provided."""
        sub = Subreddit(
            id="2qh13",
            display_name="python",
            title="Python Programming",
            description="Python discussion",
            subscribers=1500000,
        )
        assert sub.active_users == 0

    def test_subreddit_missing_required_field_raises_error(self):
        """Subreddit model should raise ValidationError for missing required fields."""
        with pytest.raises(ValidationError):
            Subreddit(
                id="2qh13",
                display_name="python",
                title="Python Programming",
                # missing description
                subscribers=1500000,
            )


class TestCommentModel:
    """Test suite for Comment model validation."""

    def test_comment_valid_creation(self):
        """Comment model should accept valid data."""
        comment = Comment(
            id="def456",
            author="commenter",
            body="This is a comment",
            score=10,
            created_utc=1704067200.0,
            parent_id="t3_abc123",
            link_id="t3_abc123",
            depth=0,
            replies=[],
        )
        assert comment.id == "def456"
        assert comment.body == "This is a comment"
        assert comment.author == "commenter"
        assert comment.score == 10
        assert comment.depth == 0

    def test_comment_depth_defaults_to_zero(self):
        """Comment depth should default to 0."""
        comment = Comment(
            id="def456",
            author="commenter",
            body="This is a comment",
            score=10,
            created_utc=1704067200.0,
            parent_id="t3_abc123",
            link_id="t3_abc123",
        )
        assert comment.depth == 0

    def test_comment_replies_defaults_to_empty_list(self):
        """Comment replies should default to empty list."""
        comment = Comment(
            id="def456",
            author="commenter",
            body="This is a comment",
            score=10,
            created_utc=1704067200.0,
            parent_id="t3_abc123",
            link_id="t3_abc123",
        )
        assert comment.replies == []

    def test_comment_with_nested_replies(self):
        """Comment model should support nested replies."""
        reply = Comment(
            id="reply1",
            author="replier",
            body="This is a reply",
            score=5,
            created_utc=1704067201.0,
            parent_id="t1_def456",
            link_id="t3_abc123",
            depth=1,
        )
        parent = Comment(
            id="def456",
            author="commenter",
            body="This is a comment",
            score=10,
            created_utc=1704067200.0,
            parent_id="t3_abc123",
            link_id="t3_abc123",
            replies=[reply],
        )
        assert len(parent.replies) == 1
        assert parent.replies[0].id == "reply1"

    def test_comment_short_id_property(self):
        """Comment short_id property should return the comment ID."""
        comment = Comment(
            id="def456",
            author="commenter",
            body="This is a comment",
            score=10,
            created_utc=1704067200.0,
            parent_id="t3_abc123",
            link_id="t3_abc123",
        )
        assert comment.short_id == "def456"

    def test_comment_missing_required_field_raises_error(self):
        """Comment model should raise ValidationError for missing required fields."""
        with pytest.raises(ValidationError):
            Comment(
                id="def456",
                author="commenter",
                body="This is a comment",
                score=10,
                created_utc=1704067200.0,
                # missing parent_id
                link_id="t3_abc123",
            )
