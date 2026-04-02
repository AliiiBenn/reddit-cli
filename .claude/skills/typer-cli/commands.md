# Commands

Commands are the actions your CLI performs. Each command is a function decorated with `@app.command()`.

## Basic Command

```python
import typer

app = typer.Typer()

@app.command()
def create(username: str):
    """Create a new user."""
    print(f"Creating user: {username}")

@app.command()
def delete(username: str):
    """Delete an existing user."""
    print(f"Deleting user: {username}")

if __name__ == "__main__":
    app()
```

## Command with Arguments and Options

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def send(
    recipient: Annotated[str, typer.Argument(help="Email recipient")],
    subject: Annotated[str, typer.Option("--subject", "-s")] = "No Subject",
    cc: Annotated[list[str], typer.Option("--cc")] = None,
):
    """Send an email to a recipient."""
    print(f"To: {recipient}")
    print(f"Subject: {subject}")
    print(f"CC: {cc or []}")
```

## Command with Custom Name

Use `name` to change the CLI command name (default uses function name with underscores converted to dashes):

```python
import typer

app = typer.Typer()

@app.command(name="create-user")
def create(name: str):
    """Create a new user."""
    print(f"Creating user: {name}")

@app.command(name="delete-user")
def delete(name: str):
    """Delete an existing user."""
    print(f"Deleting user: {name}")

# python main.py create-user alice  # Instead of create alice
# python main.py delete-user bob   # Instead of delete bob
```

**Use when:** The function name doesn't translate well to CLI usage, or you want a different command name than the function name.

## Command with Short Help

The `short_help` appears in the main `--help` output, while `help` appears in command-specific help:

```python
import typer

app = typer.Typer()

@app.command(
    help="Create a new user account with email and password.",
    short_help="Create a new user",
)
def create(username: str, email: str, password: str):
    """Create a new user account."""
    print(f"Creating: {username}, {email}")

# python main.py --help
# Shows: create  Create a new user  (short_help)

# python main.py create --help
# Shows: Create a new user account with email and password. (help)
```

## Command Epilog

Add text at the end of help output:

```python
import typer

app = typer.Typer()

@app.command(
    help="Create a new user account.",
    epilog="Made with love | Version 2.0 | https://example.com",
)
def create(username: str):
    """Create a new user."""
    print(f"Creating: {username}")

# Help output ends with the epilog
```

## Deprecated Command

Mark a command as deprecated:

```python
import typer

app = typer.Typer()

@app.command(deprecated=True)
def old_create(username: str):
    """Old create command - use 'create' instead."""
    print(f"Creating: {username}")

@app.command()
def create(username: str):
    """Create a new user."""
    print(f"Creating: {username}")

# python main.py old-create alice
# Warning: DeprecationWarning: 'old-create' is deprecated. Use 'create' instead.
```

## no_args_is_help

Show help when no arguments are provided:

```python
import typer

app = typer.Typer(no_args_is_help=True)

@app.command()
def create(name: str):
    """Create a new user."""
    print(f"Creating: {name}")

@app.command()
def delete(name: str):
    """Delete a user."""
    print(f"Deleting: {name}")

# python main.py          # Shows help
# python main.py create   # Runs create
```

## Suggest Commands

Typer can suggest similar commands when a command is not found:

```python
import typer

app = typer.Typer(suggest_commands=True)  # Default is True

@app.command()
def create(name: str):
    """Create a new resource."""
    print(f"Creating: {name}")

@app.command()
def delete(name: str):
    """Delete a resource."""
    print(f"Deleting: {name}")

# python main.py creae
# Error: No such command 'creae'.
# Did you mean 'create'?
```

## Add Help Option

Control whether `--help` is automatically added:

```python
import typer

app = typer.Typer(add_help_option=True)  # Default is True

# --help works as expected

app2 = typer.Typer(add_help_option=False)

@app2.command()
def secret():
    """Hidden command - no --help available."""
    print("Secret!")

# python main2.py secret --help
# Error: No such option: --help
```

## Hidden Command

Hide a command from help but keep it functional:

```python
import typer

app = typer.Typer()

@app.command(hidden=True)
def debug_mode():
    """Secret debug command - not shown in help."""
    print("Debug mode activated!")

@app.command()
def normal():
    """Normal command."""
    print("Normal operation")

# python main.py --help    # Does not show debug-mode
# python main.py debug-mode  # Still works
```

## Rich Help Panel for Commands

Organize commands into visual panels:

```python
import typer

app = typer.Typer()

@app.command(rich_help_panel="User Management")
def create(name: str):
    """Create a new user."""
    print(f"Creating: {name}")

@app.command(rich_help_panel="User Management")
def delete(name: str):
    """Delete a user."""
    print(f"Deleting: {name}")

@app.command(rich_help_panel="System")
def status():
    """Check system status."""
    print("Status: OK")

@app.command(rich_help_panel="System")
def restart():
    """Restart the system."""
    print("Restarting...")

# Help output organizes commands by panel
```

## Command with Context Parameter

Access context information within a command:

```python
import typer

app = typer.Typer()

@app.command()
def info(ctx: typer.Context, name: str):
    """Display command information."""
    typer.echo(f"Command: {ctx.invoked_subcommand}")
    typer.echo(f"Name: {name}")
    typer.echo(f"All params: {ctx.params}")
```

## Chained Commands

Commands can call other commands programmatically:

```python
import typer

app = typer.Typer()

@app.command()
def build(name: str):
    """Build a project."""
    typer.echo(f"Building: {name}")

@app.command()
def deploy(name: str):
    """Deploy a project after building."""
    # First build
    ctx = typer.Context.invoke
    ctx.invoke(build, name=name)
    # Then deploy
    typer.echo(f"Deploying: {name}")

# python main.py deploy myapp
# Building: myapp
# Deploying: myapp
```

## Key Points

- Commands are functions decorated with `@app.command()`
- Function name with underscores becomes dashes in CLI (`create_user` -> `create-user`)
- Use `name` parameter for custom CLI command names
- `short_help` shows in main help, `help` shows in command help
- `epilog` adds text at the end of help output
- `deprecated=True` marks commands as deprecated
- `hidden=True` hides from help but keeps functionality
- `rich_help_panel` organizes commands visually
- `no_args_is_help=True` shows help when no args provided
- `suggest_commands=True` suggests similar commands on misspellings
