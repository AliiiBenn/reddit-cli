import asyncio
import sys
import typer

from reddit_cli.errors import handle_api_error, handle_validation_error
from reddit_cli.reddit import RedditClient, SubredditsClient


# Valid values for CLI validation
VALID_SUBREDDIT_SORT_VALUES = ["gilded", "subscribers", "active"]


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


async def _subreddit_async(
    name: str,
    rules: bool = False,
    moderators: bool = False,
) -> None:
    """Async implementation of subreddit."""
    try:
        async with RedditClient() as client:
            subreddits_client = SubredditsClient(client)

            if rules:
                rules_data = await subreddits_client.get_rules(name)
                typer.echo(f"Rules for r/{name}:")
                for i, rule in enumerate(rules_data.get("rules", []), 1):
                    typer.echo(f"  {i}. {rule.get('short_name', 'N/A')}")
                    typer.echo(f"     {rule.get('description', 'N/A')[:100]}...")
            elif moderators:
                try:
                    mods_data = await subreddits_client.get_moderators(name)
                    typer.echo(f"Moderators of r/{name}:")
                    for mod in mods_data:
                        typer.echo(f"  - {mod.get('name', 'N/A')}")
                except Exception:
                    typer.echo("Moderators list is not publicly available (requires authentication)")
            else:
                subreddit = await subreddits_client.get_subreddit(name)
                typer.echo(f"Subreddit: r/{subreddit.display_name}")
                typer.echo(f"Title: {subreddit.title}")
                typer.echo(f"Subscribers: {subreddit.subscribers:,}")
                typer.echo(f"Active users: {subreddit.active_users:,}")
                desc = subreddit.description.encode(
                    sys.stdout.encoding, errors="replace"
                ).decode(sys.stdout.encoding)
                typer.echo(f"Description: {desc[:300]}{'...' if len(desc) > 300 else ''}")
    except Exception as e:
        handle_api_error(e)


def subreddit(
    name: str,
    rules: bool = False,
    moderators: bool = False,
) -> None:
    """Get subreddit info.

    Args:
        name: Subreddit name (with or without r/ prefix)
        rules: Show subreddit rules
        moderators: Show subreddit moderators
    """
    try:
        asyncio.run(_subreddit_async(name, rules, moderators))
    except Exception as e:
        handle_api_error(e)


async def _list_subreddits_async(
    sort: str = "subscribers",
    limit: int = 25,
) -> None:
    """Async implementation of subreddits listing."""
    async with RedditClient() as client:
        subreddits_client = SubredditsClient(client)
        subreddits = await subreddits_client.list_subreddits(sort, limit)

        for sub in subreddits:
            typer.echo(f"r/{sub.display_name}")
            typer.echo(f"  {sub.title}")
            typer.echo(f"  Subscribers: {sub.subscribers:,}")
            typer.echo()


def subreddits(
    search: str | None = None,
    new: bool = False,
    gold: bool = False,
    default: bool = False,
    sort: str = "subscribers",
    limit: int = 25,
) -> None:
    """List popular subreddits.

    Args:
        search: Search subreddits by keyword
        new: List newly created subreddits
        gold: List Reddit Gold subreddits
        default: List default subreddits
        sort: Sort type (subscribers, active)
        limit: Number of subreddits to return
    """
    try:
        if search:
            asyncio.run(_search_async(search, limit))
        elif new:
            asyncio.run(_new_async(limit))
        elif gold:
            asyncio.run(_gold_async(limit))
        elif default:
            asyncio.run(_default_async(limit))
        else:
            _validate_list_params(sort, limit)
            asyncio.run(_list_subreddits_async(sort, limit))
    except Exception as e:
        handle_api_error(e)


async def _search_async(
    query: str,
    limit: int = 10,
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

        for sub in subreddits:
            nsfw_tag = " [NSFW]" if getattr(sub, "over_18", False) else ""
            typer.echo(f"r/{sub.display_name}{nsfw_tag}")
            typer.echo(f"  {sub.title}")
            typer.echo(f"  Subscribers: {sub.subscribers:,}")
            typer.echo()


async def _new_async(limit: int = 25) -> None:
    """Async implementation of new subreddits listing."""
    async with RedditClient() as client:
        subreddits_client = SubredditsClient(client)
        subreddits = await subreddits_client.list_new(limit)

        for sub in subreddits:
            typer.echo(f"r/{sub.display_name}")
            typer.echo(f"  {sub.title}")
            typer.echo(f"  Subscribers: {sub.subscribers:,}")
            typer.echo()


async def _gold_async(limit: int = 25) -> None:
    """Async implementation of gold subreddits listing."""
    async with RedditClient() as client:
        subreddits_client = SubredditsClient(client)
        subreddits = await subreddits_client.list_gold(limit)

        for sub in subreddits:
            typer.echo(f"r/{sub.display_name}")
            typer.echo(f"  {sub.title}")
            typer.echo(f"  Subscribers: {sub.subscribers:,}")
            typer.echo()


async def _default_async(limit: int = 25) -> None:
    """Async implementation of default subreddits listing."""
    async with RedditClient() as client:
        subreddits_client = SubredditsClient(client)
        subreddits = await subreddits_client.list_default(limit)

        for sub in subreddits:
            typer.echo(f"r/{sub.display_name}")
            typer.echo(f"  {sub.title}")
            typer.echo(f"  Subscribers: {sub.subscribers:,}")
            typer.echo()
