import asyncio
import sys
from pathlib import Path

import typer

from reddit_cli.commands._shared import (
    _validate_format,
    validate_output_path,
)
from reddit_cli.errors import handle_api_error, handle_validation_error
from reddit_cli.export import (
    subreddit_to_sql_insert,
    subreddit_to_csv_row,
    subreddit_csv_header,
)
from reddit_cli.reddit import RedditClient, SubredditsClient
from reddit_cli.ui import print_table
from reddit_cli.xlsx_export import subreddits_to_xlsx


# Valid values for CLI validation
VALID_SUBREDDIT_SORT_VALUES = ["gilded", "subscribers", "active"]
VALID_FORMAT_VALUES = ["display", "sql", "csv", "xlsx"]


def _validate_list_params(sort: str, limit: int) -> None:
    """Validate sort and limit parameters."""
    if sort not in VALID_SUBREDDIT_SORT_VALUES:
        handle_validation_error("sort", VALID_SUBREDDIT_SORT_VALUES, sort)

    if limit < 1 or limit > 100:
        typer.echo("Error: --limit must be between 1 and 100", err=True)
        raise typer.Exit(code=2)


def _write_subreddits_output(
    subreddits: list,
    format_type: str,
    output_file: str | None,
) -> None:
    """Write subreddits to file or stdout in the specified format."""
    if format_type == "display":
        return

    if format_type == "xlsx":
        if not output_file:
            typer.echo("Error: --output is required for xlsx format", err=True)
            raise typer.Exit(code=2)
        xlsx_data = subreddits_to_xlsx(subreddits)
        with open(output_file, "wb") as f:
            f.write(xlsx_data)
        typer.echo(f"Exported {len(subreddits)} subreddits to {output_file}")
        return

    lines: list[str] = []
    if format_type == "csv":
        lines.append(subreddit_csv_header())
        for sub in subreddits:
            lines.append(subreddit_to_csv_row(sub))
    elif format_type == "sql":
        for sub in subreddits:
            lines.append(subreddit_to_sql_insert(sub))

    output = "\n".join(lines) + "\n"

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(output)
        typer.echo(f"Exported {len(subreddits)} subreddits to {output_file}")
    else:
        typer.echo(output)


def _display_subreddits_table(subreddits: list, show_nsfw: bool = False) -> None:
    """Display subreddits in a table format using Rich."""
    data = [
        {
            "Name": f"r/{sub.display_name}{' [NSFW]' if show_nsfw and getattr(sub, 'over_18', False) else ''}",
            "Title": sub.title[:50] + "..." if len(sub.title) > 50 else sub.title,
            "Subscribers": f"{sub.subscribers:,}",
        }
        for sub in subreddits
    ]
    print_table(data, ["Name", "Title", "Subscribers"])


async def _subreddit_async(
    name: str,
    rules: bool = False,
) -> tuple:
    """Async implementation of subreddit.

    Returns:
        Tuple of (subreddit_object, rules_data or None)
    """
    async with RedditClient() as client:
        subreddits_client = SubredditsClient(client)

        if rules:
            rules_data = await subreddits_client.get_rules(name)
            return None, rules_data
        else:
            subreddit = await subreddits_client.get_subreddit(name)
            return subreddit, None


def subreddit(
    name: str,
    rules: bool = False,
    format: str = "display",
    output: str | None = None,
) -> None:
    """Get subreddit info.

    Args:
        name: Subreddit name (with or without r/ prefix)
        rules: Show subreddit rules
        format: Output format (display, sql, csv, xlsx)
        output: Output file path
    """
    try:
        _validate_format(format)

        # Validate output path if provided
        output_path = None
        if output:
            output_path = validate_output_path(Path(output))

        subreddit_obj, rules_data = asyncio.run(_subreddit_async(name, rules))

        if rules:
            typer.echo(f"Rules for r/{name}:")
            for i, rule in enumerate(rules_data.get("rules", []), 1):
                typer.echo(f"  {i}. {rule.get('short_name', 'N/A')}")
                typer.echo(f"     {rule.get('description', 'N/A')[:100]}...")
        else:
            if format == "display":
                typer.echo(f"Subreddit: r/{subreddit_obj.display_name}")
                typer.echo(f"Title: {subreddit_obj.title}")
                typer.echo(f"Subscribers: {subreddit_obj.subscribers:,}")
                typer.echo(f"Active users: {subreddit_obj.active_users:,}")
                desc = subreddit_obj.description.encode(
                    sys.stdout.encoding, errors="replace"
                ).decode(sys.stdout.encoding)
                typer.echo(f"Description: {desc[:300]}{'...' if len(desc) > 300 else ''}")
            else:
                _write_subreddits_output([subreddit_obj], format, str(output_path) if output_path else None)
    except Exception as e:
        handle_api_error(e)


# =============================================================================
# Subreddits Group - Typer subcommand structure
# =============================================================================

subreddits_app = typer.Typer()


async def _list_subreddits_async(
    sort: str = "subscribers",
    limit: int = 25,
) -> list:
    """Async implementation of subreddits listing."""
    async with RedditClient() as client:
        subreddits_client = SubredditsClient(client)
        subreddits = await subreddits_client.list_subreddits(sort, limit)
        return subreddits


