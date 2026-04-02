# Exit Codes

Exit codes indicate success (0) or failure (non-zero).

## Successful Exit

```python
import typer

app = typer.Typer()

@app.command()
def create(name: str):
    """Create a resource. Exits with code 0 on success."""
    print(f"Created: {name}")
    raise typer.Exit(code=0)
```

## Error Exit with `typer.Exit()`

```python
import typer

app = typer.Typer()

@app.command()
def delete(name: str, force: bool = False):
    """Delete a resource."""
    if not force:
        print("Use --force to confirm deletion")
        raise typer.Exit(code=1)
    print(f"Deleted: {name}")
```

## Exit to stderr

```python
import typer

app = typer.Typer()

@app.command()
def fail():
    """Exit with error message to stderr."""
    raise typer.Exit("Error: something went wrong", code=1, err=True)

@app.command()
def warn():
    """Exit with warning to stderr."""
    raise typer.Exit("Warning: deprecated feature", code=0, err=True)
```

## Abort Exit with `typer.Abort()`

Use `Abort()` for unexpected errors that should halt execution:

```python
import typer

app = typer.Typer()

@app.command()
def process(filename: str):
    """Process a file."""
    if not filename.endswith(".txt"):
        typer.echo("Error: Only .txt files are supported", err=True)
        raise typer.Abort()
    print(f"Processing: {filename}")
```

## ctx.exit() - Premature Exit

Use `ctx.exit()` to exit the command early without raising an exception:

```python
import typer

app = typer.Typer()

@app.command()
def process(name: str, ctx: typer.Context):
    """Process a name with early exit capability."""
    if name == "abort":
        typer.echo("Aborting operation", err=True)
        ctx.exit(code=1)  # Exit with error code
    if name == "skip":
        typer.echo("Skipping...")
        ctx.exit(code=0)  # Exit with success
    typer.echo(f"Processing {name}")

# python main.py process abort  # Exit code 1
# python main.py process skip   # Exit code 0
```

## BadParameter with param_hint

Raise BadParameter with context about which parameter failed:

```python
from typing import Annotated
import typer

app = typer.Typer()

def validate_age(age: str, ctx: typer.Context, param: typer.Parameter):
    """Validate age parameter."""
    try:
        age_int = int(age)
    except ValueError:
        raise typer.BadParameter("Age must be a number", param_hint="age")
    if not 0 <= age_int <= 150:
        raise typer.BadParameter("Age must be between 0 and 150", param_hint="age")
    return age_int

@app.command()
def register(
    age: Annotated[int, typer.Option(callback=validate_age)],
):
    """Register a user."""
    typer.echo(f"Registering user with age: {age}")

# python main.py register --age 200
# Error: Invalid value for age: Age must be between 0 and 150
```

## TyperInterrupt for Ctrl+C

Handle keyboard interrupts gracefully:

```python
import typer

app = typer.Typer()

@app.command()
def long_task():
    """Run a task that can be interrupted."""
    try:
        import time
        typer.echo("Working... (Ctrl+C to stop)")
        time.sleep(60)
        typer.echo("Done!")
    except KeyboardInterrupt:
        typer.echo("Interrupted!", err=True)
        raise typer.TyperInterrupt()

@app.command()
def cleanup():
    """Cleanup with proper interrupt handling."""
    try:
        for i in range(10):
            typer.echo(f"Step {i}...")
            import time
            time.sleep(1)
    except typer.TyperInterrupt:
        typer.echo("Cleanup after interrupt!", err=True)
        raise
```

## Exit Code Convention

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Usage error (bad arguments) |
| 125 | Unknown option |
| 126 | Command not found (Invoke) |
| 127 | External command not found |
| 128+N | Signal N |
| 130 | Interrupted (Ctrl+C via TyperInterrupt) |

## Explicit Exit with Message

```python
import typer

app = typer.Typer()

@app.command()
def validate(name: str):
    """Validate input and exit appropriately."""
    if not name:
        typer.echo("Error: name cannot be empty", err=True)
        raise typer.Exit(code=2)  # Usage error

    if name == "invalid":
        typer.echo("Error: 'invalid' is not allowed", err=True)
        raise typer.Exit(code=1)  # General error

    typer.echo(f"Valid name: {name}")
```

## Exit in Callbacks

```python
import typer

app = typer.Typer()

__version__ = "1.0.0"

@app.callback()
def main(ctx: typer.Context, version: bool = False):
    """Main application."""
    if version:
        typer.echo(f"Version: {__version__}")
        raise typer.Exit(code=0)

@app.command()
def run():
    """Run the application."""
    typer.echo("Running...")

# python main.py --version    # Exits with code 0
# python main.py run         # Runs normally
```

## Testing Exit Codes

```python
from typer.testing import CliRunner
import typer

app = typer.Typer()

@app.command()
def delete(name: str, force: bool = False):
    """Delete a resource."""
    if not force:
        typer.echo("Use --force to confirm", err=True)
        raise typer.Exit(code=1)
    typer.echo(f"Deleted: {name}")

runner = CliRunner()

def test_delete_without_force():
    result = runner.invoke(app, ["delete", "test"])
    assert result.exit_code == 1
    assert "Use --force" in result.output

def test_delete_with_force():
    result = runner.invoke(app, ["delete", "test", "--force"])
    assert result.exit_code == 0
    assert "Deleted" in result.output
```

## Key Points

- Exit code 0 means success, non-zero means failure
- Use `typer.Exit(code=N)` for explicit exit codes
- Use `typer.Abort()` for unrecoverable errors
- Use `ctx.exit()` for early command exit without exception
- `err=True` sends output to stderr
- `param_hint` provides better error messages for parameter validation
- `TyperInterrupt` handles Ctrl+C gracefully
- Always test exit codes with `CliRunner.invoke()`
