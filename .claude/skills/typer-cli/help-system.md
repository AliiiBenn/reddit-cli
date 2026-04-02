# Help System

Typer provides extensive customization for help output.

## pretty_exceptions Controls

Control exception formatting for debugging:

```python
import typer

app = typer.Typer()

# Disable pretty exceptions (minimal output)
app = typer.Typer(pretty_exceptions_enable=False)

@app.command()
def cmd(name: str):
    """Run a command."""
    raise RuntimeError(f"Failed: {name}")
```

## Show Locals in Exceptions

```python
# Show locals in exceptions (use carefully in production)
app = typer.Typer(
    pretty_exceptions_enable=True,
    pretty_exceptions_show_locals=True,  # Shows local variables!
    pretty_exceptions_short=False,  # Full traceback
)

@app.command()
def debug(val: int):
    """Debug command."""
    x = val * 2
    y = x + 10
    raise ValueError(f"Debug at y={y}")
```

**Caution:** `pretty_exceptions_show_locals=True` can expose sensitive information. Never use in production.

## Rich Help Panels

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

## Rich Help Panels for Arguments

Organize arguments into visual panels:

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def create(
    name: Annotated[str, typer.Argument(help="The user's full name", rich_help_panel="User Information")],
    email: Annotated[str, typer.Argument(help="Email address for notifications", rich_help_panel="Contact Details")],
    phone: Annotated[str, typer.Argument(help="Phone number", rich_help_panel="Contact Details")] = None,
):
    """Create a new user account."""
    print(f"Creating: {name}, {email}")

# Help displays arguments organized by panels
```

## Rich Markup Mode

Set global markup mode for help text:

```python
import typer

app = typer.Typer(rich_markup_mode="markdown")

@app.command()
def create(name: str):
    """Create a **new** user account.

    This command creates a user with the given *name*.
    """
    typer.echo(f"Creating: {name}")

# Help text renders markdown formatting
```

**Available modes:**
- `"rich"` - Default Rich markup (bold, italic, colors)
- `"markdown"` - Markdown formatting
- `"none"` - No markup (plain text)

## Custom Help Text Format

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

## Hidden Help Option

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

## Pretty Exceptions Settings Summary

| Setting | Purpose | Production Safe |
|---------|---------|-----------------|
| `pretty_exceptions_enable` | Enable/disable pretty formatting | Yes (disable in prod) |
| `pretty_exceptions_show_locals` | Show local variables in traceback | No |
| `pretty_exceptions_short` | Use shorter traceback format | Yes |

## Hidden Commands and Options

Hide from help but keep functional:

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command(hidden=True)
def secret_command():
    """This command is hidden from help."""
    typer.echo("Secret!")

@app.command()
def public_command():
    """This command is visible."""
    typer.echo("Public!")

@app.command()
def config(
    secret_key: Annotated[str, typer.Option(hidden=True)] = "default",
):
    """Configure settings."""
    typer.echo(f"Secret key: {secret_key}")

# python main.py --help           # Shows only public_command
# python main.py secret-command    # Still works
# python main.py config --help    # Shows only visible options
```

## Key Points

- `pretty_exceptions_show_locals=True` exposes sensitive data - never use in production
- `rich_help_panel` organizes commands and arguments visually
- `rich_markup_mode` enables markdown ("markdown") or rich markup ("rich")
- `short_help` shows in main listing, `help` shows in command-specific help
- `epilog` adds text at the end of help output
- `no_args_is_help=True` shows help when no arguments provided
- `suggest_commands=True` suggests similar commands on typos
- `hidden=True` hides commands/options from help
- `add_help_option=False` disables automatic `--help`
