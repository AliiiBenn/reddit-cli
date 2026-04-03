"""Rich UI helper functions for enhanced CLI output."""
from typing import Any

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

# Console instance for stderr output (user-facing messages)
console = Console(stderr=True)


def print_table(data: list[dict[str, Any]], columns: list[str]) -> None:
    """Print data as a Rich table.

    Args:
        data: List of dictionaries containing row data
        columns: List of column names/headers
    """
    if not data:
        console.print("[dim]No data to display[/dim]")
        return

    table = Table(show_header=True, header_style="bold cyan")

    for col in columns:
        table.add_column(col)

    for row in data:
        table.add_row(*[str(row.get(col, "")) for col in columns])

    console.print(table)


def print_posts(posts: list) -> None:
    """Pretty print post listings with colored scores.

    Args:
        posts: List of Post objects with attributes: title, score, id,
               subreddit, author, num_comments
    """
    if not posts:
        console.print("[dim]No posts found[/dim]")
        return

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Score", style="yellow", justify="right")
    table.add_column("Title", style="white")
    table.add_column("Subreddit", style="cyan")
    table.add_column("Author", style="green")
    table.add_column("Comments", style="magenta", justify="right")

    for post in posts:
        # Color score based on value
        score_str = f"{post.score:,}"
        if post.score >= 10000:
            score_str = f"[yellow]{score_str}[/yellow]"
        elif post.score >= 1000:
            score_str = f"[cyan]{score_str}[/cyan]"

        table.add_row(
            score_str,
            post.title[:60] + "..." if len(post.title) > 60 else post.title,
            f"r/{post.subreddit}",
            post.author,
            str(post.num_comments),
        )

    console.print(table)


def print_comments(comments: list, indent: int = 0) -> None:
    """Print comments with indentation.

    Args:
        comments: List of Comment objects with attributes: body, score,
                  author, replies, id
        indent: Current indentation level (for recursion)
    """
    for comment in comments:
        prefix = "  " * indent

        # Comment header with score and author
        console.print(
            f"{prefix}[yellow]{comment.score:>4}[/yellow] [bold green]{comment.author}[/bold green]"
        )

        # Comment body (truncated if too long)
        body = comment.body
        if len(body) > 200:
            body = body[:200] + "..."

        console.print(f"{prefix}[dim]{body}[/dim]")
        console.print()

        # Recursively print replies
        if comment.replies:
            print_comments(comment.replies, indent + 1)


def print_progress(message: str) -> Progress:
    """Show progress during loading.

    Args:
        message: Progress message to display

    Returns:
        Progress context manager
    """
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    )
