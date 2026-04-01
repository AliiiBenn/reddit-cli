import asyncio
import typer

from reddit_cli.reddit import RedditClient, PostsClient

app = typer.Typer()


async def _browse_frontpage_async(
    sort: str = "hot",
    limit: int = 25,
    period: str | None = None,
    after: str | None = None,
    before: str | None = None,
) -> None:
    """Async implementation of frontpage browsing."""
    async with RedditClient() as client:
        posts_client = PostsClient(client)
        posts, after_cursor, before_cursor = await posts_client.list_posts(
            "reddit", sort, limit, period, after, before
        )

        for post in posts:
            print(f"[{post.score}] {post.title}")
            print(f"  ID: {post.id}")
            print(f"  r/{post.subreddit} by {post.author}")
            print(f"  {post.num_comments} comments")
            print()

        if after_cursor or before_cursor:
            print("---")
            if after_cursor:
                print(f"After: {after_cursor}")
            if before_cursor:
                print(f"Before: {before_cursor}")


@app.command(name="frontpage")
def frontpage(
    sort: str = "hot",
    limit: int = 25,
    period: str | None = None,
    after: str | None = None,
    before: str | None = None,
) -> None:
    """Browse the frontpage.

    Args:
        sort: Sort type (hot, new, top, rising, controversial, gilded)
        limit: Number of posts to return
        period: Time period for top/controversial (day, week, month, year, all)
        after: Pagination cursor
        before: Pagination cursor
    """
    asyncio.run(_browse_frontpage_async(sort, limit, period, after, before))


@app.command(name="home")
def home(
    sort: str = "hot",
    limit: int = 25,
    period: str | None = None,
    after: str | None = None,
    before: str | None = None,
) -> None:
    """Alias for frontpage.

    Args:
        sort: Sort type (hot, new, top, rising, controversial, gilded)
        limit: Number of posts to return
        period: Time period for top/controversial (day, week, month, year, all)
        after: Pagination cursor
        before: Pagination cursor
    """
    asyncio.run(_browse_frontpage_async(sort, limit, period, after, before))


@app.command(name="best")
def best(
    limit: int = 25,
    period: str = "all",
    after: str | None = None,
    before: str | None = None,
) -> None:
    """Browse the best posts overall.

    Args:
        limit: Number of posts to return
        period: Time period (day, week, month, year, all)
        after: Pagination cursor
        before: Pagination cursor
    """
    asyncio.run(_browse_frontpage_async("top", limit, period, after, before))
