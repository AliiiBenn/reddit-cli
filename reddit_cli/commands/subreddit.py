import asyncio
import sys
import typer

from reddit_cli.errors import handle_api_error, handle_validation_error
from reddit_cli.export import (
    subreddit_to_sql_insert,
    subreddit_to_csv_row,
    subreddit_csv_header,
)
from reddit_cli.reddit import RedditClient, SubredditsClient


# Valid values for CLI validation
VALID_SUBREDDIT_SORT_VALUES = ["gilded", "subscribers", "active"]
VALID_FORMAT_VALUES = ["display", "sql", "csv"]


def _validate_list_params(sort: str, limit: int) -> None:
    """Validate sort and limit parameters.

    Args:
        sort: Sort type
        limit: Number of results

    Raises:
        typer.Exit: If validation fails with exit code 2
    """
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
    """Write subreddits to file or stdout in the specified format.

    Args:
        subreddits: List of Subreddit objects
        format_type: Output format (display, sql, csv)
        output_file: File path or None for stdout
    """
    if format_type == "display":
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
        format: Output format (display, sql, csv)
        output: Output file path
    """
    try:
        if format not in VALID_FORMAT_VALUES:
            handle_validation_error("format", VALID_FORMAT_VALUES, format)

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
                _write_subreddits_output([subreddit_obj], format, output)
    except Exception as e:
        handle_api_error(e)


async def _list_subreddits_async(
    sort: str = "subscribers",
    limit: int = 25,
) -> list:
    """Async implementation of subreddits listing.

    Returns:
        List of Subreddit objects
    """
    async with RedditClient() as client:
        subreddits_client = SubredditsClient(client)
        subreddits = await subreddits_client.list_subreddits(sort, limit)
        return subreddits


def subreddits(
    search: str | None = None,
    new: bool = False,
    gold: bool = False,
    default: bool = False,
    sort: str = "subscribers",
    limit: int = 25,
    format: str = "display",
    output: str | None = None,
) -> None:
    """List popular subreddits.

    Args:
        search: Search subreddits by keyword
        new: List newly created subreddits
        gold: List Reddit Gold subreddits
        default: List default subreddits
        sort: Sort type (subscribers, active)
        limit: Number of subreddits to return
        format: Output format (display, sql, csv)
        output: Output file path
    """
    try:
        if format not in VALID_FORMAT_VALUES:
            handle_validation_error("format", VALID_FORMAT_VALUES, format)

        if search:
            asyncio.run(_search_async(search, limit, format, output))
        elif new:
            asyncio.run(_new_async(limit, format, output))
        elif gold:
            asyncio.run(_gold_async(limit, format, output))
        elif default:
            asyncio.run(_default_async(limit, format, output))
        else:
            _validate_list_params(sort, limit)
            subreddits_list = asyncio.run(_list_subreddits_async(sort, limit))
            if format == "display":
                for sub in subreddits_list:
                    typer.echo(f"r/{sub.display_name}")
                    typer.echo(f"  {sub.title}")
                    typer.echo(f"  Subscribers: {sub.subscribers:,}")
                    typer.echo()
            else:
                _write_subreddits_output(subreddits_list, format, output)
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
            for sub in subreddits:
                nsfw_tag = " [NSFW]" if getattr(sub, "over_18", False) else ""
                typer.echo(f"r/{sub.display_name}{nsfw_tag}")
                typer.echo(f"  {sub.title}")
                typer.echo(f"  Subscribers: {sub.subscribers:,}")
                typer.echo()
        else:
            _write_subreddits_output(subreddits, format, output)


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
            for sub in subreddits:
                typer.echo(f"r/{sub.display_name}")
                typer.echo(f"  {sub.title}")
                typer.echo(f"  Subscribers: {sub.subscribers:,}")
                typer.echo()
        else:
            _write_subreddits_output(subreddits, format, output)


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
            for sub in subreddits:
                typer.echo(f"r/{sub.display_name}")
                typer.echo(f"  {sub.title}")
                typer.echo(f"  Subscribers: {sub.subscribers:,}")
                typer.echo()
        else:
            _write_subreddits_output(subreddits, format, output)


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
            for sub in subreddits:
                typer.echo(f"r/{sub.display_name}")
                typer.echo(f"  {sub.title}")
                typer.echo(f"  Subscribers: {sub.subscribers:,}")
                typer.echo()
        else:
            _write_subreddits_output(subreddits, format, output)
