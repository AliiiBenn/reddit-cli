# Context

Access CLI state via `typer.Context`. The context object provides access to command parameters, arguments, and allows state sharing.

## Basic Context Usage

```python
import typer

app = typer.Typer()

@app.command()
def info(ctx: typer.Context, name: str):
    """Display command information."""
    typer.echo(f"Command invoked: {ctx.invoked_subcommand}")
    typer.echo(f"Name: {name}")
    typer.echo(f"All params: {ctx.params}")
```

## Context Attributes

| Attribute | Description |
|-----------|-------------|
| `ctx.invoked_subcommand` | Name of the command being invoked, or `None` |
| `ctx.args` | List of extra raw arguments passed to the command |
| `ctx.params` | Dict of parsed parameters for the command |
| `ctx.command` | The command object being executed |
| `ctx.obj` | Custom object for passing state between commands |

## Sharing State via ctx.obj

Use `ctx.obj` to share state between callbacks and commands:

```python
import typer

app = typer.Typer()

@app.callback()
def main_callback(ctx: typer.Context, verbose: bool = False):
    """Initialize application state."""
    ctx.obj = {"verbose": verbose, "registry": []}

@app.command()
def create(ctx: typer.Context, name: str):
    """Create a new item and add to registry."""
    ctx.obj["registry"].append(name)
    typer.echo(f"Created: {name}")
    typer.echo(f"Total items: {len(ctx.obj['registry'])}")

@app.command()
def list_items(ctx: typer.Context):
    """List all registered items."""
    for item in ctx.obj["registry"]:
        typer.echo(f" - {item}")

@app.command()
def clear(ctx: typer.Context):
    """Clear the registry."""
    ctx.obj["registry"].clear()
    typer.echo("Registry cleared")

# python main.py create apple
# python main.py create banana
# python main.py list-items
# -> apple
# -> banana
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

## Resilient Parsing

Use `ctx.resilient_parsing` to skip validation during shell completion:

```python
from typing import Annotated
import typer

app = typer.Typer()

def validate_name(name: str, ctx: typer.Context, param: typer.Parameter):
    """Validate name, skip during completion."""
    if ctx.resilient_parsing:
        return name  # Return raw value during completion
    if name == "admin":
        raise typer.BadParameter("admin is a reserved name")
    return name

@app.command()
def create(
    name: Annotated[str, typer.Option(callback=validate_name)],
):
    """Create a user."""
    typer.echo(f"Creating user: {name}")

# During shell completion, validation is skipped
# This prevents completion failures for valid intermediate states
```

## ctx.command - Access Command Object

Access the command object from context:

```python
import typer

app = typer.Typer()

@app.command()
def info(ctx: typer.Context):
    """Display command information."""
    typer.echo(f"Command name: {ctx.command.name}")
    typer.echo(f"Command params: {list(ctx.command.params.keys())}")
    typer.echo(f"Command help: {ctx.command.help}")
    typer.echo(f"Short help: {ctx.command.short_help}")

# python main.py info
# Command name: info
# Command params: ['ctx']
# Command help: Display command information.
# Short help: None
```

## Context with invoke_without_command

Use context to detect if a subcommand was invoked:

```python
import typer

app = typer.Typer()

users_app = typer.Typer()

@users_app.callback(invoke_without_command=True)
def users_callback(ctx: typer.Context, verbose: bool = False):
    """Users management."""
    if ctx.invoked_subcommand is None:
        typer.echo("No specific user command invoked")
    else:
        typer.echo(f"Invoking: {ctx.invoked_subcommand}")
    if verbose:
        typer.echo("Verbose mode enabled")

@users_app.command()
def create(name: str):
    """Create a new user."""
    typer.echo(f"Creating user: {name}")

@users_app.command()
def delete(name: str):
    """Delete a user."""
    typer.echo(f"Deleting user: {name}")

app.add_typer(users_app, name="users")

# python main.py users          # No specific command
# Output: "No specific user command invoked"

# python main.py users create alice
# Output: "Invoking: create"
```

## Context for Default Values

Use context to set dynamic defaults:

```python
from datetime import datetime
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def log(ctx: typer.Context, message: str, timestamp: bool = False):
    """Log a message."""
    if timestamp:
        now = datetime.now().isoformat()
        typer.echo(f"[{now}] {message}")
    else:
        typer.echo(message)

# Access context info for conditional logic
@app.command()
def process(name: str, ctx: typer.Context):
    """Process with context-aware behavior."""
    if ctx.args:
        typer.echo(f"Extra args detected: {ctx.args}")
    typer.echo(f"Processing: {name}")
```

## Accessing Parent Context

Access parent app state from subcommands:

```python
import typer

app = typer.Typer()

@app.callback()
def main(ctx: typer.Context, debug: bool = False):
    """Main application."""
    ctx.obj = {"debug": debug}

users_app = typer.Typer()

@users_app.command()
def create(ctx: typer.Context, name: str):
    """Create a user."""
    parent_debug = ctx.parent and ctx.parent.obj and ctx.parent.obj.get("debug")
    if parent_debug:
        typer.echo(f"[DEBUG] Creating user: {name}")
    else:
        typer.echo(f"Creating user: {name}")

app.add_typer(users_app, name="users")

# python main.py --debug users create alice
# [DEBUG] Creating user: alice
```

## ctx.params - Read-Only Dictionary

`ctx.params` contains parsed parameters but should not be modified directly:

```python
# Bad - ctx.params is read-only
@app.command()
def bad(ctx: typer.Context, name: str):
    ctx.params["name"] = "hack"  # ERROR - params is read-only

# Good - use ctx.obj for shared state
@app.callback()
def main(ctx: typer.Context):
    ctx.obj = {"counter": 0}
```

## Key Points

- `ctx.obj` is the recommended way to share state between commands
- `ctx.params` is read-only - do not modify it directly
- `ctx.resilient_parsing` is True during shell completion - skip validation
- `ctx.exit()` allows early exit without raising an exception
- `ctx.invoked_subcommand` is None when no subcommand is invoked
- `ctx.parent` provides access to parent context in nested subcommands
- `ctx.command` provides access to the command object being executed
