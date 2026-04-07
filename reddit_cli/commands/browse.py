import asyncio
from pathlib import Path

import typer

from reddit_cli.commands._shared import (
    VALID_SORT_VALUES,
    VALID_PERIOD_VALUES,
    _validate_sort_period,
    _validate_format,
    validate_output_path,
)
from reddit_cli.errors import handle_api_error
from reddit_cli.export import (
    post_to_sql_insert,
    post_to_csv_row,
    post_csv_header,
    posts_to_json,
)
from reddit_cli.reddit import RedditClient, PostsClient
from reddit_cli.ui import print_posts
from reddit_cli.xlsx_export import posts_to_xlsx


# Valid values for CLI validation (includes json for browse)
VALID_FORMAT_VALUES = ["display", "sql", "csv", "xlsx", "json"]


def _write_output(
    posts: list,
    format_type: str,
    output_file: str | None,
) -> None:
    """Write posts to file or stdout in the specified format.

    Args:
        posts: List of Post objects
        format_type: Output format (display, sql, csv, xlsx)
        output_file: File path or None for stdout
    """
    if format_type == "display":
        return

    if format_type == "xlsx":
        if not output_file:
            typer.echo("Error: --output is required for xlsx format", err=True)
            raise typer.Exit(code=2)
        xlsx_data = posts_to_xlsx(posts)
        with open(output_file, "wb") as f:
            f.write(xlsx_data)
        typer.echo(f"Exported {len(posts)} posts to {output_file}")
        return

    if format_type == "json":
        output = posts_to_json(posts)
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(output)
            typer.echo(f"Exported {len(posts)} posts to {output_file}")
        else:
            typer.echo(output)
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


async def _browse_async(
    subreddit: str,
    sort: str = "hot",
    limit: int = 25,
    period: str | None = None,
    after: str | None = None,
    before: str | None = None,
) -> tuple:
    """Async implementation of browse.

    Returns:
        Tuple of (posts, after_cursor, before_cursor)
    """
    async with RedditClient() as client:
        posts_client = PostsClient(client)
        posts, after_cursor, before_cursor = await posts_client.list_posts(
            subreddit, sort, limit, period, after, before
        )
        return posts, after_cursor, before_cursor


def _display_posts(posts: list, after_cursor: str | None, before_cursor: str | None) -> None:
    """Display posts in terminal format using Rich."""
    print_posts(posts)

    if after_cursor or before_cursor:
        typer.echo("---")
        if after_cursor:
            typer.echo(f"After: {after_cursor}")
        if before_cursor:
            typer.echo(f"Before: {before_cursor}")


async def _search_async(
    subreddit: str,
    query: str,
    sort: str = "relevance",
    limit: int = 25,
    period: str | None = None,
) -> tuple:
    """Async implementation of subreddit search.

    Returns:
        Tuple of (posts, after_cursor, before_cursor)
    """
    async with RedditClient() as client:
        posts_client = PostsClient(client)
        posts, after_cursor, before_cursor = await posts_client.search_posts(
            query, subreddit, sort, limit, period
        )
        return posts, after_cursor, before_cursor


def browse(
    subreddit: str,
    search: str | None = None,
    sort: str = "hot",
    limit: int = 25,
    period: str | None = None,
    after: str | None = None,
    before: str | None = None,
    format: str = "display",
    output: str | None = None,
) -> None:
    """Browse posts from a subreddit.

    Args:
        subreddit: Subreddit name (without r/)
        search: Search within the subreddit
        sort: Sort type (hot, new, top, rising, controversial, gilded)
        limit: Number of posts to return
        period: Time period for top/controversial (day, week, month, year, all)
        after: Pagination cursor (get posts after this ID)
        before: Pagination cursor (get posts before this ID)
        format: Output format (display, sql, csv, xlsx)
        output: Output file path
    """
    try:
        _validate_sort_period(sort, period, limit, VALID_SORT_VALUES, VALID_PERIOD_VALUES)

        _validate_format(format, VALID_FORMAT_VALUES)

        # Validate output path if provided
        output_path = None
        if output:
            output_path = validate_output_path(Path(output))

        if search:
            posts, after_cursor, before_cursor = asyncio.run(
                _search_async(subreddit, search, sort, limit, period)
            )
            if not posts:
                typer.echo(f"No posts found matching '{search}' in r/{subreddit}")
                return
            if format == "display":
                typer.echo(f"Search results for '{search}' in r/{subreddit}:")
                typer.echo()
                _display_posts(posts, after_cursor, before_cursor)
            else:
                _write_output(posts, format, str(output_path) if output_path else None)
        else:
            posts, after_cursor, before_cursor = asyncio.run(
                _browse_async(subreddit, sort, limit, period, after, before)
            )
            if format == "display":
                _display_posts(posts, after_cursor, before_cursor)
            else:
                _write_output(posts, format, str(output_path) if output_path else None)
    except Exception as e:
        handle_api_error(e)
