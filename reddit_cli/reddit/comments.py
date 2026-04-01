from reddit_cli.reddit.base import RedditClient
from reddit_cli.reddit.models import Comment


class CommentsClient:
    """Client for Reddit comment endpoints."""

    def __init__(self, client: RedditClient) -> None:
        self._client = client

    async def get_comments(
        self,
        post_id: str,
        sort: str = "confidence",
        depth: int | None = None,
    ) -> list[Comment]:
        """Get comments for a post.

        Args:
            post_id: Post ID (with or without t3_ prefix)
            sort: Sort type (confidence, top, new, old, controversial, qa)
            depth: Maximum comment depth (None for unlimited)
        """
        if post_id.startswith("t3_"):
            post_id = post_id[3:]

        path = f"/comments/{post_id}.json"
        params = f"?sort={sort}"

        data = await self._client.get(path + params)
        comments_data = data[1]["data"]["children"]

        comments = []
        for item in comments_data:
            if item["kind"] == "t1":  # Comment
                comment = self._parse_comment(item["data"], depth or 999, 0)
                comments.append(comment)

        return comments

    def _parse_comment(
        self, data: dict, max_depth: int, current_depth: int
    ) -> Comment:
        """Parse a comment and its replies recursively."""
        replies: list[Comment] = []

        if data.get("replies") and isinstance(data["replies"], dict):
            for reply in data["replies"]["data"]["children"]:
                if reply["kind"] == "t1" and current_depth < max_depth:
                    replies.append(
                        self._parse_comment(
                            reply["data"], max_depth, current_depth + 1
                        )
                    )

        return Comment(
            id=data["id"],
            author=data["author"],
            body=data["body"],
            score=data["score"],
            created_utc=data["created_utc"],
            parent_id=data["parent_id"],
            link_id=data["link_id"],
            depth=current_depth,
            replies=replies,
        )

    async def get_comment(self, comment_id: str) -> Comment:
        """Get a single comment by ID.

        Args:
            comment_id: Comment ID (with or without t1_ prefix)
        """
        if comment_id.startswith("t1_"):
            comment_id = comment_id[3:]

        data = await self._client.get(f"/by_id/t1_{comment_id}.json")
        # Response is a list with [0] = post, [1] = comments
        # The comment itself is nested in the listing
        comment_data = data[1]["data"]["children"][0]["data"]
        return self._parse_comment(comment_data, 0, 0)
