import asyncio
import typer

from reddit_cli.errors import handle_api_error, handle_validation_error
from reddit_cli.reddit import RedditClient, PostsClient


# Valid values for CLI validation
VALID_SORT_VALUES = ["hot", "new", "top", "rising", "controversial", "gilded"]
VALID_PERIOD_VALUES = ["day", "week", "month", "year", "all"]


def _validate_sort_period(sort: str, period: str | None, limit: int) -> None:
    """Validate sort, period, and limit parameters.

    Args:
        sort: Sort type
        period: Time period (or None)
        limit: Number of results

    Raises:
        typer.Exit: If validation fails with exit code 2
    """
    if sort not in VALID_SORT_VALUES:
        handle_validation_error("sort", VALID_SORT_VALUES, sort)

    if period is not None and period not in VALID_PERIOD_VALUES:
        handle_validation_error("period", VALID_PERIOD_VALUES, period)

    if limit < 1 or limit > 100:
        typer.echo("Error: --limit must be between 1 and 100", err=True)
        raise typer.Exit(code=2)


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
            typer.echo(f"[{post.score}] {post.title}")
            typer.echo(f"  ID: {post.id}")
            typer.echo(f"  r/{post.subreddit} by {post.author}")
            typer.echo(f"  {post.num_comments} comments")
            typer.echo()

        if after_cursor or before_cursor:
            typer.echo("---")
            if after_cursor:
                typer.echo(f"After: {after_cursor}")
            if before_cursor:
                typer.echo(f"Before: {before_cursor}")


async def _sticky_async(subreddit: str) -> None:
    """Async implementation of sticky."""
    async with RedditClient() as client:
        posts_client = PostsClient(client)
        post = await posts_client.get_sticky(subreddit)
        typer.echo(f"[{post.score}] {post.title}")
        typer.echo(f"  ID: {post.id}")
        typer.echo(f"  r/{post.subreddit} by {post.author}")
        typer.echo(f"  {post.num_comments} comments")
        typer.echo(f"  URL: {post.url}")


async def _random_async(subreddit: str) -> None:
    """Async implementation of random."""
    async with RedditClient() as client:
        posts_client = PostsClient(client)
        try:
            post = await posts_client.get_random(subreddit)
            typer.echo(f"[{post.score}] {post.title}")
            typer.echo(f"  ID: {post.id}")
            typer.echo(f"  r/{post.subreddit} by {post.author}")
            typer.echo(f"  {post.num_comments} comments")
            typer.echo(f"  URL: {post.url}")
        except ValueError as e:
            typer.echo(f"Error: {e}")


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
            typer.echo(f"No posts found matching '{query}' in r/{subreddit}")
            return

        typer.echo(f"Search results for '{query}' in r/{subreddit}:")
        typer.echo()
        for post in posts:
            typer.echo(f"[{post.score}] {post.title}")
            typer.echo(f"  ID: {post.id}")
            typer.echo(f"  r/{post.subreddit} by {post.author}")
            typer.echo(f"  {post.num_comments} comments")
            typer.echo()

        if after_cursor or before_cursor:
            typer.echo("---")
            if after_cursor:
                typer.echo(f"After: {after_cursor}")
            if before_cursor:
                typer.echo(f"Before: {before_cursor}")


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
        # Validate parameters unless using sticky or random (which don't use them)
        if not sticky and not random:
            _validate_sort_period(sort, period, limit)

        if sticky:
            asyncio.run(_sticky_async(subreddit))
        elif random:
            asyncio.run(_random_async(subreddit))
        elif search:
            asyncio.run(_search_async(subreddit, search, sort, limit, period))
        else:
            asyncio.run(_browse_async(subreddit, sort, limit, period, after, before))
    except Exception as e:
        handle_api_error(e)
