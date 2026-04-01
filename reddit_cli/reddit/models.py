from pydantic import BaseModel, Field


class Post(BaseModel):
    """Reddit post model."""

    id: str
    title: str
    author: str
    subreddit: str
    score: int
    num_comments: int
    permalink: str
    url: str
    created_utc: float
    selftext: str = ""

    @property
    def short_id(self) -> str:
        """Return the post short ID (without prefix)."""
        return self.id


class Subreddit(BaseModel):
    """Subreddit model."""

    id: str
    display_name: str
    title: str
    description: str
    subscribers: int
    active_users: int = Field(default=0, validation_alias="accounts_active")


class Comment(BaseModel):
    """Reddit comment model."""

    id: str
    author: str
    body: str
    score: int
    created_utc: float
    parent_id: str
    link_id: str
    depth: int = 0
    replies: list["Comment"] = []

    @property
    def short_id(self) -> str:
        """Return the comment short ID (without prefix)."""
        return self.id
