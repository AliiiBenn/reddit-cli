"""Export utilities for SQL, CSV, and JSON formats."""

import json
import re
from reddit_cli.reddit.models import Post, Comment, Subreddit

# Whitelist pattern for table names (alphanumeric and underscores only)
_VALID_TABLE_NAME_PATTERN = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

# Maximum length for table names
_MAX_TABLE_NAME_LENGTH = 64


def _validate_table_name(table: str) -> str:
    """Validate table name to prevent SQL injection.

    Args:
        table: Table name to validate

    Returns:
        Validated table name

    Raises:
        ValueError: If table name contains invalid characters or is too long
    """
    if not table or len(table) > _MAX_TABLE_NAME_LENGTH:
        raise ValueError(f"Invalid table name: {table}")
    if not _VALID_TABLE_NAME_PATTERN.match(table):
        raise ValueError(f"Table name must contain only alphanumeric characters and underscores: {table}")
    return table


def escape_sql_value(value: str) -> str:
    """Escape a string value for SQL insertion.

    Args:
        value: String value to escape

    Returns:
        Escaped string safe for SQL
    """
    return value.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n").replace("\r", "\\r")


def post_to_sql_insert(post: Post, table: str = "posts") -> str:
    """Convert a Post to a SQL INSERT statement.

    Args:
        post: Post model instance
        table: Table name

    Returns:
        SQL INSERT statement
    """
    safe_table = _validate_table_name(table)
    return (
        f"INSERT INTO {safe_table} "
        f"(id, title, author, subreddit, score, num_comments, url, permalink, created_utc, selftext) "
        f"VALUES "
        f"('{post.id}', '{escape_sql_value(post.title)}', '{escape_sql_value(post.author)}', "
        f"'{escape_sql_value(post.subreddit)}', {post.score}, {post.num_comments}, "
        f"'{escape_sql_value(post.url)}', '{escape_sql_value(post.permalink)}', "
        f"{post.created_utc}, '{escape_sql_value(post.selftext)}');"
    )


def post_to_csv_row(post: Post) -> str:
    """Convert a Post to a CSV row.

    Args:
        post: Post model instance

    Returns:
        CSV row string
    """
    return (
        f"{post.id},"
        f"\"{post.title.replace('\"', '\"\"')}\","
        f"{post.author},"
        f"{post.subreddit},"
        f"{post.score},"
        f"{post.num_comments},"
        f"\"{post.url.replace('\"', '\"\"')}\","
        f"\"{post.permalink.replace('\"', '\"\"')}\","
        f"{post.created_utc},"
        f"\"{post.selftext.replace('\"', '\"\"')}\""
    )


def post_csv_header() -> str:
    """Return CSV header for posts."""
    return "id,title,author,subreddit,score,num_comments,url,permalink,created_utc,selftext"


def comment_to_sql_insert(comment: Comment, table: str = "comments") -> str:
    """Convert a Comment to a SQL INSERT statement.

    Args:
        comment: Comment model instance
        table: Table name

    Returns:
        SQL INSERT statement
    """
    safe_table = _validate_table_name(table)
    return (
        f"INSERT INTO {safe_table} "
        f"(id, author, body, score, created_utc, parent_id, link_id, depth) "
        f"VALUES "
        f"('{comment.id}', '{escape_sql_value(comment.author)}', '{escape_sql_value(comment.body)}', "
        f"{comment.score}, {comment.created_utc}, '{comment.parent_id}', '{comment.link_id}', {comment.depth});"
    )


def comment_to_csv_row(comment: Comment) -> str:
    """Convert a Comment to a CSV row.

    Args:
        comment: Comment model instance

    Returns:
        CSV row string
    """
    return (
        f"{comment.id},"
        f"{comment.author},"
        f"\"{comment.body.replace('\"', '\"\"')}\","
        f"{comment.score},"
        f"{comment.created_utc},"
        f"{comment.parent_id},"
        f"{comment.link_id},"
        f"{comment.depth}"
    )


def comment_csv_header() -> str:
    """Return CSV header for comments."""
    return "id,author,body,score,created_utc,parent_id,link_id,depth"


def subreddit_to_sql_insert(subreddit: Subreddit, table: str = "subreddits") -> str:
    """Convert a Subreddit to a SQL INSERT statement.

    Args:
        subreddit: Subreddit model instance
        table: Table name

    Returns:
        SQL INSERT statement
    """
    safe_table = _validate_table_name(table)
    return (
        f"INSERT INTO {safe_table} "
        f"(id, display_name, title, description, subscribers, active_users) "
        f"VALUES "
        f"('{subreddit.id}', '{escape_sql_value(subreddit.display_name)}', "
        f"'{escape_sql_value(subreddit.title)}', '{escape_sql_value(subreddit.description)}', "
        f"{subreddit.subscribers}, {subreddit.active_users});"
    )


def subreddit_to_csv_row(subreddit: Subreddit) -> str:
    """Convert a Subreddit to a CSV row.

    Args:
        subreddit: Subreddit model instance

    Returns:
        CSV row string
    """
    return (
        f"{subreddit.id},"
        f"\"{subreddit.display_name.replace('\"', '\"\"')}\","
        f"\"{subreddit.title.replace('\"', '\"\"')}\","
        f"\"{subreddit.description.replace('\"', '\"\"')}\","
        f"{subreddit.subscribers},"
        f"{subreddit.active_users}"
    )


def subreddit_csv_header() -> str:
    """Return CSV header for subreddits."""
    return "id,display_name,title,description,subscribers,active_users"


def post_to_json(post: Post) -> str:
    """Convert a Post to a JSON string.

    Args:
        post: Post model instance

    Returns:
        JSON string representation of the post
    """
    return json.dumps(post.model_dump(), ensure_ascii=False)


def posts_to_json(posts: list[Post]) -> str:
    """Convert a list of Posts to a JSON string.

    Args:
        posts: List of Post model instances

    Returns:
        JSON string representation of the posts
    """
    return json.dumps([post.model_dump() for post in posts], ensure_ascii=False)


def comment_to_json(comment: Comment) -> str:
    """Convert a Comment to a JSON string.

    Args:
        comment: Comment model instance

    Returns:
        JSON string representation of the comment
    """
    return json.dumps(comment.model_dump(), ensure_ascii=False)


def comments_to_json(comments: list[Comment]) -> str:
    """Convert a list of Comments to a JSON string.

    Args:
        comments: List of Comment model instances

    Returns:
        JSON string representation of the comments
    """
    return json.dumps([comment.model_dump() for comment in comments], ensure_ascii=False)
