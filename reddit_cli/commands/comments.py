import asyncio
import sys
import typer

from reddit_cli.errors import handle_api_error, handle_validation_error
from reddit_cli.export import (
    comment_to_sql_insert,
    comment_to_csv_row,
    comment_csv_header,
)
from reddit_cli.reddit import RedditClient, CommentsClient, Comment


VALID_FORMAT_VALUES = ["display", "sql", "csv"]


def _flatten_comments(comments: list[Comment]) -> list[Comment]:
    """Flatten nested comments into a flat list.

    Args:
        comments: List of comments with nested replies

    Returns:
        Flat list of all comments
    """
    flat = []
    for comment in comments:
        flat.append(comment)
        if comment.replies:
            flat.extend(_flatten_comments(comment.replies))
    return flat


def _write_comments_output(
    comments: list[Comment],
    format_type: str,
    output_file: str | None,
) -> None:
    """Write comments to file or stdout in the specified format.

    Args:
        comments: List of Comment objects
        format_type: Output format (display, sql, csv)
        output_file: File path or None for stdout
    """
    flat_comments = _flatten_comments(comments)

    if format_type == "display":
        return

    lines: list[str] = []
    if format_type == "csv":
        lines.append(comment_csv_header())
        for comment in flat_comments:
            lines.append(comment_to_csv_row(comment))
    elif format_type == "sql":
        for comment in flat_comments:
            lines.append(comment_to_sql_insert(comment))

    output = "\n".join(lines) + "\n"

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(output)
        typer.echo(f"Exported {len(flat_comments)} comments to {output_file}")
    else:
        typer.echo(output)


async def _comments_async(post_id: str, sort: str, depth: int | None) -> list[Comment]:
    """Async implementation of comments.

    Returns:
        List of Comment objects
    """
    async with RedditClient() as client:
        comments_client = CommentsClient(client)
        comments = await comments_client.get_comments(post_id, sort, depth)
        return comments


def _print_comment(comment: "Comment", indent: int = 0) -> None:
    """Print a comment and its replies recursively."""
    prefix = "  " * indent
    body = comment.body.encode(sys.stdout.encoding, errors="replace").decode(
        sys.stdout.encoding
    )

    typer.echo(f"{prefix}[{comment.score}] {comment.author}")
    typer.echo(f"{prefix}{body[:200]}{'...' if len(body) > 200 else ''}")
    typer.echo()

    for reply in comment.replies:
        _print_comment(reply, indent + 1)


def comments(
    post_id: str,
    sort: str = "confidence",
    depth: int | None = None,
    format: str = "display",
    output: str | None = None,
) -> None:
    """View comments for a post.

    Args:
        post_id: Post ID (with or without t3_ prefix)
        sort: Sort type (confidence, top, new, old, controversial, qa)
        depth: Maximum comment depth
        format: Output format (display, sql, csv)
        output: Output file path
    """
    try:
        if format not in VALID_FORMAT_VALUES:
            handle_validation_error("format", VALID_FORMAT_VALUES, format)

        comments_list = asyncio.run(_comments_async(post_id, sort, depth))

        if format == "display":
            for comment in comments_list:
                _print_comment(comment)
        else:
            _write_comments_output(comments_list, format, output)
    except Exception as e:
        handle_api_error(e)


def comment(
    post_id: str,
    comment_id: str,
    replies: bool = False,
    format: str = "display",
    output: str | None = None,
) -> None:
    """View a single comment from a post.

    Args:
        post_id: Post ID (with or without t3_ prefix)
        comment_id: Comment ID (with or without t1_ prefix)
        replies: Include replies
        format: Output format (display, sql, csv)
        output: Output file path
    """
    try:
        if format not in VALID_FORMAT_VALUES:
            handle_validation_error("format", VALID_FORMAT_VALUES, format)

        asyncio.run(_comment_async(post_id, comment_id, replies, format, output))
    except Exception as e:
        handle_api_error(e)


async def _comment_async(
    post_id: str,
    comment_id: str,
    replies: bool = False,
    format: str = "display",
    output: str | None = None,
) -> None:
    """Async implementation of single comment."""
    async with RedditClient() as client:
        comments_client = CommentsClient(client)
        depth = 999 if replies else 0
        comments_list = await comments_client.get_comments(post_id, depth=depth)

        # Find the specific comment
        target_id = comment_id.removeprefix("t1_")
        target_comment = None
        for c in comments_list:
            if c.id == target_id:
                target_comment = c
                break

        if not target_comment:
            typer.echo(f"Comment {comment_id} not found in post {post_id}")
            return

        if format == "display":
            typer.echo(f"[{target_comment.score}] {target_comment.author}")
            typer.echo(f"ID: {target_comment.id}")
            typer.echo(f"Parent: {target_comment.parent_id}")
            body = target_comment.body.encode(sys.stdout.encoding, errors="replace").decode(
                sys.stdout.encoding
            )
            typer.echo(body)
            typer.echo()
            if replies and target_comment.replies:
                typer.echo("Replies:")
                for reply in target_comment.replies:
                    _print_comment(reply, 1)
        else:
            comments_to_export = [target_comment]
            if replies and target_comment.replies:
                comments_to_export.extend(_flatten_comments(target_comment.replies))
            _write_comments_output(comments_to_export, format, output)
