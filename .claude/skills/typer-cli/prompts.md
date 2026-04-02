# Prompts

Prompts interactively ask users for input.

## Simple Prompt with Option

Use `typer.Option(prompt=True)` for simple interactive options:

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def create_user(
    username: Annotated[str, typer.Option(prompt=True)],
):
    """Create a new user with interactive prompt."""
    print(f"Creating user: {username}")
```

## Confirmation Prompt

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def delete(
    username: str,
    force: Annotated[bool, typer.Option(prompt="Are you sure?")],
):
    """Delete a user with confirmation."""
    if force:
        print(f"Deleting user: {username}")
    else:
        print("Deletion cancelled")
```

## Custom Prompt Message

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def delete(
    username: str,
    force: Annotated[bool, typer.Option(prompt=f"Delete user {username}?")],
):
    """Delete a user with custom confirmation message."""
    if force:
        print(f"Deleted: {username}")
```

## Interactive Input with `typer.prompt()`

```python
import typer

app = typer.Typer()

@app.command()
def create_project():
    """Create a new project interactively."""
    name = typer.prompt("Project name")
    description = typer.prompt("Description", default="No description")
    color = typer.prompt("Favorite color", default="red")

    print(f"Creating project: {name}")
    print(f"Description: {description}")
    print(f"Color: {color}")
```

## Prompt with Type Conversion

```python
import typer

app = typer.Typer()

@app.command()
def calculate():
    """Calculate with user input."""
    age = typer.prompt("Enter your age", type=int)
    height = typer.prompt("Enter your height (meters)", type=float)

    print(f"Age: {age}, Height: {height}")
    print(f"In 10 years you will be {age + 10}")

# python main.py calculate
# Enter your age: 25
# Enter your height (meters): 1.75
# Age: 25, Height: 1.75
# In 10 years you will be 35
```

## Prompt with Custom Validation

```python
import typer

app = typer.Typer()

@app.command()
def create_account():
    """Create an account with validation."""
    while True:
        username = typer.prompt("Enter username")
        if len(username) >= 3:
            break
        typer.echo("Username must be at least 3 characters", err=True)

    while True:
        password = typer.prompt("Enter password", hide_input=True)
        if len(password) >= 8:
            break
        typer.echo("Password must be at least 8 characters", err=True)

    typer.echo(f"Account created for: {username}")
```

## Confirmation with `confirm()`

```python
import typer

app = typer.Typer()

@app.command()
def deploy():
    """Deploy the application."""
    if not typer.confirm("Are you sure you want to deploy?"):
        print("Deployment cancelled")
        raise typer.Abort()

    print("Deploying...")

@app.command()
def cleanup():
    """Clean up resources."""
    if not typer.confirm("This will delete all temporary files. Continue?"):
        typer.echo("Cleanup aborted")
        return
    typer.echo("Cleaning up...")
```

## Confirm with Default

```python
import typer

app = typer.Typer()

@app.command()
def update():
    """Update the application."""
    # Default is False (user must explicitly say yes)
    if not typer.confirm("Update to latest version?", default=False):
        typer.echo("Update cancelled")
        return
    typer.echo("Updating...")

@app.command()
def restart():
    """Restart the service."""
    # Default is True (user can press Enter to accept)
    if not typer.confirm("Restart now?", default=True):
        typer.echo("Restart postponed")
        return
    typer.echo("Restarting...")
```

## Hidden Input for Passwords

```python
import typer

app = typer.Typer()

@app.command()
def login():
    """Login with password."""
    username = typer.prompt("Username")
    password = typer.prompt("Password", hide_input=True)

    if username == "admin" and password == "secret":
        typer.echo("Login successful!")
    else:
        typer.echo("Login failed!", err=True)
        raise typer.Abort()
```

## Prompt with Custom Parser

```python
import typer

app = typer.Typer()

def parse_port(value: str) -> int:
    """Parse and validate port number."""
    try:
        port = int(value)
    except ValueError:
        typer.echo("Invalid port number", err=True)
        raise typer.Abort()
    if not (1 <= port <= 65535):
        typer.echo("Port must be between 1 and 65535", err=True)
        raise typer.Abort()
    return port

@app.command()
def serve():
    """Start server with custom port."""
    port = typer.prompt("Enter port", type=parse_port, default=8080)
    typer.echo(f"Starting server on port {port}")
```

## Prompt Required (Always Ask)

Force a prompt even when the option has a default:

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def setup(
    username: Annotated[str, typer.Option(prompt=True, prompt_required=True)],
):
    """Set up a new user account."""
    typer.echo(f"Setting up {username}")

# python main.py setup                  # Always prompts
# python main.py setup --username bob   # Still prompts (prompt_required=True)
# python main.py setup --username ""     # Empty string triggers re-prompt
```

## Multiple Prompts in Sequence

```python
import typer

app = typer.Typer()

@app.command()
def new_project():
    """Create a new project with multiple prompts."""
    typer.echo("Let's create a new project!")
    typer.echo("")

    name = typer.prompt("Project name", default="my-project")
    description = typer.prompt("Description", default="")
    owner = typer.prompt("Project owner")

    while True:
        confirm = typer.confirm("Is this correct?")
        if confirm:
            break
        typer.echo("Let's try again...")
        name = typer.prompt("Project name")
        description = typer.prompt("Description")
        owner = typer.prompt("Project owner")

    typer.echo("")
    typer.echo(f"Creating project: {name}")
    typer.echo(f"Description: {description or 'None'}")
    typer.echo(f"Owner: {owner}")
```

## Key Points

- `typer.Option(prompt=True)` makes an option prompt if not provided
- `typer.prompt()` directly asks for user input
- `typer.confirm()` asks for yes/no confirmation
- Use `hide_input=True` for password-like input
- `type=` parameter allows automatic type conversion
- `default=` provides default value (press Enter to accept)
- Validation should be done manually or with custom parser
- `prompt_required=True` always prompts even with CLI value
- Empty string (`""`) with `prompt_required=True` triggers re-prompt
- Use `raise typer.Abort()` to cancel on validation failure
