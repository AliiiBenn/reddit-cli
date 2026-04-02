import asyncio
import sys
import typer

from reddit_cli.errors import handle_api_error
from reddit_cli.reddit import RedditClient, CommentsClient, Comment


async def _comments_async(
    post_id: str,
    sort: str = "confidence",
    depth: int | None = None,
) -> None:
    """Async implementation of comments."""
    async with RedditClient() as client:
        comments_client = CommentsClient(client)
        comments = await comments_client.get_comments(post_id, sort, depth)

        for comment in comments:
            _print_comment(comment)


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
) -> None:
    """View comments for a post.

    Args:
        post_id: Post ID (with or without t3_ prefix)
        sort: Sort type (confidence, top, new, old, controversial, qa)
        depth: Maximum comment depth
    """
    try:
        asyncio.run(_comments_async(post_id, sort, depth))
    except Exception as e:
        handle_api_error(e)


# Alias
def comment(
    post_id: str,
    comment_id: str,
    replies: bool = False,
) -> None:
    """View a single comment from a post.

    Args:
        post_id: Post ID (with or without t3_ prefix)
        comment_id: Comment ID (with or without t1_ prefix)
        replies: Include replies
    """
    try:
        asyncio.run(_comment_async(post_id, comment_id, replies))
    except Exception as e:
        handle_api_error(e)


async def _comment_async(
    post_id: str,
    comment_id: str,
    replies: bool = False,
) -> None:
    """Async implementation of single comment."""
    async with RedditClient() as client:
        comments_client = CommentsClient(client)
        depth = 999 if replies else 0
        comments = await comments_client.get_comments(post_id, depth=depth)

        # Find the specific comment
        target_id = comment_id.removeprefix("t1_")
        for c in comments:
            if c.id == target_id:
                typer.echo(f"[{c.score}] {c.author}")
                typer.echo(f"ID: {c.id}")
                typer.echo(f"Parent: {c.parent_id}")
                body = c.body.encode(sys.stdout.encoding, errors="replace").decode(
                    sys.stdout.encoding
                )
                typer.echo(body)
                typer.echo()
                if replies and c.replies:
                    typer.echo("Replies:")
                    for reply in c.replies:
                        _print_comment(reply, 1)
                return

        typer.echo(f"Comment {comment_id} not found in post {post_id}")
