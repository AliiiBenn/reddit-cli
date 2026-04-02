import typer

from reddit_cli.commands.browse import browse
from reddit_cli.commands.comments import comment, comments
from reddit_cli.commands.navigation import best, frontpage, home
from reddit_cli.commands.post import post
from reddit_cli.commands.search import search
from reddit_cli.commands.subreddit import subreddit, subreddits


def show_help() -> None:
    """Show custom help text."""
    typer.echo(HELP_TEXT)


HELP_TEXT = """
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

    reddit browse <subreddit> --sticky     Get sticky post
    reddit browse <subreddit> --random     Get random post
    reddit browse <subreddit> --search <q> Search within subreddit
        --sort relevance|hot|top|new|comments
        --period day|week|month|year|all

SEARCH
    reddit search <query>                 Search posts globally
        --sort relevance|hot|top|new|comments
        --period day|week|month|year|all
        --limit <n>

POSTS
    reddit post view <post_id>            View a post with details
    reddit post duplicates <post_id>      Get crossposts of a post
    reddit post info <post_id>            Get post info

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

    reddit subreddits --search <query>  Search subreddits by keyword
        --limit <n>               Number of results (max 25)

    reddit subreddits --new            List newly created subreddits
    reddit subreddits --gold            List Reddit Gold subreddits
    reddit subreddits --default         List default subreddits

EXAMPLES
    reddit frontpage
    reddit browse python --sort hot --limit 10
    reddit browse python --sticky
    reddit browse python --random
    reddit browse python --search javascript --limit 20
    reddit search programming --sort top --period month
    reddit post t3_abc123 --duplicates
    reddit comments t3_abc123 --sort top --depth 3
    reddit subreddit python --rules
    reddit subreddits --sort subscribers
    reddit subreddits --search python --limit 10
    reddit subreddits --new

For more information: https://github.com/AliiiBenn/reddit-cli
"""


app = typer.Typer()
app.command()(browse)
app.command()(post)
app.command()(subreddit)
app.command()(subreddits)
app.command()(comments)
app.command()(comment)
app.command()(frontpage)
app.command()(home)
app.command()(best)
app.command()(search)


@app.command()
def ping() -> None:
    """Ping the CLI."""
    typer.echo("pong")


@app.command(name="help")
def help_cmd() -> None:
    """Show this help message with all available commands."""
    typer.echo(HELP_TEXT)


@app.callback(invoke_without_command=True)
def main_callback(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        show_help()
        raise typer.Exit()


if __name__ == "__main__":
    app()
