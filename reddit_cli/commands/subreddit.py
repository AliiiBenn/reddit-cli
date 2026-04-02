import asyncio
import sys
import typer

from reddit_cli.reddit import RedditClient, SubredditsClient

subreddit_app = typer.Typer()
subreddits_app = typer.Typer()


async def _subreddit_async(
    name: str,
    rules: bool = False,
    moderators: bool = False,
) -> None:
    """Async implementation of subreddit."""
    async with RedditClient() as client:
        subreddits_client = SubredditsClient(client)

        if rules:
            rules_data = await subreddits_client.get_rules(name)
            print(f"Rules for r/{name}:")
            for i, rule in enumerate(rules_data.get("rules", []), 1):
                print(f"  {i}. {rule.get('short_name', 'N/A')}")
                print(f"     {rule.get('description', 'N/A')[:100]}...")
        elif moderators:
            try:
                mods_data = await subreddits_client.get_moderators(name)
                print(f"Moderators of r/{name}:")
                for mod in mods_data:
                    print(f"  - {mod.get('name', 'N/A')}")
            except Exception:
                print("Moderators list is not publicly available (requires authentication)")
        else:
            subreddit = await subreddits_client.get_subreddit(name)
            print(f"Subreddit: r/{subreddit.display_name}")
            print(f"Title: {subreddit.title}")
            print(f"Subscribers: {subreddit.subscribers:,}")
            print(f"Active users: {subreddit.active_users:,}")
            desc = subreddit.description.encode(
                sys.stdout.encoding, errors="replace"
            ).decode(sys.stdout.encoding)
            print(f"Description: {desc[:300]}{'...' if len(desc) > 300 else ''}")


@subreddit_app.command()
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
    asyncio.run(_subreddit_async(name, rules, moderators))


async def _list_subreddits_async(
    sort: str = "subscribers",
    limit: int = 25,
) -> None:
    """Async implementation of subreddits listing."""
    async with RedditClient() as client:
        subreddits_client = SubredditsClient(client)
        subreddits = await subreddits_client.list_subreddits(sort, limit)

        for sub in subreddits:
            print(f"r/{sub.display_name}")
            print(f"  {sub.title}")
            print(f"  Subscribers: {sub.subscribers:,}")
            print()


@subreddits_app.command(name="subreddits")
def subreddits(
    sort: str = "subscribers",
    limit: int = 25,
) -> None:
    """List popular subreddits.

    Args:
        sort: Sort type (subscribers, active)
        limit: Number of subreddits to return
    """
    asyncio.run(_list_subreddits_async(sort, limit))


@subreddits_app.command(name="search")
def search(
    query: str,
    limit: int = 10,
    include_nsfw: bool = False,
) -> None:
    """Search subreddits by keyword.

    Args:
        query: Search query
        limit: Number of results (max 25)
        include_nsfw: Include NSFW subreddits
    """
    asyncio.run(_search_async(query, limit, include_nsfw))


async def _search_async(
    query: str,
    limit: int = 10,
    include_nsfw: bool = False,
) -> None:
    """Async implementation of subreddit search."""
    async with RedditClient() as client:
        subreddits_client = SubredditsClient(client)
        subreddits = await subreddits_client.search_subreddits(
            query, limit, include_nsfw
        )

        if not subreddits:
            print(f"No subreddits found matching '{query}'")
            return

        for sub in subreddits:
            nsfw_tag = " [NSFW]" if getattr(sub, "over_18", False) else ""
            print(f"r/{sub.display_name}{nsfw_tag}")
            print(f"  {sub.title}")
            print(f"  Subscribers: {sub.subscribers:,}")
            print()


@subreddits_app.command(name="new")
def new(
    limit: int = 25,
) -> None:
    """List newly created subreddits.

    Args:
        limit: Number of subreddits to return
    """
    asyncio.run(_new_async(limit))


async def _new_async(limit: int = 25) -> None:
    """Async implementation of new subreddits listing."""
    async with RedditClient() as client:
        subreddits_client = SubredditsClient(client)
        subreddits = await subreddits_client.list_new(limit)

        for sub in subreddits:
            print(f"r/{sub.display_name}")
            print(f"  {sub.title}")
            print(f"  Subscribers: {sub.subscribers:,}")
            print()


@subreddits_app.command(name="gold")
def gold(
    limit: int = 25,
) -> None:
    """List Reddit Gold subreddits.

    Args:
        limit: Number of subreddits to return
    """
    asyncio.run(_gold_async(limit))


async def _gold_async(limit: int = 25) -> None:
    """Async implementation of gold subreddits listing."""
    async with RedditClient() as client:
        subreddits_client = SubredditsClient(client)
        subreddits = await subreddits_client.list_gold(limit)

        for sub in subreddits:
            print(f"r/{sub.display_name}")
            print(f"  {sub.title}")
            print(f"  Subscribers: {sub.subscribers:,}")
            print()


@subreddits_app.command(name="default")
def default(
    limit: int = 25,
) -> None:
    """List default subreddits.

    Args:
        limit: Number of subreddits to return
    """
    asyncio.run(_default_async(limit))


async def _default_async(limit: int = 25) -> None:
    """Async implementation of default subreddits listing."""
    async with RedditClient() as client:
        subreddits_client = SubredditsClient(client)
        subreddits = await subreddits_client.list_default(limit)

        for sub in subreddits:
            print(f"r/{sub.display_name}")
            print(f"  {sub.title}")
            print(f"  Subscribers: {sub.subscribers:,}")
            print()
