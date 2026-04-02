# Typer Environment Variables

Typer respects several environment variables for debugging and output control.

## Debug Environment Variables

| Variable | Purpose |
|----------|---------|
| `TYPER_STANDARD_TRACEBACK` | Full traceback mode for debugging production apps |
| `TYPER_USE_RICH` | Disable Rich entirely for standard error output |
| `TYPER_COLOR_SYSTEM` | Force color output |
| `TYPER_terminal_columns` | Override terminal width |
| `TYPER_terminal_rows` | Override terminal height |

## TYPER_STANDARD_TRACEBACK

Full traceback mode - critical for debugging production apps:

```bash
# Debug a Typer app in production without modifying code
TYPER_STANDARD_TRACEBACK=1 python -m myapp

# With specific error
TYPER_STANDARD_TRACEBACK=1 python -m myapp create --name test
```

This shows the full Python traceback instead of the pretty Rich-formatted one.

## TYPER_USE_RICH

Disable Rich to get standard error output:

```bash
# Disable Rich for standard errors
TYPER_USE_RICH=0 python -m myapp

# Useful when redirecting errors to a file
TYPER_USE_RICH=0 python -m myapp 2> error.log
```

## TYPER_COLOR_SYSTEM

Force color output regardless of terminal:

```bash
# Force colors
TYPER_COLOR_SYSTEM=always python -m myapp

# Disable colors
TYPER_COLOR_SYSTEM=none python -m myapp
```

## Terminal Size Variables

Override terminal dimensions:

```bash
# Debug with specific terminal size
TYPER_terminal_columns=120 TYPER_STANDARD_TRACEBACK=1 python -m myapp

# Force smaller terminal for testing
TYPER_terminal_columns=80 TYPER_terminal_rows=24 python -m myapp
```

## Combining for Debugging

```bash
# Maximum debugging info
TYPER_STANDARD_TRACEBACK=1 TYPER_USE_RICH=1 TYPER_terminal_columns=120 python -m myapp

# Production-like but with full tracebacks
TYPER_STANDARD_TRACEBACK=1 python -m myapp
```

## Using in Code

You can also check these in your application:

```python
import os
import typer

def is_debug_mode() -> bool:
    return os.getenv("TYPER_STANDARD_TRACEBACK") == "1"

def is_rich_disabled() -> bool:
    return os.getenv("TYPER_USE_RICH") == "0"

@app.command()
def debug_command():
    if is_debug_mode():
        typer.echo("Debug mode enabled")
```

See also:
- [pretty-exceptions.md](pretty-exceptions.md) - For pretty_exceptions configuration
- [rich-errors.md](rich-errors.md) - For Rich error formatting
