import asyncio
import typer

from reddit_cli.reddit import RedditClient, PostsClient

app = typer.Typer()


async def _browse_async(
    subreddit: str,
    sort: str = "hot",
    limit: int = 25,
    period: str | None = None,
    after: str | None = None,
    before: str | None = None,
) -> None:
    """Async implementation of browse."""
    async with RedditClient() as client:
        posts_client = PostsClient(client)
        posts, after_cursor, before_cursor = await posts_client.list_posts(
            subreddit, sort, limit, period, after, before
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


@app.command()
def browse(
    subreddit: str,
    sort: str = "hot",
    limit: int = 25,
    period: str | None = None,
    after: str | None = None,
    before: str | None = None,
) -> None:
    """Browse posts from a subreddit.

    Args:
        subreddit: Subreddit name (without r/)
        sort: Sort type (hot, new, top, rising, controversial, gilded)
        limit: Number of posts to return
        period: Time period for top/controversial (day, week, month, year, all)
        after: Pagination cursor (get posts after this ID)
        before: Pagination cursor (get posts before this ID)
    """
    asyncio.run(_browse_async(subreddit, sort, limit, period, after, before))
