# Callbacks

Callbacks run before commands and can define app-level options. They are decorated with `@app.callback()`.

## Basic Callback

```python
import typer

app = typer.Typer()
state = {"verbose": False}

@app.callback()
def main(verbose: bool = False):
    """Manage items in the CLI app."""
    if verbose:
        state["verbose"] = True
        print("Verbose mode enabled")

@app.command()
def create(name: str):
    """Create a new item."""
    if state["verbose"]:
        print(f"About to create: {name}")
    print(f"Created: {name}")

@app.command()
def delete(name: str):
    """Delete an existing item."""
    if state["verbose"]:
        print(f"About to delete: {name}")
    print(f"Deleted: {name}")

if __name__ == "__main__":
    app()
```

The callback's docstring becomes the app's help text.

## Invoke Callback Without Command

```python
import typer

app = typer.Typer()

@app.callback(invoke_without_command=True)
def main():
    """Initialize the application."""
    print("Initializing database...")

@app.command()
def create(name: str):
    """Create a new item."""
    print(f"Created: {name}")

# python main.py        -> "Initializing database..."
# python main.py create -> "Initializing database..." then "Created: ..."
```

## Exclusive Callback (Skip When Command Invoked)

```python
import typer

app = typer.Typer()

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Initialize the application."""
    if ctx.invoked_subcommand is None:
        print("No command invoked - running default")

@app.command()
def create(name: str):
    """Create a new item."""
    print(f"Created: {name}")

# python main.py        -> "No command invoked - running default"
# python main.py create -> (callback skipped)
```

## Eager Option with `is_eager=True`

Options with `is_eager=True` are parsed before all other options. Use this for `--version` to show version immediately without parsing other arguments:

```python
__version__ = "1.0.0"
app = typer.Typer()

@app.callback(is_eager=True)
def version_callback(
    ctx: typer.Context,
    version: bool = False,
):
    """Show version information."""
    if version:
        typer.echo(f"v{__version__}")
        raise typer.Exit()
```

## Callback Override Precedence

When multiple callbacks are defined, the precedence order is:

```
add_typer(callback=...) > @subapp.callback() > typer.Typer(callback=...)
```

The callback from `add_typer()` takes highest precedence, followed by subapp callbacks, then main app callbacks.

## Callback with Multiple Options

```python
import typer

app = typer.Typer()

@app.callback()
def main(
    ctx: typer.Context,
    verbose: bool = False,
    config: str = "default.cfg",
    debug: bool = False,
):
    """Main application with global options."""
    ctx.obj = {
        "verbose": verbose,
        "config": config,
        "debug": debug,
    }
    if verbose:
        typer.echo(f"Verbose mode enabled")
    if debug:
        typer.echo(f"Debug mode enabled")
    if verbose or debug:
        typer.echo(f"Using config: {config}")

@app.command()
def build(name: str, ctx: typer.Context):
    """Build a project."""
    config = ctx.obj["config"]
    typer.echo(f"Building {name} with config {config}")

@app.command()
def deploy(name: str, ctx: typer.Context):
    """Deploy a project."""
    if ctx.obj["debug"]:
        typer.echo("Debug: Starting deployment...")
    typer.echo(f"Deploying {name}")
```

## Subapp Callback

Callbacks can be defined on subapps to handle subcommand-specific options:

```python
import typer

app = typer.Typer()

# Users subapp
users_app = typer.Typer()

@users_app.callback()
def users_callback(verbose: bool = False):
    """User management options."""
    if verbose:
        typer.echo("Users: verbose mode")

@users_app.command()
def create(name: str):
    """Create a user."""
    typer.echo(f"Creating user: {name}")

@users_app.command()
def delete(name: str):
    """Delete a user."""
    typer.echo(f"Deleting user: {name}")

# Items subapp
items_app = typer.Typer()

@items_app.callback()
def items_callback(verbose: bool = False):
    """Item management options."""
    if verbose:
        typer.echo("Items: verbose mode")

@items_app.command()
def create(name: str):
    """Create an item."""
    typer.echo(f"Creating item: {name}")

app.add_typer(users_app, name="users")
app.add_typer(items_app, name="items")

# python main.py users create alice    # No verbose output
# python main.py users --verbose create alice  # Shows "Users: verbose mode"
```

## Callback Parameter Access

Access parameter information inside callbacks:

```python
from typer import CallbackParam
from typing import Annotated
import typer

app = typer.Typer()

def detailed_callback(
    value: str,
    ctx: typer.Context,
    param: CallbackParam,
):
    """Callback with full parameter access."""
    typer.echo(f"Parameter name: {param.name}")
    typer.echo(f"Parameter help: {param.help}")
    typer.echo(f"Parameter default: {param.default}")
    typer.echo(f"Parameter annotation: {param.annotation}")

@app.command()
def create(
    name: Annotated[str, typer.Option(callback=detailed_callback)],
):
    """Create a resource."""
    typer.echo(f"Creating: {name}")
```

## Callback with Context State

```python
import typer

app = typer.Typer()

@app.callback()
def main(ctx: typer.Context, config: str = "config.yaml"):
    """Initialize application state."""
    ctx.obj = {"config": config, "initialized": True}
    typer.echo(f"Loaded config: {config}")

@app.command()
def status(ctx: typer.Context):
    """Check status."""
    if ctx.obj.get("initialized"):
        typer.echo("Application is initialized")
    else:
        typer.echo("Application not initialized")
    typer.echo(f"Config: {ctx.obj.get('config')}")

# python main.py status
# Loaded config: config.yaml
# Application is initialized
# Config: config.yaml
```

## Callback Precedence with add_typer

The callback precedence can be explicitly set using `add_typer()` with `callback` parameter:

```python
import typer

app = typer.Typer()

@app.callback()
def main():
    """Main app."""
    typer.echo("Main callback")

sub_app = typer.Typer()

@sub_app.callback()
def sub():
    """Sub app."""
    typer.echo("Sub callback")

@app.command()
def main_cmd():
    """Main command."""
    typer.echo("Main command")

@sub_app.command()
def sub_cmd():
    """Sub command."""
    typer.echo("Sub command")

# Default behavior - both callbacks run
app.add_typer(sub_app, name="sub")

# With explicit callback override
# app.add_typer(sub_app, name="sub", callback=lambda: typer.echo("Override!"))
```

## Key Points

- Callbacks run before commands and define app-level options
- The callback's docstring becomes the app's help text
- `invoke_without_command=True` makes callback run even when subcommand invoked
- `ctx.invoked_subcommand is None` checks if no subcommand was invoked
- `is_eager=True` parses option before all others (for `--version`)
- Callback precedence: `add_typer(callback=...)` > subapp callback > main callback
- Use `ctx.obj` to share state between callbacks and commands
- `CallbackParam` provides access to parameter metadata in callbacks
