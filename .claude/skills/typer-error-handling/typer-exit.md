# typer.Exit()

`typer.Exit()` terminates the application with a specific exit code.

## Basic Usage

```python
import typer

app = typer.Typer()

@app.command()
def create_user(name: str):
    if not name:
        typer.Exit("Name is required", code=1)
    typer.echo(f"User created: {name}")
```

## Parameters

- `code: int = 0` - The exit code to return
- `err: bool = False` - If True, sends output to stderr instead of stdout

## Critical: err=True for Errors

Without `err=True`, the message goes to stdout, not stderr:

```python
# WRONG - Message goes to stdout!
raise typer.Exit("Error occurred", code=1)

# CORRECT - Message goes to stderr!
raise typer.Exit("Error occurred", code=1, err=True)
```

## Exit Variations

```python
# Silent exit with code 0
raise typer.Exit()  # No message, code 0

# Exit with code 1 (implicit when err=True)
raise typer.Exit(code=1)  # Shows nothing

# Exit with message to stdout (usually wrong)
raise typer.Exit("Message", code=1)  # Goes to stdout!

# Exit with message to stderr (correct for errors)
raise typer.Exit("Error", code=2, err=True)  # Goes to stderr
```

## ctx.exit() - Premature Exit

Use `ctx.exit()` to exit the command early without raising an exception:

```python
import typer

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

## Good Patterns

```python
# Good: Explicit Exit Codes with stderr
@app.command()
def create(name: str, email: str):
    if not name:
        typer.echo("Error: Name is required", err=True)
        raise typer.Exit(code=2)

    if not email or "@" not in email:
        typer.echo("Error: Valid email is required", err=True)
        raise typer.Exit(code=2)

    user = db.create(name=name, email=email)
    typer.echo(f"Created user {user.id}")
```

## Anti-Patterns

```python
# Bad - Silent failure
@app.command()
def delete(name: str):
    if not exists(name):
        typer.echo("User not found")  # Still exits with 0!
    delete_user(name)

# Good - Proper non-zero exit code
@app.command()
def delete(name: str):
    if not exists(name):
        typer.echo("Error: User not found", err=True)
        raise typer.Exit(code=3)
    delete_user(name)
```

## When to Use typer.Exit()

- For clean exits with specific exit codes
- When you want to display a message to the user
- When `err=True` for error messages to stderr

See also:
- [typer-abort.md](typer-abort.md) - For fatal errors showing "Aborted!"
- [typer-interrupt.md](typer-interrupt.md) - For Ctrl+C handling
- [system-exit.md](system-exit.md) - Differences with SystemExit
