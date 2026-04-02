from reddit_cli.reddit.base import RedditClient
from reddit_cli.reddit.models import Subreddit


class SubredditsClient:
    """Client for Reddit subreddit endpoints."""

    def __init__(self, client: RedditClient) -> None:
        self._client = client

    async def get_subreddit(self, name: str) -> Subreddit:
        """Get subreddit info.

        Args:
            name: Subreddit name (with or without r/ prefix)
        """
        if name.startswith("r/"):
            name = name[2:]

        data = await self._client.get(f"/r/{name}/about.json")
        return Subreddit(**data["data"])

    async def get_rules(self, name: str) -> dict:
        """Get subreddit rules.

        Args:
            name: Subreddit name (with or without r/ prefix)
        """
        if name.startswith("r/"):
            name = name[2:]

        data = await self._client.get(f"/r/{name}/about/rules.json")
        return data

    async def get_moderators(self, name: str) -> list[dict]:
        """Get subreddit moderators.

        Args:
            name: Subreddit name (with or without r/ prefix)
        """
        if name.startswith("r/"):
            name = name[2:]

        data = await self._client.get(f"/r/{name}/about/moderators.json")
        return data["data"]["children"]

    async def list_subreddits(
        self,
        sort: str = "subscribers",
        limit: int = 25,
    ) -> list[Subreddit]:
        """List popular subreddits.

        Args:
            sort: Sort type (subscribers, active)
            limit: Number of subreddits to return
        """
        path = "/subreddits.json"
        params: dict[str, int | str] = {"limit": limit, "sort": sort}

        data = await self._client.get(path, params=params)
        subreddits = data.get("data", {}).get("children", [])
        return [Subreddit(**sub["data"]) for sub in subreddits]

    async def search_subreddits(
        self,
        query: str,
        limit: int = 10,
        include_over_18: bool = False,
    ) -> list[Subreddit]:
        """Search subreddits by keyword.

        Args:
            query: Search query
            limit: Number of results (max 25)
            include_over_18: Include NSFW subreddits
        """
        params: dict[str, int | str | bool] = {
            "query": query,
            "limit": min(limit, 25),
            "include_over_18": include_over_18,
        }

        data = await self._client.get("/api/subreddit_autocomplete_v2", params=params)
        subreddits = data.get("subreddits", [])
        return [Subreddit(**sub) for sub in subreddits]
