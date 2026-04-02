# typer.secho() and typer.style()

These shorthand functions avoid importing Rich directly.

## typer.secho() - Styled Echo

`scho` is equivalent to `echo` with Rich formatting:

```python
# secho - styled echo (equivalent to typer.echo with rich formatting)
typer.secho("Error: file not found", fg="red", err=True)
typer.secho("Warning: low memory", fg="yellow", err=True)
typer.secho("Success!", fg="green")

# Combining with Rich markup
typer.secho("[bold]Alert![/bold] Something went wrong", fg="red", err=True)
```

## typer.style() - Create Styled Strings

Create styled strings for use in f-strings or concatenation:

```python
# style() - create styled strings for f-strings
text = f"Error: {typer.style('Invalid input', fg='red', bold=True)}"
typer.echo(text)

# Combining styles
typer.secho(
    f"Processing: {typer.style('complete', fg='green')}",
    err=True
)
```

## Color Options

```python
# Foreground colors (fg)
typer.secho("Red text", fg="red")
typer.secho("Green text", fg="green")
typer.secho("Yellow text", fg="yellow")
typer.secho("Blue text", fg="blue")
typer.secho("Magenta text", fg="magenta")
typer.secho("Cyan text", fg="cyan")
typer.secho("White text", fg="white")
typer.secho("Black text", fg="black")

# Bold
typer.secho("Bold text", bold=True)

# Italic
typer.secho("Italic text", italic=True)

# Underline
typer.secho("Underlined text", underline=True)

# Strikethrough
typer.secho("Strikethrough text", strikethrough=True)
```

## Common Patterns

```python
# Error message
typer.secho("Error: something went wrong", fg="red", err=True)

# Warning message
typer.secho("Warning: deprecated feature", fg="yellow", err=True)

# Success message
typer.secho("Success: operation completed", fg="green")

# Info message
typer.secho("Info: processing file", fg="blue")

# Bold error
typer.secho("Error: file not found", fg="red", bold=True, err=True)

# Combining multiple styles
typer.secho("Critical error", fg="red", bold=True, underline=True, err=True)
```

## Rich Markup in secho

```python
# Using Rich markup tags
typer.secho("[bold red]Error![/bold red] File not found", err=True)
typer.secho("[yellow]Warning:[/yellow] Low memory", err=True)
typer.secho("[green]Success![/green] Operation complete")

# Nested markup
typer.secho("[bold]Status: [green]OK[/green][/bold]")
```

## Background Colors

```python
# Background colors (bg)
typer.secho("Text with red background", bg="red")
typer.secho("Text with yellow background", bg="yellow")
typer.secho("White text on red background", fg="white", bg="red")
```

## Complete Example

```python
import typer

app = typer.Typer()

@app.command()
def process_file(filename: str):
    typer.secho(f"Processing: {filename}", fg="blue")

    # Validate file exists
    import os
    if not os.path.exists(filename):
        typer.secho(f"Error: File '{filename}' not found", fg="red", err=True)
        raise typer.Exit(code=2)

    # Do work...
    typer.secho("Success: File processed", fg="green")
```

See also:
- [rich-errors.md](rich-errors.md) - For Rich Panel and Table formatting
- [logging.md](logging.md) - For logging integration
