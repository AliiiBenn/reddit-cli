from reddit_cli.reddit.base import RedditClient
from reddit_cli.reddit.models import Post


class PostsClient:
    """Client for Reddit post endpoints."""

    def __init__(self, client: RedditClient) -> None:
        self._client = client

    async def list_posts(
        self,
        subreddit: str,
        sort: str = "hot",
        limit: int = 25,
        period: str | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> tuple[list[Post], str | None, str | None]:
        """List posts from a subreddit.

        Args:
            subreddit: Subreddit name (without r/)
            sort: Sort type (hot, new, top, rising, controversial, gilded)
            limit: Number of posts to return (max 100)
            period: Time period for top/controversial (day, week, month, year, all)
            after: Pagination cursor (get posts after this ID)
            before: Pagination cursor (get posts before this ID)

        Returns:
            Tuple of (posts, after_cursor, before_cursor)
        """
        path = f"/r/{subreddit}/{sort}.json"

        params: dict[str, int | str] = {"limit": limit}
        if period and sort in ("top", "controversial"):
            params["t"] = period
        if after:
            params["after"] = after
        if before:
            params["before"] = before

        data = await self._client.get(path, params=params)
        posts = data.get("data", {}).get("children", [])
        after_cursor = data.get("data", {}).get("after")
        before_cursor = data.get("data", {}).get("before")

        return [Post(**post["data"]) for post in posts], after_cursor, before_cursor

    async def get_post(self, post_id: str) -> Post:
        """Get a single post by ID.

        Args:
            post_id: Post ID (with or without t3_ prefix)
        """
        if post_id.startswith("t3_"):
            post_id = post_id[3:]

        # We need the subreddit to fetch the post, so we search by id first
        data = await self._client.get(f"/by_id/t3_{post_id}.json")
        return Post(**data["data"]["children"][0]["data"])
