# Click Exception Compatibility

Typer is built on Click, so some exceptions are shared between the two libraries.

## Exception Compatibility

### BadParameter

Typer's `BadParameter` **inherits** from Click's `BadParameter`:

```python
import click
from typer import BadParameter

# Typer's BadParameter HERITS from click.BadParameter
# So catching click.BadParameter also catches Typer's

try:
    # Typer code
    raise BadParameter("Invalid email")
except click.BadParameter as e:
    # This catches Typer's BadParameter!
    typer.echo(f"Parameter error: {e.param}")
```

### Abort is NOT Compatible

**Important:** `typer.Abort` is NOT the same as `click.Abort`:

```python
import click

try:
    raise typer.Abort()
except click.Abort:
    pass  # DOES NOT CATCH typer.Abort!

# You must catch SystemExit to catch typer.Abort
try:
    raise typer.Abort()
except SystemExit:
    pass  # This DOES catch it
```

## Click Exceptions Reference

| Click Exception | Typer Equivalent | Compatible |
|----------------|------------------|-------------|
| `click.Abort` | `typer.Abort` | NO |
| `click.BadParameter` | `typer.BadParameter` | YES |
| `click.MissingParameter` | `typer.MissingArgument` | YES (partially) |
| `click.NoSuchOption` | `typer.NoSuchOption` | YES |
| `click.BadOptionUsage` | - | NO |

## Accessing Click Context

You can access Click's context from Typer:

```python
from click import Context

@app.command()
def main(ctx: typer.Context):
    # Access Click context
    click_ctx = ctx.make_context("command", [])
    # Or directly access the Click command object
    click_command = ctx.command
```

## Using Click Exceptions in Typer

```python
import click
from typer import BadParameter

@app.command()
def create(name: str):
    try:
        # Some Click code that raises BadParameter
        click.BadParameter("Invalid name", param_hint="name")
    except click.BadParameter as e:
        # This catches both Click and Typer BadParameter
        typer.echo(f"Parameter error for {e.param}: {e.format_message()}")
        raise typer.Exit(code=2)
```

## Migration from Click to Typer

When migrating from Click to Typer, be aware that:

1. `click.Abort` → Use `typer.Abort()`
2. `click.BadParameter` → Use `typer.BadParameter`
3. `click.echo(..., err=True)` → Use `typer.echo(..., err=True)`
4. `click.style()` → Use `typer.style()`

See also:
- [exception-hierarchy.md](exception-hierarchy.md) - For the full exception hierarchy
- [typer-abort.md](typer-abort.md) - For typer.Abort usage
- [secho-style.md](secho-style.md) - For typer styling functions
