import asyncio
import sys
import typer

from reddit_cli.errors import handle_api_error
from reddit_cli.reddit import RedditClient, PostsClient


async def _post_async(post_id: str) -> None:
    """Async implementation of post."""
    async with RedditClient() as client:
        posts_client = PostsClient(client)
        post = await posts_client.get_post(post_id)

        typer.echo(f"Title: {post.title}")
        typer.echo(f"Score: {post.score}")
        typer.echo(f"Comments: {post.num_comments}")
        typer.echo(f"Author: {post.author}")
        typer.echo(f"Subreddit: r/{post.subreddit}")
        typer.echo(f"URL: {post.url}")
        typer.echo(f"Permalink: https://reddit.com{post.permalink}")
        typer.echo()
        if post.selftext:
            typer.echo(post.selftext.encode(sys.stdout.encoding, errors="replace").decode(sys.stdout.encoding))


def post(
    post_id: str,
    view: bool = False,
    info: bool = False,
) -> None:
    """View a single post by ID.

    Args:
        post_id: Post ID (with or without t3_ prefix)
        view: Show post details
        info: Show detailed post info
    """
    try:
        asyncio.run(_post_async(post_id))
    except Exception as e:
        handle_api_error(e)
