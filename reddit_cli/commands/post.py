import asyncio
import sys
import typer

from reddit_cli.reddit import RedditClient, PostsClient

app = typer.Typer()


async def _post_async(post_id: str) -> None:
    """Async implementation of post."""
    async with RedditClient() as client:
        posts_client = PostsClient(client)
        post = await posts_client.get_post(post_id)

        print(f"Title: {post.title}")
        print(f"Score: {post.score}")
        print(f"Comments: {post.num_comments}")
        print(f"Author: {post.author}")
        print(f"Subreddit: r/{post.subreddit}")
        print(f"URL: {post.url}")
        print(f"Permalink: https://reddit.com{post.permalink}")
        print()
        if post.selftext:
            print(post.selftext.encode(sys.stdout.encoding, errors="replace").decode(sys.stdout.encoding))


@app.command()
def post(post_id: str) -> None:
    """View a single post by ID.

    Args:
        post_id: Post ID (with or without t3_ prefix)
    """
    asyncio.run(_post_async(post_id))


@app.command(name="view")
def view(post_id: str) -> None:
    """Alias for post command.

    Args:
        post_id: Post ID (with or without t3_ prefix)
    """
    asyncio.run(_post_async(post_id))
