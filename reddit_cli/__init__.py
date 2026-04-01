import asyncio
import typer

from reddit_cli.commands.browse import browse
from reddit_cli.commands.comments import comment, comments
from reddit_cli.commands.navigation import best, frontpage, home
from reddit_cli.commands.post import post, view
from reddit_cli.commands.subreddit import subreddit, subreddits
from reddit_cli.reddit import RedditClient, PostsClient

app = typer.Typer(invoke_without_command=True)
app.command()(browse)
app.command()(post)
app.command()(view)
app.command()(comments)
app.command()(comment)
app.command()(subreddit)
app.command()(subreddits)
app.command()(frontpage)
app.command()(home)
app.command()(best)


@app.callback()
def main() -> None:
    """Browse the frontpage by default."""
    asyncio.run(_frontpage_default())


async def _frontpage_default() -> None:
    """Default: show frontpage."""
    async with RedditClient() as client:
        posts_client = PostsClient(client)
        posts, after_cursor, before_cursor = await posts_client.list_posts("reddit", "hot", 25, None)

        for post in posts:
            print(f"[{post.score}] {post.title}")
            print(f"  ID: {post.id}")
            print(f"  r/{post.subreddit} by {post.author}")
            print(f"  {post.num_comments} comments")
            print()


@app.command()
def ping() -> str:
    """Ping the CLI."""
    return "pong"
