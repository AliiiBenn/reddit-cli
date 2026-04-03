import asyncio
import typer

from reddit_cli.errors import handle_api_error, handle_validation_error
from reddit_cli.export import (
    post_to_sql_insert,
    post_to_csv_row,
    post_csv_header,
)
from reddit_cli.reddit import RedditClient, PostsClient


# Valid values for CLI validation
VALID_SORT_VALUES = ["hot", "new", "top", "rising", "controversial", "gilded"]
VALID_PERIOD_VALUES = ["day", "week", "month", "year", "all"]
VALID_FORMAT_VALUES = ["display", "sql", "csv"]


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


def _write_posts_output(
    posts: list,
    format_type: str,
    output_file: str | None,
) -> None:
    """Write posts to file or stdout in the specified format.

    Args:
        posts: List of Post objects
        format_type: Output format (display, sql, csv)
        output_file: File path or None for stdout
    """
    if format_type == "display":
        return

    lines: list[str] = []
    if format_type == "csv":
        lines.append(post_csv_header())
        for post in posts:
            lines.append(post_to_csv_row(post))
    elif format_type == "sql":
        for post in posts:
            lines.append(post_to_sql_insert(post))

    output = "\n".join(lines) + "\n"

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(output)
        typer.echo(f"Exported {len(posts)} posts to {output_file}")
    else:
        typer.echo(output)


def _display_posts(posts: list, after_cursor: str | None, before_cursor: str | None) -> None:
    """Display posts in terminal format."""
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


async def _browse_frontpage_async(
    sort: str = "hot",
    limit: int = 25,
    period: str | None = None,
    after: str | None = None,
    before: str | None = None,
) -> tuple:
    """Async implementation of frontpage browsing.

    Returns:
        Tuple of (posts, after_cursor, before_cursor)
    """
    async with RedditClient() as client:
        posts_client = PostsClient(client)
        posts, after_cursor, before_cursor = await posts_client.list_posts(
            "reddit", sort, limit, period, after, before
        )
        return posts, after_cursor, before_cursor


def frontpage(
    sort: str = "hot",
    limit: int = 25,
    period: str | None = None,
    after: str | None = None,
    before: str | None = None,
    format: str = "display",
    output: str | None = None,
) -> None:
    """Browse the frontpage.

    Args:
        sort: Sort type (hot, new, top, rising, controversial, gilded)
        limit: Number of posts to return
        period: Time period for top/controversial (day, week, month, year, all)
        after: Pagination cursor
        before: Pagination cursor
        format: Output format (display, sql, csv)
        output: Output file path
    """
    try:
        if format not in VALID_FORMAT_VALUES:
            handle_validation_error("format", VALID_FORMAT_VALUES, format)

        _validate_sort_period(sort, period, limit)
        posts, after_cursor, before_cursor = asyncio.run(
            _browse_frontpage_async(sort, limit, period, after, before)
        )

        if format == "display":
            _display_posts(posts, after_cursor, before_cursor)
        else:
            _write_posts_output(posts, format, output)
    except Exception as e:
        handle_api_error(e)


def home(
    sort: str = "hot",
    limit: int = 25,
    period: str | None = None,
    after: str | None = None,
    before: str | None = None,
    format: str = "display",
    output: str | None = None,
) -> None:
    """Alias for frontpage.

    Args:
        sort: Sort type (hot, new, top, rising, controversial, gilded)
        limit: Number of posts to return
        period: Time period for top/controversial (day, week, month, year, all)
        after: Pagination cursor
        before: Pagination cursor
        format: Output format (display, sql, csv)
        output: Output file path
    """
    try:
        if format not in VALID_FORMAT_VALUES:
            handle_validation_error("format", VALID_FORMAT_VALUES, format)

        _validate_sort_period(sort, period, limit)
        posts, after_cursor, before_cursor = asyncio.run(
            _browse_frontpage_async(sort, limit, period, after, before)
        )

        if format == "display":
            _display_posts(posts, after_cursor, before_cursor)
        else:
            _write_posts_output(posts, format, output)
    except Exception as e:
        handle_api_error(e)


def best(
    limit: int = 25,
    period: str = "all",
    after: str | None = None,
    before: str | None = None,
    format: str = "display",
    output: str | None = None,
) -> None:
    """Browse the best posts overall.

    Args:
        limit: Number of posts to return
        period: Time period (day, week, month, year, all)
        after: Pagination cursor
        before: Pagination cursor
        format: Output format (display, sql, csv)
        output: Output file path
    """
    try:
        if format not in VALID_FORMAT_VALUES:
            handle_validation_error("format", VALID_FORMAT_VALUES, format)

        _validate_sort_period("top", period, limit)
        posts, after_cursor, before_cursor = asyncio.run(
            _browse_frontpage_async("top", limit, period, after, before)
        )

        if format == "display":
            _display_posts(posts, after_cursor, before_cursor)
        else:
            _write_posts_output(posts, format, output)
    except Exception as e:
        handle_api_error(e)