@subreddits_app.command(name="popular")
def subreddits_popular(
    sort: str = typer.Option("subscribers", "--sort", help="Sort type (subscribers, active, gilded)"),
    limit: int = typer.Option(25, "--limit", help="Number of results"),
    format: str = typer.Option("display", "--format", help="Output format (display, sql, csv, xlsx)"),
    output: str | None = typer.Option(None, "--output", help="Output file path"),
) -> None:
    """List popular subreddits."""
    try:
        _validate_format(format)

        _validate_list_params(sort, limit)

        # Validate output path if provided
        output_path = None
        if output:
            output_path = validate_output_path(Path(output))

        subreddits_list = asyncio.run(_list_subreddits_async(sort, limit))
        if format == "display":
            _display_subreddits_table(subreddits_list)
        else:
            _write_subreddits_output(subreddits_list, format, str(output_path) if output_path else None)
    except Exception as e:
        handle_api_error(e)


async def _search_async(
    query: str,
    limit: int = 10,
    format: str = "display",
    output: str | None = None,
) -> None:
    """Async implementation of subreddit search."""
    async with RedditClient() as client:
        subreddits_client = SubredditsClient(client)
        subreddits = await subreddits_client.search_subreddits(
            query, limit, False
        )

        if not subreddits:
            typer.echo(f"No subreddits found matching '{query}'")
            return

        if format == "display":
            _display_subreddits_table(subreddits, show_nsfw=True)
        else:
            _write_subreddits_output(subreddits, format, output)


@subreddits_app.command(name="search")
def subreddits_search(
    query: str = typer.Argument(..., help="Search query"),
    limit: int = typer.Option(25, "--limit", help="Number of results"),
    format: str = typer.Option("display", "--format", help="Output format (display, sql, csv, xlsx)"),
    output: str | None = typer.Option(None, "--output", help="Output file path"),
) -> None:
    """Search subreddits by keyword."""
    try:
        _validate_format(format)

        # Validate output path if provided
        output_path = None
        if output:
            output_path = validate_output_path(Path(output))

        asyncio.run(_search_async(query, limit, format, str(output_path) if output_path else None))
    except Exception as e:
        handle_api_error(e)


async def _new_async(
    limit: int = 25,
    format: str = "display",
    output: str | None = None,
) -> None:
    """Async implementation of new subreddits listing."""
    async with RedditClient() as client:
        subreddits_client = SubredditsClient(client)
        subreddits = await subreddits_client.list_new(limit)

        if format == "display":
            _display_subreddits_table(subreddits)
        else:
            _write_subreddits_output(subreddits, format, output)


@subreddits_app.command(name="new")
def subreddits_new(
    limit: int = typer.Option(25, "--limit", help="Number of results"),
    format: str = typer.Option("display", "--format", help="Output format (display, sql, csv, xlsx)"),
    output: str | None = typer.Option(None, "--output", help="Output file path"),
) -> None:
    """List newly created subreddits."""
    try:
        _validate_format(format)

        # Validate output path if provided
        output_path = None
        if output:
            output_path = validate_output_path(Path(output))

        asyncio.run(_new_async(limit, format, str(output_path) if output_path else None))
    except Exception as e:
        handle_api_error(e)


async def _gold_async(
    limit: int = 25,
    format: str = "display",
    output: str | None = None,
) -> None:
    """Async implementation of gold subreddits listing."""
    async with RedditClient() as client:
        subreddits_client = SubredditsClient(client)
        subreddits = await subreddits_client.list_gold(limit)

        if format == "display":
            _display_subreddits_table(subreddits)
        else:
            _write_subreddits_output(subreddits, format, output)


@subreddits_app.command(name="gold")
def subreddits_gold(
    limit: int = typer.Option(25, "--limit", help="Number of results"),
    format: str = typer.Option("display", "--format", help="Output format (display, sql, csv, xlsx)"),
    output: str | None = typer.Option(None, "--output", help="Output file path"),
) -> None:
    """List Reddit Gold subreddits."""
    try:
        _validate_format(format)

        # Validate output path if provided
        output_path = None
        if output:
            output_path = validate_output_path(Path(output))

        asyncio.run(_gold_async(limit, format, str(output_path) if output_path else None))
    except Exception as e:
        handle_api_error(e)


async def _default_async(
    limit: int = 25,
    format: str = "display",
    output: str | None = None,
) -> None:
    """Async implementation of default subreddits listing."""
    async with RedditClient() as client:
        subreddits_client = SubredditsClient(client)
        subreddits = await subreddits_client.list_default(limit)

        if format == "display":
            _display_subreddits_table(subreddits)
        else:
            _write_subreddits_output(subreddits, format, output)


@subreddits_app.command(name="default")
def subreddits_default(
    limit: int = typer.Option(25, "--limit", help="Number of results"),
    format: str = typer.Option("display", "--format", help="Output format (display, sql, csv, xlsx)"),
    output: str | None = typer.Option(None, "--output", help="Output file path"),
) -> None:
    """List default subreddits."""
    try:
        _validate_format(format)

        # Validate output path if provided
        output_path = None
        if output:
            output_path = validate_output_path(Path(output))

        asyncio.run(_default_async(limit, format, str(output_path) if output_path else None))
    except Exception as e:
        handle_api_error(e)


@subreddits_app.command(name="rules")
def subreddits_rules(
    name: str = typer.Argument(..., help="Subreddit name (with or without r/ prefix)"),
) -> None:
    """Show subreddit rules."""
    try:
        asyncio.run(_rules_async(name))
    except Exception as e:
        handle_api_error(e)


async def _rules_async(name: str) -> None:
    """Async implementation of subreddit rules."""
    async with RedditClient() as client:
        subreddits_client = SubredditsClient(client)
        rules_data = await subreddits_client.get_rules(name)

        typer.echo(f"Rules for r/{name}:")
        for i, rule in enumerate(rules_data.get("rules", []), 1):
            typer.echo(f"  {i}. {rule.get('short_name', 'N/A')}")
            typer.echo(f"     {rule.get('description', 'N/A')[:100]}...")
