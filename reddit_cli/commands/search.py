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


@app.command()
def search(
    query: str,
    sort: str = "relevance",
    limit: int = 25,
    period: str | None = None,
) -> None:
    """Search for posts globally across Reddit.

    Args:
        query: Search query
        sort: Sort type (relevance, hot, top, new, comments)
        limit: Number of results
        period: Time period (day, week, month, year, all)
    """
    try:
        asyncio.run(_search_async(query, sort, limit, period))
    except Exception as e:
        _handle_api_error(e)


async def _search_async(
    query: str,
    sort: str = "relevance",
    limit: int = 25,
    period: str | None = None,
) -> None:
    """Async implementation of global search."""
    async with RedditClient() as client:
        posts_client = PostsClient(client)
        posts, after_cursor, before_cursor = await posts_client.search_posts(
            query, None, sort, limit, period
        )

        if not posts:
            print(f"No posts found matching '{query}'")
            return

        for post in posts:
            print(f"[{post.score}] {post.title}")
            print(f"  ID: {post.id}")
            print(f"  r/{post.subreddit} by {post.author}")
            print(f"  {post.num_comments} comments")
            print()

        if after_cursor or before_cursor:
            print("---")
            if after_cursor:
                print(f"After: {after_cursor}")
            if before_cursor:
                print(f"Before: {before_cursor}")
