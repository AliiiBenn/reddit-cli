import asyncio
import typer

from reddit_cli.reddit import RedditClient, PostsClient

browse_app = typer.Typer()


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


@browse_app.callback(invoke_without_command=True)
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


@browse_app.command(name="sticky")
def sticky(
    subreddit: str,
) -> None:
    """Get the sticky post from a subreddit.

    Args:
        subreddit: Subreddit name (without r/)
    """
    asyncio.run(_sticky_async(subreddit))


async def _sticky_async(subreddit: str) -> None:
    """Async implementation of sticky."""
    async with RedditClient() as client:
        posts_client = PostsClient(client)
        post = await posts_client.get_sticky(subreddit)
        print(f"[{post.score}] {post.title}")
        print(f"  ID: {post.id}")
        print(f"  r/{post.subreddit} by {post.author}")
        print(f"  {post.num_comments} comments")
        print(f"  URL: {post.url}")


@browse_app.command(name="random")
def random(
    subreddit: str,
) -> None:
    """Get a random post from a subreddit.

    Args:
        subreddit: Subreddit name (without r/)
    """
    asyncio.run(_random_async(subreddit))


async def _random_async(subreddit: str) -> None:
    """Async implementation of random."""
    async with RedditClient() as client:
        posts_client = PostsClient(client)
        try:
            post = await posts_client.get_random(subreddit)
            print(f"[{post.score}] {post.title}")
            print(f"  ID: {post.id}")
            print(f"  r/{post.subreddit} by {post.author}")
            print(f"  {post.num_comments} comments")
            print(f"  URL: {post.url}")
        except ValueError as e:
            print(f"Error: {e}")


@browse_app.command(name="search")
def browse_search(
    subreddit: str,
    query: str,
    sort: str = "relevance",
    limit: int = 25,
    period: str | None = None,
) -> None:
    """Search within a subreddit.

    Args:
        subreddit: Subreddit name (without r/)
        query: Search query
        sort: Sort type (relevance, hot, top, new, comments)
        limit: Number of results
        period: Time period (day, week, month, year, all)
    """
    asyncio.run(_browse_search_async(subreddit, query, sort, limit, period))


async def _browse_search_async(
    subreddit: str,
    query: str,
    sort: str = "relevance",
    limit: int = 25,
    period: str | None = None,
) -> None:
    """Async implementation of subreddit search."""
    async with RedditClient() as client:
        posts_client = PostsClient(client)
        posts, after_cursor, before_cursor = await posts_client.search_posts(
            query, subreddit, sort, limit, period
        )

        if not posts:
            print(f"No posts found matching '{query}' in r/{subreddit}")
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
