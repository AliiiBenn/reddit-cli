import asyncio
import typer

from reddit_cli.commands.browse import browse
from reddit_cli.commands.comments import comment, comments
from reddit_cli.commands.navigation import best, frontpage, home
from reddit_cli.commands.post import post, view
from reddit_cli.commands.subreddit import subreddit, subreddits
from reddit_cli.reddit import RedditClient, PostsClient

app = typer.Typer(invoke_without_command=True, add_help_option=False)
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
    import sys
    # Don't run frontpage if help was requested
    if len(sys.argv) > 1 and sys.argv[1] in ("help", "--help", "-h"):
        return
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


@app.command(name="help")
def help_cmd() -> None:
    """Show this help message with all available commands."""
    print("""
Reddit CLI - Browse Reddit from your terminal

USAGE
    reddit <command> [options]

NAVIGATION
    reddit                   Browse the frontpage (hot posts)
    reddit frontpage         Browse r/reddit hot posts
    reddit home              Alias for frontpage
    reddit best              Top posts of all time

BROWSE
    reddit browse <subreddit>              List posts from a subreddit
        --sort hot|new|top|rising|controversial|gilded
        --limit <n>                       Number of posts (max 100)
        --period day|week|month|year|all  Time period for top/controversial
        --after <id>                      Pagination: next page
        --before <id>                     Pagination: previous page

POSTS
    reddit view <post_id>           View a post with details
    reddit post <post_id>           Alias for view

COMMENTS
    reddit comments <post_id>       View comments for a post
        --sort confidence|top|new|old|controversial|qa
        --depth <n>                Max comment depth

    reddit comment <post_id> <comment_id>   View a single comment
        --replies                 Include nested replies

SUBREDDITS
    reddit subreddit <name>          Get subreddit info
        --rules                   Show subreddit rules
        --moderators              List moderators (if public)

    reddit subreddits               List popular subreddits
        --sort subscribers|active
        --limit <n>               Number of results

EXAMPLES
    reddit
    reddit browse python --sort hot --limit 10
    reddit view t3_abc123
    reddit comments t3_abc123 --sort top --depth 3
    reddit subreddit python --rules
    reddit subreddits --sort subscribers

For more information: https://github.com/AliiiBenn/reddit-cli
""")
