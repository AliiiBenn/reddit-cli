import asyncio
import typer

from reddit_cli.reddit import RedditClient, PostsClient

app = typer.Typer()


@app.command()
def search(
    query: str,
    sort: str = "relevance",
    limit: int = 25,
    period: str | None = None,
) -> None:
    """Search for posts globally across Reddit.

    Args:
        query: Search query
        sort: Sort type (relevance, hot, top, new, comments)
        limit: Number of results
        period: Time period (day, week, month, year, all)
    """
    asyncio.run(_search_async(query, sort, limit, period))


async def _search_async(
    query: str,
    sort: str = "relevance",
    limit: int = 25,
    period: str | None = None,
) -> None:
    """Async implementation of global search."""
    async with RedditClient() as client:
        posts_client = PostsClient(client)
        posts, after_cursor, before_cursor = await posts_client.search_posts(
            query, None, sort, limit, period
        )

        if not posts:
            print(f"No posts found matching '{query}'")
            return

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
