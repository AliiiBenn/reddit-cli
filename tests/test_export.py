"""Unit tests for export utilities (SQL and CSV formatting)."""
from reddit_cli.export import (
    escape_sql_value,
    post_to_sql_insert,
    post_to_csv_row,
    post_csv_header,
    comment_to_sql_insert,
    comment_to_csv_row,
    comment_csv_header,
    subreddit_to_sql_insert,
    subreddit_to_csv_row,
    subreddit_csv_header,
)
from reddit_cli.reddit.models import Post, Comment, Subreddit

class TestEscapeSqlValue:
    def test_escape_empty_string(self):
        assert escape_sql_value("") == ""
    
    def test_escape_no_special_chars(self):
        assert escape_sql_value("simple text") == "simple text"

class TestPostToSqlInsert:
    def test_post_to_sql_insert_basic(self):
        post = Post(id="abc123", title="Test Post", author="testuser",
                    subreddit="python", score=100, num_comments=42,
                    permalink="/r/python/comments/abc123/test/",
                    url="https://example.com", created_utc=1704067200.0,
                    selftext="Test content")
        sql = post_to_sql_insert(post)
        assert "INSERT INTO posts" in sql
        assert "'abc123'" in sql
        assert "'Test Post'" in sql

    def test_post_to_sql_insert_custom_table(self):
        post = Post(id="abc123", title="Test Post", author="testuser",
                    subreddit="python", score=100, num_comments=42,
                    permalink="/r/python/comments/abc123/test/",
                    url="https://example.com", created_utc=1704067200.0)
        sql = post_to_sql_insert(post, table="custom_posts")
        assert "INSERT INTO custom_posts" in sql

    def test_post_to_sql_insert_empty_selftext(self):
        post = Post(id="abc123", title="Test Post", author="testuser",
                    subreddit="python", score=100, num_comments=42,
                    permalink="/r/python/comments/abc123/test/",
                    url="https://example.com", created_utc=1704067200.0, selftext="")
        sql = post_to_sql_insert(post)
        assert "INSERT INTO posts" in sql

class TestPostToCsvRow:
    def test_post_to_csv_row_basic(self):
        post = Post(id="abc123", title="Test Post", author="testuser",
                    subreddit="python", score=100, num_comments=42,
                    permalink="/r/python/comments/abc123/test/",
                    url="https://example.com", created_utc=1704067200.0,
                    selftext="Test content")
        row = post_to_csv_row(post)
        assert "abc123" in row
        assert "Test Post" in row
        assert "testuser" in row
        assert "100" in row

    def test_post_to_csv_row_empty_selftext(self):
        post = Post(id="abc123", title="Test Post", author="testuser",
                    subreddit="python", score=100, num_comments=42,
                    permalink="/r/python/comments/abc123/test/",
                    url="https://example.com", created_utc=1704067200.0,
                    selftext="")
        row = post_to_csv_row(post)
        assert row.endswith(chr(34) + chr(34))

class TestPostCsvHeader:
    def test_post_csv_header_format(self):
        header = post_csv_header()
        assert header == "id,title,author,subreddit,score,num_comments,url,permalink,created_utc,selftext"

    def test_post_csv_header_has_correct_field_count(self):
        fields = post_csv_header().split(",")
        assert len(fields) == 10

class TestCommentToSqlInsert:
    def test_comment_to_sql_insert_basic(self):
        comment = Comment(id="def456", author="commenter",
                          body="This is a comment", score=10,
                          created_utc=1704067200.0, parent_id="t3_abc123",
                          link_id="t3_abc123", depth=0)
        sql = comment_to_sql_insert(comment)
        assert "INSERT INTO comments" in sql
        assert "'def456'" in sql
        assert "'commenter'" in sql

    def test_comment_to_sql_insert_custom_table(self):
        comment = Comment(id="def456", author="commenter",
                          body="This is a comment", score=10,
                          created_utc=1704067200.0, parent_id="t3_abc123",
                          link_id="t3_abc123", depth=0)
        sql = comment_to_sql_insert(comment, table="custom_comments")
        assert "INSERT INTO custom_comments" in sql

class TestCommentToCsvRow:
    def test_comment_to_csv_row_basic(self):
        comment = Comment(id="def456", author="commenter",
                         body="This is a comment", score=10,
                         created_utc=1704067200.0, parent_id="t3_abc123",
                         link_id="t3_abc123", depth=0)
        row = comment_to_csv_row(comment)
        assert "def456" in row
        assert "commenter" in row
        assert "10" in row
        assert "0" in row

    def test_comment_to_csv_row_with_depth(self):
        comment = Comment(id="def456", author="commenter",
                         body="This is a comment", score=10,
                         created_utc=1704067200.0, parent_id="t3_abc123",
                         link_id="t3_abc123", depth=5)
        row = comment_to_csv_row(comment)
        assert row.endswith(",5")

class TestCommentCsvHeader:
    def test_comment_csv_header_format(self):
        header = comment_csv_header()
        assert header == "id,author,body,score,created_utc,parent_id,link_id,depth"

    def test_comment_csv_header_has_correct_field_count(self):
        fields = comment_csv_header().split(",")
        assert len(fields) == 8


class TestSubredditToSqlInsert:
    def test_subreddit_to_sql_insert_basic(self):
        subreddit = Subreddit(id="2qh13", display_name="python",
                             title="Python Programming",
                             description="Python discussion",
                             subscribers=1500000, accounts_active=25000)
        sql = subreddit_to_sql_insert(subreddit)
        assert "INSERT INTO subreddits" in sql
        assert "'2qh13'" in sql
        assert "1500000" in sql
        assert "25000" in sql

    def test_subreddit_to_sql_insert_custom_table(self):
        subreddit = Subreddit(id="2qh13", display_name="python",
                             title="Python Programming",
                             description="Python discussion",
                             subscribers=1500000)
        sql = subreddit_to_sql_insert(subreddit, table="custom_subs")
        assert "INSERT INTO custom_subs" in sql

class TestSubredditToCsvRow:
    def test_subreddit_to_csv_row_basic(self):
        subreddit = Subreddit(id="2qh13", display_name="python",
                             title="Python Programming",
                             description="Python discussion",
                             subscribers=1500000, accounts_active=25000)
        row = subreddit_to_csv_row(subreddit)
        assert "2qh13" in row
        assert "python" in row
        assert "Python Programming" in row
        assert "1500000" in row
        assert "25000" in row

    def test_subreddit_to_csv_row_empty_description(self):
        subreddit = Subreddit(id="2qh13", display_name="python",
                             title="Python Programming",
                             description="", subscribers=1500000)
        row = subreddit_to_csv_row(subreddit)
        assert ',' + chr(34) + chr(34) + ',' in row


    def test_subreddit_csv_header_format(self):
        header = subreddit_csv_header()
        assert header == "id,display_name,title,description,subscribers,active_users"

    def test_subreddit_csv_header_has_correct_field_count(self):
        fields = subreddit_csv_header().split(",")
        assert len(fields) == 6

    def test_subreddit_with_zero_subscribers(self):
        subreddit = Subreddit(id="2qh13", display_name="test",
                             title="Test Subreddit",
                             description="Description",
                             subscribers=0, accounts_active=0)
        sql = subreddit_to_sql_insert(subreddit)
        csv = subreddit_to_csv_row(subreddit)
        assert ", 0, 0" in sql or ",0,0" in sql
        assert ",0,0" in csv
