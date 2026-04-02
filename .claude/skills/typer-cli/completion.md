# Shell Completion

Typer supports automatic shell completion for bash, zsh, fish, and PowerShell.

## Automatic Completion

Typer automatically provides completion for annotated types:

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def create(
    name: Annotated[str, typer.Argument],
    count: Annotated[int, typer.Option("--count")] = 1,
):
    """Create resources."""
    for i in range(count):
        typer.echo(f"Creating: {name}")
```

Completion works automatically for:
- `str`, `int`, `float`, `bool`
- `Path` - file/directory paths
- `Enum` - enum values
- `list[str]`, `list[int]` - multiple values

## Custom Completion with `CompletionItem`

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
        CompletionItem("bottle", help="Bottle microframework"),
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

## Dynamic Completion Based on Context

```python
from typing import Annotated
import typer
from typer.shell_completion import CompletionItem

app = typer.Typer()

def complete_env(ctx: typer.Context, param: typer.Parameter, incomplete: str):
    """Complete environment names based on existing config."""
    # Simulate reading from config
    environments = [
        CompletionItem("development", help="Local development"),
        CompletionItem("staging", help="Staging environment"),
        CompletionItem("production", help="Production environment"),
    ]

    # Can access other params via ctx.params if needed
    for env in environments:
        if env.value.startswith(incomplete):
            yield env

@app.command()
def deploy(
    environment: Annotated[str, typer.Option(shell_complete=complete_env)],
):
    """Deploy to an environment."""
    typer.echo(f"Deploying to {environment}")

@app.command()
def test(
    environment: Annotated[str, typer.Option(shell_complete=complete_env)],
):
    """Test in an environment."""
    typer.echo(f"Testing in {environment}")
```

## File Completion

Use `CompletionType.FILE` for file path completion:

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def read(
    file: Annotated[str, typer.Argument(completion=typer.CompletionType.FILE)],
):
    """Read a file."""
    with open(file) as f:
        typer.echo(f.read())

@app.command()
def save(
    output: Annotated[str, typer.Option("--output", completion=typer.CompletionType.FILE)],
):
    """Save to a file."""
    typer.echo(f"Saving to {output}")
```

## Directory Completion

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def list_dir(
    path: Annotated[str, typer.Argument(completion=typer.CompletionType.DIR)],
):
    """List a directory."""
    import os
    for item in os.listdir(path):
        typer.echo(item)
```

## Custom Completion with Filtering

```python
from typing import Annotated
import typer
from typer.shell_completion import CompletionItem

app = typer.Typer()

def complete_tag(ctx: typer.Context, param: typer.Parameter, incomplete: str):
    """Complete git-like tags with filtering."""
    # Simulate available tags
    tags = [
        "v1.0.0",
        "v1.1.0",
        "v2.0.0-beta",
        "v2.0.0",
        "latest",
    ]

    for tag in tags:
        if tag.startswith(incomplete):
            # Add extra info for display
            help_text = "stable" if "beta" not in tag else "pre-release"
            yield CompletionItem(tag, help=help_text)

@app.command()
def checkout(
    tag: Annotated[str, typer.Option("--tag", shell_complete=complete_tag)],
):
    """Checkout a tag."""
    typer.echo(f"Checking out {tag}")
```

## Enabling Shell Completion

After implementing completion, enable it for your shell:

```bash
# Bash
eval "$(python -m mycli --show-completion bash)"

# Zsh
eval "$(python -m mycli --show-completion zsh)"

# Fish
python -m mycli --show-completion fish | source
```

Or add to your shell config file for permanent enabling.

## Completion for Multiple Values

```python
from typing import Annotated
import typer
from typer.shell_completion import CompletionItem

app = typer.Typer()

def complete_color(ctx: typer.Context, param: typer.Parameter, incomplete: str):
    """Complete color names."""
    colors = ["red", "green", "blue", "yellow", "cyan", "magenta", "white", "black"]
    for color in colors:
        if color.startswith(incomplete):
            yield CompletionItem(color)

@app.command()
def set_color(
    colors: Annotated[list[str], typer.Option("--color", shell_complete=complete_color)],
):
    """Set colors."""
    typer.echo(f"Colors: {', '.join(colors)}")

# python main.py set-color --color red --color blue
# Completes individual color values
```

## Case-Insensitive Completion

```python
from typing import Annotated
import typer
from typer.shell_completion import CompletionItem

app = typer.Typer()

def complete_framework(ctx: typer.Context, param: typer.Parameter, incomplete: str):
    """Complete framework names (case-insensitive)."""
    frameworks = [
        CompletionItem("Django"),
        CompletionItem("FastAPI"),
        CompletionItem("Flask"),
    ]
    for fw in frameworks:
        if fw.value.lower().startswith(incomplete.lower()):
            yield fw

@app.command()
def new(
    framework: Annotated[str, typer.Option(shell_complete=complete_framework)],
):
    """Create a new project."""
    typer.echo(f"Creating {framework} project")

# python main.py new D  # Completes Django
# python main.py new d  # Also completes Django
```

## Completion for Boolean Flags

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def build(
    debug: Annotated[bool, typer.Option("--debug/--no-debug")] = False,
    verbose: Annotated[bool, typer.Option("-v", "--verbose")] = False,
):
    """Build the project."""
    mode = "debug" if debug else "release"
    level = "verbose" if verbose else "normal"
    typer.echo(f"Building {mode} mode, {level} output")
```

## Key Points

- Typer automatically provides completion for standard types
- Use `CompletionItem` for custom completions with help text
- `shell_complete` function receives `ctx`, `param`, and `incomplete`
- Filter completions based on `incomplete` prefix
- Use `typer.CompletionType.FILE` for file path completion
- Use `typer.CompletionType.DIR` for directory completion
- Enable completion with `--show-completion` shell-name
- Completion works for both arguments and options
- Case-insensitive completion requires manual filtering in the completion function
