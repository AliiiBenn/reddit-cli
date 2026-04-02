# Arguments

Arguments are positional parameters in Typer. By default, they are required unless they have a default value.

## Required Argument

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def main(name: Annotated[str, typer.Argument()]):
    """Greet the user by name."""
    print(f"Hello {name}!")
```

## Optional Argument with Default

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def main(name: Annotated[str, typer.Argument()] = "World"):
    """Greet the user with an optional name."""
    print(f"Hello {name}!")
```

## Argument with Help Text

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def main(
    name: Annotated[str, typer.Argument(help="The user's name")],
):
    print(f"Hello {name}!")
```

## Dynamic Default with `default_factory`

```python
import random
from typing import Annotated
import typer

app = typer.Typer()

def get_random_greeting():
    return random.choice(["Hello", "Hi", "Greetings"])

@app.command()
def main(name: Annotated[str, typer.Argument(default_factory=get_random_greeting)]):
    """Greet with a random greeting."""
    print(f"{name}, World!")
```

## Custom Metavar

The `metavar` attribute customizes how the argument appears in help text:

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def create(
    username: Annotated[str, typer.Argument(metavar="USERNAME")],
):
    """Create a new user."""
    print(f"Creating user: {username}")

# Help shows: create USERNAME
# Instead of: create --username TEXT
```

**Use when:** You want to show a placeholder value different from the parameter name, or when the actual values are limited (like an enum).

## Rich Help Panel for Arguments

Organize arguments into visual panels in help output:

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

**Use when:** Commands have many arguments that can be logically grouped.

## Show Environment Variable

Control whether the environment variable name is shown in help:

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def config(
    secret: Annotated[str, typer.Option(envvar="API_SECRET", show_envvar=False)] = "default",
    public: Annotated[str, typer.Option(envvar="PUBLIC_KEY", show_envvar=True)] = "default",
):
    """Configure API settings."""
    print(f"Secret configured, public key: {public}")

# --secret TEXT                    # No env var shown
# --public TEXT  [default: default] (or from PUBLIC_KEY)  # Env var shown
```

**Use when:** Some environment variables are internal/implementation details and should not be exposed to users.

## Argument with Multiple Values (nargs)

Use `nargs` to accept multiple positional values:

```python
from typing import Annotated, Tuple
import typer

app = typer.Typer()

@app.command()
def move(
    coordinates: Annotated[Tuple[int, int], typer.Argument(nargs=2)],
):
    """Move to coordinates."""
    x, y = coordinates
    print(f"Moving to ({x}, {y})")

# python main.py move 10 20
# Moving to (10, 20)
```

## Hidden Argument

Use `hidden=True` to hide an argument from help but still accept it:

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def secret(
    name: Annotated[str, typer.Argument(hidden=True)],
):
    """Process a secret name."""
    print(f"Processing: {name}")

# python main.py secret --help   # Shows only basic info
# python main.py secret alice     # Still works
```

## Argument with Completion

Typer supports automatic shell completion for arguments:

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def create(
    name: Annotated[str, typer.Argument(completion=typer.CompletionType.FILE)],
):
    """Create from file."""
    print(f"Creating from: {name}")
```

Completion is automatic for annotated types like `str`, `int`, `Path`, `Enum`.

## Key Points

- Arguments are positional parameters (required by default)
- Use `Annotated` syntax for all parameter definitions
- Arguments with defaults are optional
- `metavar` customizes help display text
- `rich_help_panel` organizes arguments visually
- `hidden=True` hides from help but keeps functionality
- `default_factory` generates dynamic default values
