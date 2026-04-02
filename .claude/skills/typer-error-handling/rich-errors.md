# Rich Error Formatting

Typer integrates with the Rich library for beautiful terminal output of errors.

## Basic Rich Formatting

```python
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import typer

console = Console()

@app.command()
def error_example(message: str):
    panel = Panel(
        Text(message, style="bold red"),
        title="Error",
        border_style="red"
    )
    console.print(panel)
```

## console.print_exception

For debugging, use Rich's `console.print_exception` for formatted tracebacks:

```python
from rich.console import Console
from rich.traceback import Traceback

console = Console()

@app.command()
def debug_command():
    try:
        risky()
    except Exception:
        console.print_exception(max_frames=10)  # Full Rich traceback!
        raise typer.Exit(code=1, err=True)
```

## Logging Errors to File

```python
@app.command()
def log_command():
    try:
        risky()
    except Exception:
        import traceback
        with open("error.log", "w") as f:
            traceback.print_exception(
                type(result.exception),
                result.exception,
                result.exception.__traceback__,
                file=f
            )
        typer.echo("Error logged to error.log", err=True)
        raise typer.Exit(code=1, err=True)
```

## Styled Error Messages

```python
from rich.console import Console
from rich import print as rprint

console = Console()

@app.command()
def formatted_error(status_code: int):
    error_messages = {
        400: ("Bad Request", "red"),
        401: ("Unauthorized", "yellow"),
        403: ("Forbidden", "red"),
        404: ("Not Found", "yellow"),
        500: ("Internal Server Error", "red"),
    }

    if status_code in error_messages:
        msg, color = error_messages[status_code]
        rprint(f"[{color}]Error {status_code}: [/{color}] {msg}")
    else:
        rprint(f"[red]Unknown error: {status_code}[/red]")
```

## Rich Tables for Error Context

```python
from rich.console import Console
from rich.table import Table

console = Console()

@app.command()
def show_error_context(item_id: str):
    try:
        item = lookup_item(item_id)
    except NotFoundError:
        table = Table(title="Error Context")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="red")

        table.add_row("Item ID", item_id)
        table.add_row("Status", "Not Found")
        table.add_row("Action", "Verify the item exists")

        console.print(table)
        raise typer.Exit(code=3)
```

## Good: Rich Panel for Errors

```python
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

@app.command()
def deploy(environment: str):
    valid_environments = ["dev", "staging", "production"]

    if environment not in valid_environments:
        panel = Panel(
            Text(f"Invalid environment: '{environment}'", style="red"),
            title="Deployment Error",
            subtitle=f"Valid options: {', '.join(valid_environments)}"
        )
        console.print(panel)
        raise typer.Exit(code=2)
```

## Anti-Patterns

```python
# Bad - Plain text errors lose importance
def bad_error():
    raise typer.Exit("Something went wrong", code=1)

# Good - Rich formatting conveys severity
def good_error():
    from rich.console import Console
    console = Console()
    console.print("[bold red]Error:[/bold red] Something went wrong")
    raise typer.Exit(code=1)
```

## Console for stderr

```python
from rich.console import Console

error_console = Console(stderr=True)

@app.command()
def warn():
    """Show warning message to stderr."""
    error_console.print("[yellow]Warning: deprecated feature[/yellow]")

@app.command()
def error():
    """Show error message to stderr."""
    error_console.print("[bold red]Error: operation failed[/bold red]")
```

See also:
- [secho-style.md](secho-style.md) - For typer.secho() and typer.style()
- [pretty-exceptions.md](pretty-exceptions.md) - For exception formatting
