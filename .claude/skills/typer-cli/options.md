# Options

Options are named parameters that start with `--`. They are optional by default.

## Optional Option

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def main(
    name: str,
    lastname: Annotated[str, typer.Option()] = "Unknown",
):
    print(f"Hello {name} {lastname}")

# python main.py Alice
# python main.py Alice --lastname Smith
```

## Boolean Flag

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def main(
    name: str,
    verbose: Annotated[bool, typer.Option("-v", "--verbose")] = False,
):
    if verbose:
        print(f"DEBUG: Processing {name}")
    print(f"Hello {name}")
```

## Negatable Flag

Use `--flag/--no-flag` syntax for boolean flags that can be negated:

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def main(
    name: str,
    verbose: Annotated[bool, typer.Option("--verbose/--no-verbose")] = False,
):
    """Run with --verbose or --no-verbose."""
    if verbose:
        typer.echo("Verbose mode on")
    else:
        typer.echo("Verbose mode off")
```

## Required Option

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def main(name: str, lastname: Annotated[str, typer.Option()]):
    """Last name is required."""
    print(f"Hello {name} {lastname}")

# python main.py Alice --lastname Smith
# Without --lastname: Error: Missing option '--lastname'
```

## Option with Custom Name

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def main(full_name: Annotated[str, typer.Option("--full-name", "-f")]):
    """Use --full-name or -f to specify the full name."""
    print(f"Hello {full_name}")
```

## Multiple Option Values (List)

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def main(names: Annotated[list[str], typer.Option("--name")] = []):
    """Accept multiple --name arguments."""
    for name in names:
        print(f"Hello {name}")

# python main.py --name Alice --name Bob --name Charlie
```

## Environment Variable with `envvar`

Options can read from environment variables:

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def main(
    token: Annotated[str, typer.Option(envvar="API_TOKEN")],
):
    """Use API token from API_TOKEN environment variable."""
    typer.echo(f"Using token: {token}")

# python main.py                          # Reads from $API_TOKEN
# API_TOKEN=secret python main.py          # Overrides with secret
```

## Multiple Environment Variables Fallback

Options can fall back through multiple environment variables:

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def main(
    token: Annotated[
        str,
        typer.Option(envvar=["API_TOKEN", "TOKEN", "AUTH_TOKEN"])
    ],
):
    """Use token from first available env var."""
    typer.echo(f"Using token: {token}")

# python main.py
# TOKEN=fallback python main.py  # Uses TOKEN
# AUTH_TOKEN=primary python main.py  # Uses AUTH_TOKEN
```

**Environment Variable Precedence:**

```
CLI argument > Environment variable > Default value
```

```python
@app.command()
def config(
    verbose: Annotated[bool, typer.Option("--verbose", envvar="VERBOSE")] = False,
):
    """Precedence: CLI > env var > default"""
    if verbose:
        typer.echo("Verbose mode enabled")
```

## Multiple Values with `nargs`

Use `nargs` to accept exactly N values for an option:

```python
from typing import Annotated, Tuple
import typer

app = typer.Typer()

@app.command()
def main(
    coordinates: Annotated[Tuple[float, float], typer.Option(nargs=2)] = (0.0, 0.0),
):
    """Accept exactly 2 values for coordinates."""
    x, y = coordinates
    typer.echo(f"X: {x}, Y: {y}")

# python main.py --coordinates 10.5 20.5
```

## Context Settings

Use `context_settings` to control argument parsing behavior:

```python
from typing import Annotated
import typer

app = typer.Typer(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})

@app.command()
def main(ctx: typer.Context, name: str):
    """Handle extra arguments."""
    typer.echo(f"Name: {name}")
    if ctx.args:
        typer.echo(f"Extra args: {ctx.args}")

# python main.py Alice --extra1 value1 --extra2 value2
# -> Name: Alice, Extra args: ['--extra1', 'value1', '--extra2', 'value2']
```

## Hidden Options and Commands

Use `hidden=True` to hide options or commands from help:

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

## Show Default Value

Control whether default values are shown in help:

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def main(
    name: Annotated[str, typer.Option(show_default=False)] = "World",
    count: Annotated[int, typer.Option(show_default=True)] = 5,
):
    """Configure settings."""
    typer.echo(f"{name}: {count}")

# --help shows:
# --name TEXT                    # No default shown
# --count INTEGER [default: 5]  # Default shown
```

## Shell Completion with Custom Items

Use `shell_complete` with `CompletionItem` for custom shell completion:

```python
from typing import Annotated
import typer
from typer.shell_completion import CompletionItem

app = typer.Typer()

def complete_framework(ctx: typer.Context, param: typer.Parameter, incomplete: str):
    """Complete framework names."""
    frameworks = [
        CompletionItem("django", help="Django web framework"),
        CompletionItem("fastapi", help="FastAPI web framework"),
        CompletionItem("flask", help="Flask microframework"),
        CompletionItem("pyramid", help="Pyramid WSGI framework"),
    ]
    for fw in frameworks:
        if fw.value.startswith(incomplete):
            yield fw

@app.command()
def new(
    framework: Annotated[str, typer.Option(shell_complete=complete_framework)],
):
    """Create a new project."""
    typer.echo(f"Creating {framework} project")

# python main.py new d  # Tab completion shows django
# python main.py new f  # Tab completion shows fastapi, flask
```

**Use when:** You need custom completion logic that depends on context or filters available choices dynamically.

## Case-Insensitive Options

Control whether option names are case-sensitive:

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def network(
    network: Annotated[str, typer.Option("--network", case_sensitive=False)] = "simple",
):
    """Connect to a network."""
    typer.echo(f"Connecting to {network}")

# python main.py --NETWORK custom  # Works! network="custom"
# python main.py --network custom  # Also works
```

**Use when:** Building user-friendly CLIs where case should not matter for option names.

## Custom Parser for Options

Use `parser` to apply custom type conversion and validation:

```python
from typing import Annotated
import typer

app = typer.Typer()

def parse_port(value: str) -> int:
    """Parse and validate a port number."""
    try:
        port = int(value)
    except ValueError:
        raise typer.BadParameter("Port must be a number")
    if not 1 <= port <= 65535:
        raise typer.BadParameter("Port must be between 1 and 65535")
    return port

@app.command()
def serve(
    port: Annotated[int, typer.Option(parser=parse_port)] = 8080,
):
    """Start the server on a specific port."""
    typer.echo(f"Starting server on port {port}")

# python main.py serve --port 3000  # OK
# python main.py serve --port 99999  # Error: Port must be between 1 and 65535
```

**Use when:** You need complex validation beyond basic type conversion.

## Prompt Required

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
# python main.py setup --username ""    # Empty string triggers re-prompt
```

**Use when:** You need explicit user confirmation even if a value is provided on command line.

## Shell Completion with CompletionType

Typer supports shell completion for common types:

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def main(
    name: Annotated[str, typer.Argument(completion=typer.CompletionType.FILE)],
):
    """Select a file."""
    typer.echo(f"Selected: {name}")
```

Completion is automatic for annotated types like `str`, `int`, `Path`, `Enum`.

## Key Points

- Options are named parameters starting with `--` (optional by default)
- Use `Annotated` syntax for all parameter definitions
- Boolean flags use `True/False` defaults
- Negatable flags use `--flag/--no-flag` syntax
- `envvar` reads from environment variables with fallback chain support
- `shell_complete` provides custom completion logic
- `parser` allows custom type validation
- `case_sensitive=False` allows case-insensitive option names
- `hidden=True` hides from help but keeps functionality
- `show_default` controls default value visibility
