# TyperInterrupt (Ctrl+C Handling)

`TyperInterrupt` is raised when the user presses Ctrl+C. It produces exit code 130 (128 + SIGINT=2).

## Basic Handling

```python
from typer import TyperInterrupt, echo

app = typer.Typer()

@app.callback()
def main():
    pass

@app.command()
def long_task():
    """Task that can be interrupted."""
    try:
        # Long-running work
        import time
        time.sleep(60)
    except TyperInterrupt:
        # Handle Ctrl+C
        echo("Cancelled by user", err=True)
        raise TyperInterrupt()  # Re-raise for exit code 130!
```

## Exit Code 130

The exit code 130 is calculated as `128 + SIGINT(2)`:

```
128 + 2 = 130
```

This is the standard convention for shell scripts to detect Ctrl+C interruption.

## KeyboardInterrupt vs TyperInterrupt

`KeyboardInterrupt` inherits from `BaseException`, not `Exception`. This means a regular `except Exception` will NOT catch it:

```python
# This will NOT catch KeyboardInterrupt
try:
    risky()
except Exception:
    pass  # KeyboardInterrupt passes through!

# This WILL catch KeyboardInterrupt
try:
    risky()
except KeyboardInterrupt:
    pass  # Caught!
```

## Complete Ctrl+C Handling Pattern

```python
from typer import TyperInterrupt, echo
import typer

app = typer.Typer()

@app.command()
def long_task():
    """Task that can be interrupted."""
    try:
        # Work that can be interrupted
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

## Main Entry Point Handling

```python
if __name__ == "__main__":
    try:
        app()
    except (KeyboardInterrupt, TyperInterrupt):
        typer.echo("\nInterrupted", err=True)
        raise SystemExit(130) from None
```

## Testing Interrupt Handling

```python
from typer.testing import CliRunner

runner = CliRunner()

def test_user_interrupt():
    result = runner.invoke(app, [], input="\x03")  # Ctrl+C
    assert result.exit_code == 130

def test_keyboard_interrupt():
    result = runner.invoke(app, ["long-task"], input="\x03")
    assert result.exit_code == 130
    assert "Interrupted" in result.output
```

## Best Practices

1. **Always re-raise TyperInterrupt** after catching to ensure proper exit code
2. **Use `except KeyboardInterrupt`** at the top level to catch both
3. **Perform cleanup in finally blocks** to ensure resources are released
4. **Provide user feedback** when interruption occurs

See also:
- [typer-abort.md](typer-abort.md) - For general abort patterns
- [context-managers.md](context-managers.md) - For resource cleanup
