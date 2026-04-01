import asyncio
import sys
import typer

from reddit_cli.reddit import RedditClient, SubredditsClient

app = typer.Typer()


async def _subreddit_async(
    name: str,
    rules: bool = False,
    moderators: bool = False,
) -> None:
    """Async implementation of subreddit."""
    async with RedditClient() as client:
        subreddits_client = SubredditsClient(client)

        if rules:
            data = await subreddits_client.get_rules(name)
            print(f"Rules for r/{name}:")
            for i, rule in enumerate(data.get("rules", []), 1):
                print(f"  {i}. {rule.get('short_name', 'N/A')}")
                print(f"     {rule.get('description', 'N/A')[:100]}...")
        elif moderators:
            try:
                data = await subreddits_client.get_moderators(name)
                print(f"Moderators of r/{name}:")
                for mod in data:
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


@app.command()
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


@app.command(name="subreddits")
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
