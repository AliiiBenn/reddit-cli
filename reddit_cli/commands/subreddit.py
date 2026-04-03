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


# =============================================================================
# Subreddits Group - Typer subcommand structure
# =============================================================================

subreddits_app = typer.Typer(invoke_without_command=True)


@subreddits_app.callback()
def subreddits_callback(
    ctx: typer.Context,
    search: str | None = typer.Option(None, "--search", help="Search subreddits by keyword"),
    new: bool = typer.Option(False, "--new", help="List newly created subreddits"),
    gold: bool = typer.Option(False, "--gold", help="List Reddit Gold subreddits"),
    default: bool = typer.Option(False, "--default", help="List default subreddits"),
    sort: str = typer.Option("subscribers", "--sort", help="Sort type (subscribers, active)"),
    limit: int = typer.Option(25, "--limit", help="Number of results"),
    format: str = typer.Option("display", "--format", help="Output format (display, sql, csv)"),
    output: str | None = typer.Option(None, "--output", help="Output file path"),
) -> None:
    """List popular subreddits.

    This command supports both the new subcommand syntax and legacy flat options:
    - reddit subreddits popular [--sort subscribers|active] [--limit N]
    - reddit subreddits search <query> [--limit N]
    - reddit subreddits new [--limit N]
    - reddit subreddits gold [--limit N]
    - reddit subreddits default [--limit N]

    Legacy syntax (still supported):
    - reddit subreddits [--sort subscribers|active] [--limit N]
    - reddit subreddits --search <query> [--limit N]
    - reddit subreddits --new [--limit N]
    - reddit subreddits --gold [--limit N]
    - reddit subreddits --default [--limit N]

    Args:
        ctx: Typer context
        search: Search subreddits by keyword (legacy option)
        new: List newly created subreddits (legacy option)
        gold: List Reddit Gold subreddits (legacy option)
        default: List default subreddits (legacy option)
        sort: Sort type
        limit: Number of results
        format: Output format
        output: Output file path
    """
    # Store options in context for subcommands to use
    ctx.obj = {
        "sort": sort,
        "limit": limit,
        "format": format,
        "output": output,
    }

    # Handle legacy flat-options syntax when no subcommand is given
    # This allows old tests to pass while supporting the new subcommand structure
    # When a subcommand is invoked, we just store options and return
    # The subcommand will handle the actual logic
    if ctx.invoked_subcommand is not None:
        # A subcommand was invoked - it will handle the logic
        return

    # No subcommand invoked - handle legacy options or default to popular
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
            # Default: list popular subreddits
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
        raise typer.Exit(code=1)


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


@subreddits_app.command(name="popular")
def subreddits_popular(
    ctx: typer.Context,
) -> None:
    """List popular subreddits.

    Args:
        ctx: Typer context with default options
    """
    try:
        opts = ctx.obj or {}
        sort = opts.get("sort", "subscribers")
        limit = opts.get("limit", 25)
        format_type = opts.get("format", "display")
        output_file = opts.get("output")

        if format_type not in VALID_FORMAT_VALUES:
            handle_validation_error("format", VALID_FORMAT_VALUES, format_type)

        _validate_list_params(sort, limit)
        subreddits_list = asyncio.run(_list_subreddits_async(sort, limit))
        if format_type == "display":
            for sub in subreddits_list:
                typer.echo(f"r/{sub.display_name}")
                typer.echo(f"  {sub.title}")
                typer.echo(f"  Subscribers: {sub.subscribers:,}")
                typer.echo()
        else:
            _write_subreddits_output(subreddits_list, format_type, output_file)
    except Exception as e:
        handle_api_error(e)


@subreddits_app.command(name="search")
def subreddits_search(
    ctx: typer.Context,
    query: str = typer.Argument(..., help="Search query"),
) -> None:
    """Search subreddits by keyword.

    Args:
        ctx: Typer context with default options
        query: Search query
    """
    try:
        opts = ctx.obj or {}
        limit = opts.get("limit", 25)
        format_type = opts.get("format", "display")
        output_file = opts.get("output")

        if format_type not in VALID_FORMAT_VALUES:
            handle_validation_error("format", VALID_FORMAT_VALUES, format_type)

        asyncio.run(_search_async(query, limit, format_type, output_file))
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


@subreddits_app.command(name="new")
def subreddits_new(
    ctx: typer.Context,
) -> None:
    """List newly created subreddits.

    Args:
        ctx: Typer context with default options
    """
    try:
        opts = ctx.obj or {}
        limit = opts.get("limit", 25)
        format_type = opts.get("format", "display")
        output_file = opts.get("output")

        if format_type not in VALID_FORMAT_VALUES:
            handle_validation_error("format", VALID_FORMAT_VALUES, format_type)

        asyncio.run(_new_async(limit, format_type, output_file))
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
            for sub in subreddits:
                typer.echo(f"r/{sub.display_name}")
                typer.echo(f"  {sub.title}")
                typer.echo(f"  Subscribers: {sub.subscribers:,}")
                typer.echo()
        else:
            _write_subreddits_output(subreddits, format, output)


@subreddits_app.command(name="gold")
def subreddits_gold(
    ctx: typer.Context,
) -> None:
    """List Reddit Gold subreddits.

    Args:
        ctx: Typer context with default options
    """
    try:
        opts = ctx.obj or {}
        limit = opts.get("limit", 25)
        format_type = opts.get("format", "display")
        output_file = opts.get("output")

        if format_type not in VALID_FORMAT_VALUES:
            handle_validation_error("format", VALID_FORMAT_VALUES, format_type)

        asyncio.run(_gold_async(limit, format_type, output_file))
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
            for sub in subreddits:
                typer.echo(f"r/{sub.display_name}")
                typer.echo(f"  {sub.title}")
                typer.echo(f"  Subscribers: {sub.subscribers:,}")
                typer.echo()
        else:
            _write_subreddits_output(subreddits, format, output)


@subreddits_app.command(name="default")
def subreddits_default(
    ctx: typer.Context,
) -> None:
    """List default subreddits.

    Args:
        ctx: Typer context with default options
    """
    try:
        opts = ctx.obj or {}
        limit = opts.get("limit", 25)
        format_type = opts.get("format", "display")
        output_file = opts.get("output")

        if format_type not in VALID_FORMAT_VALUES:
            handle_validation_error("format", VALID_FORMAT_VALUES, format_type)

        asyncio.run(_default_async(limit, format_type, output_file))
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
            for sub in subreddits:
                typer.echo(f"r/{sub.display_name}")
                typer.echo(f"  {sub.title}")
                typer.echo(f"  Subscribers: {sub.subscribers:,}")
                typer.echo()
        else:
            _write_subreddits_output(subreddits, format, output)


@subreddits_app.command(name="rules")
def subreddits_rules(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Subreddit name (with or without r/ prefix)"),
) -> None:
    """Show subreddit rules.

    Args:
        ctx: Typer context with default options
        name: Subreddit name
    """
    try:
        opts = ctx.obj or {}
        format_type = opts.get("format", "display")

        if format_type not in VALID_FORMAT_VALUES:
            handle_validation_error("format", VALID_FORMAT_VALUES, format_type)

        if format_type != "display":
            typer.echo("Rules can only be displayed in display format", err=True)
            raise typer.Exit(code=1)

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


# For backward compatibility - subreddits command with flat options
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
    """List popular subreddits (legacy flat-options command).

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
