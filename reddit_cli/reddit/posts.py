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

    async def get_sticky(self, subreddit: str) -> Post:
        """Get the sticky post from a subreddit.

        Args:
            subreddit: Subreddit name (without r/)
        """
        data = await self._client.get(f"/r/{subreddit}/sticky.json")
        return Post(**data["data"]["children"][0]["data"])

    async def get_random(self, subreddit: str) -> Post:
        """Get a random post from a subreddit.

        Args:
            subreddit: Subreddit name (without r/)
        """
        data = await self._client.get(f"/r/{subreddit}/random.json")
        posts = data.get("data", {}).get("children", [])
        if posts:
            return Post(**posts[0]["data"])
        raise ValueError(f"No random post found in r/{subreddit}")

    async def get_duplicates(self, post_id: str) -> tuple[Post, list[Post]]:
        """Get all crossposts/duplicates of a post.

        Args:
            post_id: Post ID (with or without t3_ prefix)

        Returns:
            Tuple of (original_post, list of crossposts)
        """
        if post_id.startswith("t3_"):
            post_id = post_id[3:]

        data = await self._client.get(f"/api/duplicates/t3_{post_id}.json")

        # Handle list response format (Reddit API returns list for duplicates)
        if isinstance(data, list) and len(data) >= 2:
            original = [Post(**p["data"]) for p in data[0].get("data", {}).get("children", [])]
            duplicates = [Post(**p["data"]) for p in data[1].get("data", {}).get("children", [])]
            if original:
                return original[0], duplicates
            return Post(id="", title="", author="", subreddit="", score=0, num_comments=0, permalink="", url="", created_utc=0.0), []

        # Handle dict response format
        children = data.get("", data.get("data", {}))

        if isinstance(children, list) and len(children) >= 2:
            original = [Post(**p["data"]) for p in children[0].get("data", {}).get("children", [])]
            duplicates = [Post(**p["data"]) for p in children[1].get("data", {}).get("children", [])]
            if original:
                return original[0], duplicates

        # Alternative response format
        posts = data.get("data", {}).get("children", [])
        if posts:
            return posts[0], []
        return Post(id="", title="", author="", subreddit="", score=0, num_comments=0, permalink="", url="", created_utc=0.0), []

    async def search_posts(
        self,
        query: str,
        subreddit: str | None = None,
        sort: str = "relevance",
        limit: int = 25,
        period: str | None = None,
    ) -> tuple[list[Post], str | None, str | None]:
        """Search for posts.

        Args:
            query: Search query
            subreddit: Optional subreddit to search within
            sort: Sort type (relevance, hot, top, new, comments)
            limit: Number of results
            period: Time period for top (day, week, month, year, all)

        Returns:
            Tuple of (posts, after_cursor, before_cursor)
        """
        params: dict[str, int | str] = {
            "q": query,
            "limit": limit,
            "sort": sort,
            "type": "link",
        }
        if subreddit:
            params["restrict_sr"] = "on"
        if period:
            params["t"] = period

        path = "/search.json"
        if subreddit:
            path = f"/r/{subreddit}/search.json"

        data = await self._client.get(path, params=params)
        posts = data.get("data", {}).get("children", [])
        after_cursor = data.get("data", {}).get("after")
        before_cursor = data.get("data", {}).get("before")

        return [Post(**post["data"]) for post in posts], after_cursor, before_cursor
