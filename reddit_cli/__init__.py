import typer

from reddit_cli.commands.browse import browse
from reddit_cli.commands.comments import comment, comments
from reddit_cli.commands.navigation import best, frontpage, home
from reddit_cli.commands.post import post, view
from reddit_cli.commands.subreddit import subreddit_app, subreddits_app

app = typer.Typer(add_help_option=False)
app.add_typer(subreddit_app, name="subreddit")
app.add_typer(subreddits_app, name="subreddits")
app.command()(browse)
app.command()(post)
app.command()(view)
app.command()(comments)
app.command()(comment)
app.command()(frontpage)
app.command()(home)
app.command()(best)


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

    reddit subreddits search <query>  Search subreddits by keyword
        --limit <n>               Number of results (max 25)
        --include-nsfw            Include NSFW subreddits

EXAMPLES
    reddit frontpage
    reddit browse python --sort hot --limit 10
    reddit view t3_abc123
    reddit comments t3_abc123 --sort top --depth 3
    reddit subreddit python --rules
    reddit subreddits --sort subscribers
    reddit subreddits search python --limit 10

For more information: https://github.com/AliiiBenn/reddit-cli
""")
