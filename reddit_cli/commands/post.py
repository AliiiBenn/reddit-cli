import asyncio
import sys
import httpx
import typer

from reddit_cli.reddit import RedditClient, PostsClient

app = typer.Typer()


def _handle_api_error(e: Exception) -> None:
    """Print a user-friendly error message for API errors and exit with code 1."""
    if isinstance(e, httpx.TimeoutException):
        print("Error: Connection timed out. Please check your internet connection and try again.", file=sys.stderr)
    elif isinstance(e, httpx.ConnectError):
        print("Error: Could not connect to Reddit. Please check your internet connection.", file=sys.stderr)
    elif isinstance(e, httpx.HTTPStatusError):
        print(f"Error: Reddit API returned status {e.response.status_code}. Please try again later.", file=sys.stderr)
    else:
        print(f"Error: {e}", file=sys.stderr)
    raise typer.Exit(1)


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


@app.command(name="post")
def post(
    post_id: str,
    view: bool = False,
    info: bool = False,
    duplicates: bool = False,
) -> None:
    """View a single post by ID.

    Args:
        post_id: Post ID (with or without t3_ prefix)
        view: Show post details (alias for post)
        info: Show detailed post info
        duplicates: Show crossposts/duplicates of the post
    """
    try:
        if duplicates:
            asyncio.run(_duplicates_async(post_id))
        else:
            asyncio.run(_post_async(post_id))
    except Exception as e:
        _handle_api_error(e)


if __name__ == "__main__":
    app()
