import asyncio
import sys
import typer

from reddit_cli.reddit import RedditClient, PostsClient

post_app = typer.Typer()


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


@post_app.callback(invoke_without_command=True)
def post(post_id: str) -> None:
    """View a single post by ID.

    Args:
        post_id: Post ID (with or without t3_ prefix)
    """
    asyncio.run(_post_async(post_id))


@post_app.command(name="view")
def view(post_id: str) -> None:
    """Alias for post command.

    Args:
        post_id: Post ID (with or without t3_ prefix)
    """
    asyncio.run(_post_async(post_id))


@post_app.command(name="info")
def info(post_id: str) -> None:
    """Get detailed info about a post.

    Args:
        post_id: Post ID (with or without t3_ prefix)
    """
    asyncio.run(_post_async(post_id))


@post_app.command(name="duplicates")
def duplicates(post_id: str) -> None:
    """Get all crossposts/duplicates of a post.

    Args:
        post_id: Post ID (with or without t3_ prefix)
    """
    asyncio.run(_duplicates_async(post_id))


async def _duplicates_async(post_id: str) -> None:
    """Async implementation of duplicates."""
    async with RedditClient() as client:
        posts_client = PostsClient(client)
        original, crossposts = await posts_client.get_duplicates(post_id)

        print("Original Post:")
        print(f"  [{original.score}] {original.title}")
        print(f"  r/{original.subreddit} by {original.author}")
        print(f"  https://reddit.com{original.permalink}")
        print()

        if crossposts:
            print(f"Crossposts ({len(crossposts)}):")
            for cp in crossposts:
                print(f"  [{cp.score}] {cp.title}")
                print(f"    r/{cp.subreddit} by {cp.author}")
                print(f"    https://reddit.com{cp.permalink}")
                print()
        else:
            print("No crossposts found.")
