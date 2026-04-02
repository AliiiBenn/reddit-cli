import asyncio
import sys
import httpx
import typer

from reddit_cli.reddit import RedditClient, SubredditsClient

subreddit_app = typer.Typer()
subreddits_app = typer.Typer()


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
    except Exception as e:
        _handle_api_error(e)


@subreddit_app.command(name="subreddit")
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
        _handle_api_error(e)


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
            asyncio.run(_list_subreddits_async(sort, limit))
    except Exception as e:
        _handle_api_error(e)


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
            print(f"No subreddits found matching '{query}'")
            return

        for sub in subreddits:
            nsfw_tag = " [NSFW]" if getattr(sub, "over_18", False) else ""
            print(f"r/{sub.display_name}{nsfw_tag}")
            print(f"  {sub.title}")
            print(f"  Subscribers: {sub.subscribers:,}")
            print()


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


if __name__ == "__main__":
    subreddits_app()
