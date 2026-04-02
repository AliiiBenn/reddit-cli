# Context Managers for Resource Cleanup

Use context managers to ensure resources are cleaned up properly.

## Pattern 1: Context Manager (Recommended)

```python
@app.command()
def process(input: Path):
    with open(input) as f:  # Automatically closes even if exception
        data = f.read()
    typer.echo(f"Processed {len(data)} bytes")
```

## Pattern 2: try/finally for Non-Context-Managers

```python
@app.command()
def safe_create(name: str):
    resource = acquire_resource()
    try:
        do_work(resource)
    finally:
        release_resource(resource)  # Always executes

# Or with multiple resources
@app.command()
def copy_files(source: Path, dest: Path):
    src = None
    dst = None
    try:
        src = open(source)
        dst = open(dest, 'w')
        # Copy data...
    finally:
        if src:
            src.close()
        if dst:
            dst.close()
```

## Pattern 3: Better with Context Managers

```python
import contextlib

@app.command()
def copy_files(source: Path, dest: Path):
    with contextlib.ExitStack() as stack:
        src = stack.enter_context(open(source))
        dst = stack.enter_context(open(dest, 'w'))
        # Copy data...
```

## Anti-Pattern: Exit in finally

**NEVER do this:**

```python
@app.command()
def bad_pattern():
    try:
        risky()
    finally:
        cleanup()
        # BAD: raise typer.Exit(code=1) here!
        # The finally executes but the exit code may be lost
```

## Cleanup with TyperInterrupt

```python
@app.command()
def cleanup_task():
    """Task with proper cleanup on interrupt."""
    resource = None
    try:
        resource = acquire_resource()
        # Do work...
    except KeyboardInterrupt:
        typer.echo("Interrupted!", err=True)
        raise typer.TyperInterrupt()
    finally:
        if resource:
            release_resource(resource)
```

## Combining Logging and Cleanup

```python
import logging

logger = logging.getLogger(__name__)

@app.command()
def safe_operation(path: Path):
    resource = None
    try:
        resource = acquire_resource()
        do_work(resource)
    except FileNotFoundError:
        logger.error(f"File not found: {path}")
        typer.echo(f"Error: File '{path}' not found", err=True)
        raise typer.Exit(code=2)
    except PermissionError:
        logger.error(f"Permission denied: {path}")
        typer.echo(f"Error: Permission denied for '{path}'", err=True)
        raise typer.Exit(code=2)
    except Exception as e:
        logger.exception(f"Unexpected error: {path}")
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)
    finally:
        if resource:
            cleanup(resource)
```

## Best Practices

1. **Use context managers when possible** - `with open() as f:` handles cleanup automatically
2. **Always clean up in `finally`** - Resources should be released even on exceptions
3. **Don't raise exceptions in `finally`** - This can mask the original exception
4. **Don't call `sys.exit()` in `finally`** - Exit codes can be lost or incorrect

See also:
- [typer-interrupt.md](typer-interrupt.md) - For Ctrl+C handling
- [logging.md](logging.md) - For logging integration
