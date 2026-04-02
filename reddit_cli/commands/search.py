import asyncio
import typer

from reddit_cli.errors import handle_api_error, handle_validation_error
from reddit_cli.reddit import RedditClient, PostsClient


# Valid values for CLI validation
VALID_SEARCH_SORT_VALUES = ["relevance", "hot", "top", "new", "comments"]
VALID_PERIOD_VALUES = ["hour", "day", "week", "month", "year", "all"]


def _validate_search_params(sort: str, period: str | None, limit: int) -> None:
    """Validate search parameters.

    Args:
        sort: Sort type
        period: Time period (or None)
        limit: Number of results

    Raises:
        typer.Exit: If validation fails with exit code 2
    """
    if sort not in VALID_SEARCH_SORT_VALUES:
        handle_validation_error("sort", VALID_SEARCH_SORT_VALUES, sort)

    if period is not None and period not in VALID_PERIOD_VALUES:
        handle_validation_error("period", VALID_PERIOD_VALUES, period)

    if limit < 1 or limit > 100:
        typer.echo("Error: --limit must be between 1 and 100", err=True)
        raise typer.Exit(code=2)


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
        _validate_search_params(sort, period, limit)
        asyncio.run(_search_async(query, sort, limit, period))
    except Exception as e:
        handle_api_error(e)


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
            typer.echo(f"No posts found matching '{query}'")
            return

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
