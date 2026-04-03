import asyncio
import sys
import typer

from reddit_cli.errors import handle_api_error, handle_validation_error
from reddit_cli.export import post_to_sql_insert, post_to_csv_row, post_csv_header
from reddit_cli.reddit import RedditClient, PostsClient
from reddit_cli.xlsx_export import posts_to_xlsx


VALID_FORMAT_VALUES = ["display", "sql", "csv", "xlsx"]


async def _post_async(post_id: str):
    """Async implementation of post.

    Returns:
        Post object
    """
    async with RedditClient() as client:
        posts_client = PostsClient(client)
        post = await posts_client.get_post(post_id)
        return post


def post(
    post_id: str,
    view: bool = False,
    info: bool = False,
    format: str = "display",
    output: str | None = None,
) -> None:
    """View a single post by ID.

    Args:
        post_id: Post ID (with or without t3_ prefix)
        view: Show post details
        info: Show detailed post info
        format: Output format (display, sql, csv, xlsx)
        output: Output file path
    """
    try:
        if format not in VALID_FORMAT_VALUES:
            handle_validation_error("format", VALID_FORMAT_VALUES, format)

        post_obj = asyncio.run(_post_async(post_id))

        if format == "display":
            typer.echo(f"Title: {post_obj.title}")
            typer.echo(f"Score: {post_obj.score}")
            typer.echo(f"Comments: {post_obj.num_comments}")
            typer.echo(f"Author: {post_obj.author}")
            typer.echo(f"Subreddit: r/{post_obj.subreddit}")
            typer.echo(f"URL: {post_obj.url}")
            typer.echo(f"Permalink: https://reddit.com{post_obj.permalink}")
            typer.echo()
            if post_obj.selftext:
                typer.echo(post_obj.selftext.encode(sys.stdout.encoding, errors="replace").decode(sys.stdout.encoding))
        elif format == "xlsx":
            if not output:
                typer.echo("Error: --output is required for xlsx format", err=True)
                raise typer.Exit(code=2)
            xlsx_data = posts_to_xlsx([post_obj])
            with open(output, "wb") as f:
                f.write(xlsx_data)
            typer.echo(f"Exported 1 post to {output}")
        else:
            lines = []
            if format == "csv":
                lines.append(post_csv_header())
                lines.append(post_to_csv_row(post_obj))
            elif format == "sql":
                lines.append(post_to_sql_insert(post_obj))

            output_content = "\n".join(lines) + "\n"

            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(output_content)
                typer.echo(f"Exported 1 post to {output}")
            else:
                typer.echo(output_content)
    except Exception as e:
        handle_api_error(e)
