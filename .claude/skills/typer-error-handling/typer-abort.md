# typer.Abort()

`typer.Abort()` is equivalent to `typer.Exit(code=1)` and is used for fatal errors that should stop execution immediately.

## Basic Usage

```python
import typer

app = typer.Typer()

@app.command()
def delete_user(name: str):
    if not user_exists(name):
        typer.echo(f"Error: User '{name}' not found", err=True)
        raise typer.Abort()
    typer.echo(f"Deleted: {name}")
```

## Critical: Abort Does NOT Accept Custom Message

**Important:** `typer.Abort()` does NOT accept a custom message. Typer always displays "Aborted!" when using `raise typer.Abort()`:

```python
# WRONG - Message will NOT be displayed
raise typer.Abort("Custom error message")  # Raises TypeError!

# CORRECT - Shows "Aborted!" (no custom message)
raise typer.Abort()
```

If you need a custom message, use `typer.echo()` before raising Abort:

```python
# Good - Custom message then abort
@app.command()
def delete_user(name: str):
    if not user_exists(name):
        typer.echo(f"Error: User '{name}' not found", err=True)
        raise typer.Abort()  # Will only show "Aborted!"
```

Or better, use `typer.Exit()` with a custom message:

```python
# Better - Custom message with Exit
@app.command()
def delete_user(name: str):
    if not user_exists(name):
        raise typer.Exit(f"Error: User '{name}' not found", code=1, err=True)
```

## Exit vs Abort vs SystemExit

```python
# typer.Exit() - explicit exits
raise typer.Exit()  # Silent, code 0
raise typer.Exit(code=1)  # Shows nothing, code 1
raise typer.Exit("Message", code=1)  # Shows message, code 1
raise typer.Exit("Error", code=2, err=True)  # To stderr

# typer.Abort() - "Aborted!" + exit code 1
raise typer.Abort()  # Shows "Aborted!", code 1
# Abort DOES NOT accept a custom message!

# SystemExit - works but LOSES Rich formatting
import sys
raise sys.exit(1)  # Basic exit, no Rich

# RECOMMENDATION:
# - For normal exit: raise typer.Exit(code=0) or return
# - For error: raise typer.Exit("msg", code=X, err=True)
# - For cancellation: typer.echo() then raise typer.Abort() or typer.Exit(code=130)
```

## When to Use Abort

- When you want to signal a fatal error
- When "Aborted!" is an acceptable message
- When you don't need a custom error message
- For user cancellation of operations

## Confirmation Prompt with Abort

```python
import typer

@app.command()
def deploy():
    """Deploy the application."""
    if not typer.confirm("Are you sure you want to deploy?"):
        typer.echo("Deployment cancelled")
        raise typer.Abort()

    typer.echo("Deploying...")
```

See also:
- [typer-exit.md](typer-exit.md) - For custom error messages
- [typer-interrupt.md](typer-interrupt.md) - For Ctrl+C handling
