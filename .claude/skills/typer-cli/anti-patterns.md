# Anti-Patterns

Common mistakes to avoid when building Typer CLIs.

## 1. Using `Optional` with Default Value

```python
# Bad - unnecessary Optional
from typing import Optional
import typer

app = typer.Typer()

@app.command()
def main(name: Optional[str] = "World"):
    print(f"Hello {name}")

# Good - direct type with default
from typing import Annotated
import typer

@app.command()
def main(name: Annotated[str, typer.Argument()] = "World"):
    print(f"Hello {name}")
```

## 2. Mixing Annotated and Non-Annotated Syntax

```python
# Bad - inconsistent style
from typing import Annotated
import typer

@app.command()
def main(name: str = typer.Argument()):  # Non-Annotated
    print(f"Hello {name}")

# Good - consistent Annotated style
from typing import Annotated
import typer

@app.command()
def main(name: Annotated[str, typer.Argument()]):
    print(f"Hello {name}")
```

## 3. Mutable Default Arguments

```python
# Bad - mutable default
import typer

app = typer.Typer()

@app.command()
def main(items: list = []):
    items.append("new")
    print(items)

# Good - None and create inside
from typing import Annotated, Optional
import typer

@app.command()
def main(items: Annotated[Optional[list[str]], typer.Option()] = None):
    items = items or []
    items.append("new")
    print(items)
```

## 4. Using `print()` Instead of `typer.echo()`

```python
# Bad - print doesn't handle Rich formatting properly
import typer

app = typer.Typer()

@app.command()
def status():
    print("Status: OK")  # Won't work well with Rich

# Good - typer.echo() handles all contexts
import typer

@app.command()
def status():
    typer.echo("Status: OK")
```

## 5. Not Checking `invoked_subcommand` with `invoke_without_command=True`

```python
# Bad - callback runs even when command is invoked
import typer

app = typer.Typer()

@app.callback(invoke_without_command=True)
def main():
    print("Initializing...")  # Runs for EVERY command

# Good - callback only runs when no command invoked
import typer

app = typer.Typer()

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        print("Initializing...")  # Only runs standalone
```

## 6. Missing Exit Code Checks in Tests

```python
# Bad - assumes success
from typer.testing import CliRunner

app = typer.Typer()

@app.command()
def create(name: str):
    print(f"Created: {name}")

runner = CliRunner()

def test_create():
    result = runner.invoke(app, ["create", "alice"])
    assert "Created" in result.output  # Exit code not checked!

# Good - always verify exit code
def test_create():
    result = runner.invoke(app, ["create", "alice"])
    assert result.exit_code == 0
    assert "Created" in result.output
```

## 7. Using Legacy Function Decorators

```python
# Bad - old decorator style
import typer

app = typer.Typer()

@app.command()
def create(name: str = typer.Argument()):
    print(f"Creating {name}")

# Good - modern Annotated style
from typing import Annotated
import typer

@app.command()
def create(name: Annotated[str, typer.Argument()]):
    print(f"Creating {name}")
```

## 8. Bare `return` in Command

```python
# Bad - bare return exits with code 0 (success)
import typer

app = typer.Typer()

@app.command()
def delete(name: str):
    if not name:
        return  # Exits with 0, implying success!
    print(f"Deleting {name}")

# Good - use typer.Exit with proper code or raise typer.Abort
import typer

@app.command()
def delete(name: str):
    if not name:
        typer.echo("Error: name required", err=True)
        raise typer.Exit(code=1)
    print(f"Deleting {name}")
```

## 9. Using `sys.exit()` Instead of `typer.Exit()`

```python
# Bad - sys.exit() bypasses Typer's error handling
import sys
import typer

app = typer.Typer()

@app.command()
def main():
    sys.exit(1)  # Doesn't allow Typer to clean up properly

# Good - use typer.Exit() for proper integration
import typer

@app.command()
def main():
    raise typer.Exit(code=1)
```

## 10. Global State Mutation in Callbacks

```python
# Bad - global state makes testing difficult
global_config = {"verbose": False}

app = typer.Typer()

@app.callback()
def main(verbose: bool = False):
    global_config["verbose"] = verbose  # Mutates global state

# Good - use Typer Context to pass state
import typer

app = typer.Typer()

@app.callback()
def main(ctx: typer.Context, verbose: bool = False):
    ctx.obj = {"verbose": verbose}  # Pass via context

@app.command()
def create(ctx: typer.Context, name: str):
    if ctx.obj and ctx.obj.get("verbose"):
        typer.echo(f"Creating {name}")
```

## 11. Modifying ctx.params Directly

```python
# Bad - ctx.params is read-only
import typer

app = typer.Typer()

@app.command()
def bad(ctx: typer.Context, name: str):
    ctx.params["name"] = "hack"  # ERROR - read-only

# Good - use ctx.obj for shared state
import typer

app = typer.Typer()

@app.callback()
def main(ctx: typer.Context):
    ctx.obj = {"counter": 0}
```

## 12. Bare return When Error Occurs

```python
# Bad - bare return on error still exits 0
import typer

app = typer.Typer()

@app.command()
def validate(name: str = ""):
    if not name:
        return  # Success exit code!
    print(f"Validating {name}")

# Good - explicit error handling
import typer

@app.command()
def validate(name: str = ""):
    if not name:
        typer.echo("Error: name required", err=True)
        raise typer.Exit(code=1)
    print(f"Validating {name}")
```

## 13. Mutable List Default with Options

```python
# Bad - list default is shared across calls
import typer

app = typer.Typer()

@app.command()
def add_tags(tags: list[str] = []):
    tags.append("new")
    print(tags)

# Good - use None and create fresh list
from typing import Annotated, Optional
import typer

@app.command()
def add_tags(tags: Annotated[Optional[list[str]], typer.Option()] = None):
    tags = tags or []
    tags.append("new")
    print(tags)
```

## 14. Not Using `rich_markup_mode` for Rich Formatting

```python
# Bad - raw markup shown in help
import typer

app = typer.Typer()

@app.command()
def create(name: str):
    """Create a **new** user account."""
    typer.echo(f"Creating: {name}")

# Good - markup rendered properly
import typer

app = typer.Typer(rich_markup_mode="markdown")

@app.command()
def create(name: str):
    """Create a **new** user account."""
    typer.echo(f"Creating: {name}")
```

## 15. Forgetting to Handle Empty Input in Prompts

```python
# Bad - empty prompt input not handled
import typer

app = typer.Typer()

@app.command()
def setup():
    name = typer.prompt("Enter name")
    typer.echo(f"Hello {name}")  # Fails if empty

# Good - explicit empty handling
import typer

app = typer.Typer()

@app.command()
def setup():
    name = typer.prompt("Enter name", default="Anonymous")
    if not name:
        name = "Anonymous"
    typer.echo(f"Hello {name}")
```

## Key Points

- Always use `Annotated` syntax for arguments and options
- Never use mutable defaults (use `None` + create inside)
- Always use `typer.echo()` instead of `print()`
- Always check exit codes in tests
- Use `ctx.obj` for shared state, not global variables
- Never modify `ctx.params` directly
- Use `typer.Exit()` instead of `sys.exit()`
- Handle empty input explicitly in prompts
