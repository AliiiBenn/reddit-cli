# Environment Variables

Typer supports reading options from environment variables.

## Basic Environment Variable

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def config(
    token: Annotated[str, typer.Option(envvar="API_TOKEN")],
):
    """Use API token from environment variable."""
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

# python main.py                          # Requires one of the env vars
# TOKEN=fallback python main.py            # Uses TOKEN
# AUTH_TOKEN=primary python main.py         # Uses AUTH_TOKEN
```

## Environment Variable Precedence

```
CLI argument > Environment variable > Default value
```

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def config(
    verbose: Annotated[bool, typer.Option("--verbose", envvar="VERBOSE")] = False,
):
    """Precedence: CLI > env var > default"""
    if verbose:
        typer.echo("Verbose mode enabled")
    else:
        typer.echo("Verbose mode disabled")
```

## Hide Environment Variable in Help

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
    typer.echo(f"Secret configured, public key: {public}")

# --secret TEXT                    # No env var shown
# --public TEXT  [default: default] (or from PUBLIC_KEY)  # Env var shown
```

**Use when:** Some environment variables are internal/implementation details and should not be exposed to users.

## Boolean Environment Variable

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def debug(
    debug: Annotated[bool, typer.Option("--debug", envvar="DEBUG")] = False,
):
    """Debug mode from environment."""
    if debug:
        typer.echo("Debug mode is ON")
    else:
        typer.echo("Debug mode is OFF")

# DEBUG=1 python main.py           # debug = True
# DEBUG=true python main.py        # debug = True
# DEBUG=0 python main.py           # debug = False
```

## Integer Environment Variable

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def serve(
    port: Annotated[int, typer.Option(envvar="PORT")] = 8080,
):
    """Server port from environment."""
    typer.echo(f"Starting server on port {port}")

# python main.py                           # Uses default 8080
# PORT=3000 python main.py                 # Uses 3000
```

## List Environment Variable

```python
from typing import Annotated, Optional
import typer

app = typer.Typer()

@app.command()
def install(
    packages: Annotated[Optional[list[str]], typer.Option(envvar="PACKAGES")] = None,
):
    """Install packages from environment."""
    packages = packages or []
    for pkg in packages:
        typer.echo(f"Installing {pkg}...")

# PACKAGES="numpy,pandas" python main.py
# Or with multiple --package flags:
# python main.py --package numpy --package pandas
```

## Environment Variable with Prompt

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def setup(
    api_key: Annotated[
        str,
        typer.Option(
            envvar="API_KEY",
            prompt="Enter your API key",
            help="API key for the service",
        ),
    ],
):
    """Setup with environment variable or prompt."""
    typer.echo(f"API key configured: {api_key[:4]}...")

# python main.py                           # Prompts for API key
# API_KEY=secret python main.py             # Uses secret from env var
```

## App-Level Environment Variables

Set environment variables at the app level with callback:

```python
import typer

app = typer.Typer()

@app.callback()
def main(
    ctx: typer.Context,
    config_path: Annotated[str, typer.Option(envvar="CONFIG_PATH")] = "config.yaml",
    log_level: Annotated[str, typer.Option(envvar="LOG_LEVEL")] = "INFO",
):
    """Main application with env var configuration."""
    import os
    os.environ["CONFIG_PATH"] = config_path
    os.environ["LOG_LEVEL"] = log_level
    ctx.obj = {"config": config_path, "log_level": log_level}

@app.command()
def status(ctx: typer.Context):
    """Show status with configured values."""
    typer.echo(f"Config: {ctx.obj['config']}")
    typer.echo(f"Log level: {ctx.obj['log_level']}")
```

## Key Points

- `envvar="NAME"` reads from environment variable `NAME`
- Multiple envvars as fallback: `envvar=["VAR1", "VAR2", "VAR3"]`
- Precedence: CLI argument > env var > default
- `show_envvar=False` hides env var from help output
- Boolean env vars accept "0", "1", "true", "false" (case insensitive)
- Integer, string, and list types work with env vars
- Use callback to set app-level environment variables
