# Subcommands

Subcommands group related commands together. Use `add_typer()` to compose multiple Typer apps.

## Multi-File Subcommands

```python
# users.py
import typer

app = typer.Typer()

@app.command()
def create(user_name: str):
    """Create a new user."""
    print(f"Creating user: {user_name}")

@app.command()
def delete(user_name: str):
    """Delete an existing user."""
    print(f"Deleting user: {user_name}")

if __name__ == "__main__":
    app()
```

```python
# items.py
import typer

app = typer.Typer()

@app.command()
def create(item: str):
    """Create a new item."""
    print(f"Creating item: {item}")

@app.command()
def delete(item: str):
    """Delete an existing item."""
    print(f"Deleting item: {item}")

@app.command()
def sell(item: str):
    """Sell an item."""
    print(f"Selling item: {item}")

if __name__ == "__main__":
    app()
```

```python
# main.py
import typer
import users
import items

app = typer.Typer()
app.add_typer(users.app, name="users")
app.add_typer(items.app, name="items")

if __name__ == "__main__":
    app()
```

Usage:
```bash
python main.py users create alice
python main.py items delete laptop
python main.py items sell laptop
```

## Single-File Subcommands

```python
import typer

app = typer.Typer()
users_app = typer.Typer()
items_app = typer.Typer()

app.add_typer(users_app, name="users")
app.add_typer(items_app, name="items")

@users_app.command("create")
def users_create(user_name: str):
    """Create a new user."""
    print(f"Creating user: {user_name}")

@users_app.command("delete")
def users_delete(user_name: str):
    """Delete an existing user."""
    print(f"Deleting user: {user_name}")

@items_app.command("create")
def items_create(item: str):
    """Create a new item."""
    print(f"Creating item: {item}")

@items_app.command("delete")
def items_delete(item: str):
    """Delete an existing item."""
    print(f"Deleting item: {item}")

if __name__ == "__main__":
    app()
```

## Nested Subcommands

```python
# reigns.py
import typer

app = typer.Typer()

@app.command()
def conquer(name: str):
    """Conquer a reign."""
    print(f"Conquering reign: {name}")

@app.command()
def destroy(name: str):
    """Destroy a reign."""
    print(f"Destroying reign: {name}")

if __name__ == "__main__":
    app()
```

```python
# main.py
import typer
import reigns

app = typer.Typer()
app.add_typer(reigns.app, name="reigns")

if __name__ == "__main__":
    app()
```

Command tree:
```
main.py
└── reigns
    ├── conquer
    └── destroy
```

## Subapp with invoke_without_command

Use `invoke_without_command=True` on subapp callbacks to execute the callback even when a specific subcommand is invoked:

```python
import typer

app = typer.Typer()

users_app = typer.Typer()

@users_app.callback(invoke_without_command=True)
def users_callback(verbose: bool = False):
    """Users management."""
    if verbose:
        typer.echo("Users: verbose mode")

@users_app.command()
def create(name: str):
    """Create a new user."""
    typer.echo(f"Creating user: {name}")

@users_app.command()
def delete(name: str):
    """Delete a user."""
    typer.echo(f"Deleting user: {name}")

app.add_typer(users_app, name="users")

# python main.py users create alice
# Output: "Creating user: alice"
# Note: Callback is NOT invoked here

# python main.py users --verbose
# Output: "Users: verbose mode"
# Note: Callback IS invoked since no command given
```

## add_typer Without Name (Top-Level Commands)

Use `add_typer()` without a name to merge commands at the top level:

```python
import typer

app = typer.Typer()
version_app = typer.Typer()
users_app = typer.Typer()

@version_app.command()
def version():
    """Show version."""
    typer.echo("v1.0.0")

@users_app.command()
def create(name: str):
    """Create a user."""
    typer.echo(f"Creating: {name}")

@users_app.command()
def delete(name: str):
    """Delete a user."""
    typer.echo(f"Deleting: {name}")

# Commands without name - merged at top level
app.add_typer(version_app)

# Commands with name - become subcommands
app.add_typer(users_app, name="users")

# python main.py version        # Top-level command
# python main.py users create   # Subcommand
```

## __main__.py Entry Point

For `python -m package` execution:

```python
# src/mycli/__init__.py
from .main import app
__version__ = "1.0.0"
```

```python
# src/mycli/main.py
import typer

app = typer.Typer()

@app.command()
def create(name: str):
    """Create a new resource."""
    print(f"Creating: {name}")

if __name__ == "__main__":
    app()
```

```python
# src/mycli/__main__.py
from .main import app

if __name__ == "__main__":
    app()
```

```toml
# pyproject.toml
[project]
name = "mycli"
version = "1.0.0"
run_module = "mycli"

[project.scripts]
mycli = "mycli.main:app"
```

```bash
python -m mycli create alice
```

## Deeply Nested Subcommands

For deeply nested command structures:

```python
# level2.py
import typer

app = typer.Typer()

@app.command()
def action(name: str):
    """Perform an action."""
    typer.echo(f"Doing: {name}")

if __name__ == "__main__":
    app()
```

```python
# level1.py
import typer
import level2

app = typer.Typer()
app.add_typer(level2.app, name="action")

if __name__ == "__main__":
    app()
```

```python
# main.py
import typer
import level1

app = typer.Typer()
app.add_typer(level1.app, name="level1")

if __name__ == "__main__":
    app()
```

Command tree:
```
main.py level1 action <name>
```

## Subcommand with Shared State

Share state across subcommands using callbacks:

```python
import typer

app = typer.Typer()

# Define shared state in parent
app_state = {"verbose": False}

@app.callback()
def main(verbose: bool = False):
    """Main application."""
    app_state["verbose"] = verbose

# Subcommand group
admin_app = typer.Typer()

@admin_app.callback(invoke_without_command=True)
def admin_callback():
    """Admin commands."""
    # Can access parent state if needed
    pass

@admin_app.command()
def create(name: str):
    """Create something."""
    if app_state["verbose"]:
        typer.echo(f"Creating: {name}")
    typer.echo(f"Created: {name}")

app.add_typer(admin_app, name="admin")
```

## Subcommand Callback Override Precedence

When multiple callbacks are defined, the precedence order is:

```
add_typer(callback=...) > @subapp.callback() > typer.Typer(callback=...)
```

The callback from `add_typer()` takes highest precedence, followed by subapp callbacks, then main app callbacks.

## Key Points

- Use `add_typer()` to compose subcommand groups
- Multi-file structure recommended for large CLIs
- Single-file structure works for smaller CLIs
- `invoke_without_command=True` runs callback even when subcommand is invoked
- `add_typer()` without `name` merges commands at top level
- Use `__main__.py` for `python -m package` entry points
- Keep subcommand depth to 2-3 levels maximum for usability
- Callbacks define precedence: `add_typer(callback=...)` > subapp callback > main callback
