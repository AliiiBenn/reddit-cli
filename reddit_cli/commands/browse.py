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


async def _browse_async(
    subreddit: str,
    sort: str = "hot",
    limit: int = 25,
    period: str | None = None,
    after: str | None = None,
    before: str | None = None,
) -> None:
    """Async implementation of browse."""
    async with RedditClient() as client:
        posts_client = PostsClient(client)
        posts, after_cursor, before_cursor = await posts_client.list_posts(
            subreddit, sort, limit, period, after, before
        )

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


async def _sticky_async(subreddit: str) -> None:
    """Async implementation of sticky."""
    async with RedditClient() as client:
        posts_client = PostsClient(client)
        post = await posts_client.get_sticky(subreddit)
        print(f"[{post.score}] {post.title}")
        print(f"  ID: {post.id}")
        print(f"  r/{post.subreddit} by {post.author}")
        print(f"  {post.num_comments} comments")
        print(f"  URL: {post.url}")


async def _random_async(subreddit: str) -> None:
    """Async implementation of random."""
    async with RedditClient() as client:
        posts_client = PostsClient(client)
        try:
            post = await posts_client.get_random(subreddit)
            print(f"[{post.score}] {post.title}")
            print(f"  ID: {post.id}")
            print(f"  r/{post.subreddit} by {post.author}")
            print(f"  {post.num_comments} comments")
            print(f"  URL: {post.url}")
        except ValueError as e:
            print(f"Error: {e}")


async def _search_async(
    subreddit: str,
    query: str,
    sort: str = "relevance",
    limit: int = 25,
    period: str | None = None,
) -> None:
    """Async implementation of subreddit search."""
    async with RedditClient() as client:
        posts_client = PostsClient(client)
        posts, after_cursor, before_cursor = await posts_client.search_posts(
            query, subreddit, sort, limit, period
        )

        if not posts:
            print(f"No posts found matching '{query}' in r/{subreddit}")
            return

        print(f"Search results for '{query}' in r/{subreddit}:")
        print()
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


@app.command(name="browse")
def browse(
    subreddit: str,
    sticky: bool = False,
    random: bool = False,
    search: str | None = None,
    sort: str = "hot",
    limit: int = 25,
    period: str | None = None,
    after: str | None = None,
    before: str | None = None,
) -> None:
    """Browse posts from a subreddit.

    Args:
        subreddit: Subreddit name (without r/)
        sticky: Get the sticky post from the subreddit
        random: Get a random post from the subreddit
        search: Search within the subreddit
        sort: Sort type (hot, new, top, rising, controversial, gilded)
        limit: Number of posts to return
        period: Time period for top/controversial (day, week, month, year, all)
        after: Pagination cursor (get posts after this ID)
        before: Pagination cursor (get posts before this ID)
    """
    try:
        if sticky:
            asyncio.run(_sticky_async(subreddit))
        elif random:
            asyncio.run(_random_async(subreddit))
        elif search:
            asyncio.run(_search_async(subreddit, search, sort, limit, period))
        else:
            asyncio.run(_browse_async(subreddit, sort, limit, period, after, before))
    except Exception as e:
        _handle_api_error(e)


if __name__ == "__main__":
    app()
