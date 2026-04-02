# Rich Integration

Typer has built-in integration with Rich for beautiful terminal output.

## Basic Output with `typer.echo()`

```python
import typer

app = typer.Typer()

@app.command()
def status():
    """Show status information."""
    typer.echo("Status: OK")
    typer.echo("Version: 1.0.0")
```

**Note:** Use `typer.echo()` instead of `print()` for proper output handling in all contexts.

## Rich-formatted Output with Tables

```python
from rich.console import Console
from rich.table import Table
import typer

app = typer.Typer()
console = Console()

@app.command()
def list_users():
    """List all users in a table."""
    table = Table(title="Users")

    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Email", style="yellow")

    table.add_row("1", "Alice", "alice@example.com")
    table.add_row("2", "Bob", "bob@example.com")
    table.add_row("3", "Charlie", "charlie@example.com")

    console.print(table)
```

## Rich Panels

```python
from rich.console import Console
from rich.panel import Panel
import typer

app = typer.Typer()
console = Console()

@app.command()
def info():
    """Show information in a panel."""
    console.print(Panel("[bold]Welcome to MyCLI[/bold]\nVersion 1.0.0", title="Info"))

@app.command()
def config_show():
    """Show configuration in a panel."""
    config_text = """
[cyan]Database:[/cyan] localhost:5432
[cyan]API Key:[/cyan] ****
[cyan]Debug:[/cyan] False
    """
    console.print(Panel(config_text, title="Configuration", border_style="green"))
```

## Styled Output with Colors

```python
from rich.console import Console
from rich.theme import Theme
import typer

app = typer.Typer()

custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
})

console = Console(theme=custom_theme)

@app.command()
def report():
    """Show a styled report."""
    console.print("Operation completed successfully", style="success")
    console.print("Warning: This feature is deprecated", style="warning")
    console.print("Error: Something went wrong", style="error")
    console.print("Info: This is informational", style="info")
```

## Rich Markup Mode

Set global markup mode for help text and output:

```python
import typer

app = typer.Typer(rich_markup_mode="markdown")

@app.command()
def create(name: str):
    """Create a **new** user account.

    This command creates a user with the given *name*.
    """
    typer.echo(f"Creating: {name}")

# Help text renders markdown formatting
```

**Available modes:**
- `"rich"` - Default Rich markup (bold, italic, colors)
- `"markdown"` - Markdown formatting
- `"none"` - No markup (plain text)

## Rich Print with Syntax Highlighting

```python
from rich.console import Console
from rich.syntax import Syntax
import typer

app = typer.Typer()
console = Console()

@app.command()
def show_code():
    """Show code with syntax highlighting."""
    code = '''
def hello(name: str) -> str:
    """Say hello."""
    return f"Hello, {name}!"

result = hello("World")
print(result)
'''
    syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
    console.print(syntax)
```

## Rich Live Display

```python
from rich.console import Console
from rich.live import Live
import typer

app = typer.Typer()
console = Console()

@app.command()
def monitor():
    """Monitor with live updates."""
    with Live("", console=console, refresh_per_second=10) as live:
        for i in range(10):
            live.update(f"[cyan]Processing...[/cyan] {i*10}%")
            import time
            time.sleep(0.5)
        live.update("[green]Complete![/green]")
```

## Error Output to stderr

```python
from rich.console import Console
import typer

app = typer.Typer()

error_console = Console(stderr=True)

@app.command()
def warn():
    """Show warning message to stderr."""
    error_console.print("[yellow]Warning: deprecated feature[/yellow]")
    typer.echo("Warning: deprecated feature", err=True)

@app.command()
def error():
    """Show error message to stderr."""
    error_console.print("[bold red]Error: operation failed[/bold red]")

@app.command()
def info_err():
    """Show info to stderr."""
    error_console.print("[blue]Info: background task running[/blue]")
```

## Rich Columns

```python
from rich.console import Console
from rich.columns import Columns
import typer

app = typer.Typer()
console = Console()

@app.command()
def list_features():
    """List features in columns."""
    features = [
        "[bold]Fast[/bold] - Lightning quick",
        "[bold]Safe[/bold] - Type-safe",
        "[bold]Easy[/bold] - Simple to use",
    ]
    console.print(Columns(features))
```

## typer.launch() - Open URLs and Files

```python
import typer

app = typer.Typer()

@app.command()
def docs():
    """Open documentation."""
    typer.launch("https://docs.example.com")

@app.command()
def open_config():
    """Open config file location."""
    typer.launch("/path/to/config.ini", locate=True)  # Opens containing folder

@app.command()
def browser():
    """Open URL in specific browser."""
    typer.launch("https://example.com", browser="firefox")

@app.command()
def vscode():
    """Open VSCode at a specific file."""
    typer.launch("/path/to/file.py", locate=True, app="code")
```

**launch() options:**
- `locate=True` - Open the folder containing the file instead of the file itself
- `browser` - Specify browser name or path
- `app` - Specify application to open with (e.g., "code", "idea")

## Rich Tree

```python
from rich.console import Console
from rich.tree import Tree
import typer

app = typer.Typer()
console = Console()

@app.command()
def tree():
    """Show a tree structure."""
    tree = Tree("Root")
    tree.add("Branch 1")
    tree.add("Branch 2")
    branch3 = tree.add("Branch 3")
    branch3.add("Leaf 3.1")
    branch3.add("Leaf 3.2")

    console.print(tree)
```

## Rich Progress with Rich

```python
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
import typer

app = typer.Typer()
console = Console()

@app.command()
def process():
    """Process with Rich progress bar."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task("Processing...", total=100)
        for i in range(100):
            progress.update(task, advance=1)
            import time
            time.sleep(0.02)
```

## Console with Different Width

```python
from rich.console import Console
import typer

app = typer.Typer()

@app.command()
def wide_output():
    """Show output with custom console width."""
    console = Console(width=120)

    for i in range(5):
        console.print(f"Item {i}: " + "x" * 80)
```

## Key Points

- Use `typer.echo()` instead of `print()` for proper output handling
- Rich tables, panels, and trees create beautiful terminal output
- `Console(stderr=True)` sends output to stderr
- `typer.launch()` opens URLs and files in external applications
- `rich_markup_mode` enables markdown or Rich markup in help text
- Rich markup: `[bold]text[/bold]`, `[cyan]text[/cyan]`, etc.
- Available styles: bold, italic, cyan, green, yellow, red, etc.
- Use `console.print()` for Rich objects, `typer.echo()` for plain text
