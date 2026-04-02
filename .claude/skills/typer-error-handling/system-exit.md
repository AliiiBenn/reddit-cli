# SystemExit vs typer.Exit

## Key Difference

**`typer.Exit`** and **``typer.Abort``** are subclasses of **`SystemExit`**, NOT `TyperError`.

This has important implications for exception handling.

## Exception Hierarchy

```
Exception (base)
└── SystemExit
    ├── typer.Exit        # Program termination (code=0 by default)
    └── typer.Abort       # Fatal termination (code=1)

TyperError (base class for parameter/validation errors)
├── BadParameter          # Invalid parameter value
├── MissingOption         # Required option not provided
├── MissingArgument       # Required argument not provided
├── NoSuchOption          # Unknown option
├── ValidationError       # General validation failure
└── TyperInterrupt        # User interrupted (Ctrl+C) - exit code 130
```

## Catching SystemExit

Since `typer.Exit` and `typer.Abort` inherit from `SystemExit`, they bypass normal `Exception` handling:

```python
# This will NOT catch typer.Exit!
try:
    raise typer.Exit("Error", code=1)
except Exception:
    print("Never reached!")

# This WILL catch typer.Exit
try:
    raise typer.Exit("Error", code=1)
except SystemExit:
    print("Caught!")

# This also catches typer.Abort
try:
    raise typer.Abort()
except SystemExit:
    print("Caught Abort!")
```

## Why This Matters

```python
# Bad - Exception handler doesn't catch Exit
@app.command()
def bad_example():
    try:
        risky_operation()
    except Exception as e:
        # This NEVER catches typer.Exit!
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)

# Good - Use proper error handling
@app.command()
def good_example():
    try:
        risky_operation()
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)
```

## Using sys.exit() in Typer

Using `sys.exit()` works but loses Rich formatting:

```python
import sys
import typer

@app.command()
def bad_example():
    # Loses Rich formatting!
    sys.exit(1)

@app.command()
def good_example():
    # Preserves Rich formatting
    raise typer.Exit(code=1)

@app.command()
def also_good():
    # Explicit message with Rich
    raise typer.Exit("Error occurred", code=1, err=True)
```

## Click Exception Compatibility

Typer is built on Click, so some exceptions are shared:

```python
import click
from typer import BadParameter

# Typer's BadParameter INHERITS from click.BadParameter
# So catching click.BadParameter also catches Typer's

try:
    # Typer code
    raise BadParameter("Invalid email")
except click.BadParameter as e:
    # This catches Typer's BadParameter!
    typer.echo(f"Parameter error: {e.param}")

# But typer.Abort IS NOT click.Abort!
try:
    raise typer.Abort()
except click.Abort:
    pass  # DOES NOT CATCH!
except SystemExit:
    pass  # DOES catch typer.Abort (because SystemExit)
```

## Best Practice

**Prefer `typer.Exit()` and `typer.Abort()` over `sys.exit()`** for proper integration with Typer's exception handling and Rich formatting.

```python
# Recommended
raise typer.Exit(code=0)  # Clean success
raise typer.Exit("Error", code=1, err=True)  # Error with message
raise typer.Abort()  # Fatal error, shows "Aborted!"

# Avoid in Typer commands
import sys
sys.exit(1)  # Works but loses Rich formatting
```

See also:
- [typer-exit.md](typer-exit.md) - For typer.Exit patterns
- [typer-abort.md](typer-abort.md) - For typer.Abort patterns
- [exception-hierarchy.md](exception-hierarchy.md) - For the full exception hierarchy
