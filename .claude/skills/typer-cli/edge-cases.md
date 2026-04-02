# Edge Cases

Handling special input cases in Typer CLIs.

## Dash as Argument Value

The dash character `-` is treated as a literal value, not stdin:

```python
import typer

app = typer.Typer()

@app.command()
def test(value: str):
    """Test a value."""
    typer.echo(f"Value: {value}")

# python main.py test -     # value = "-"
# python main.py test --    # value = "--"
```

## Empty String

Handle empty string arguments:

```python
import typer

app = typer.Typer()

@app.command()
def process(name: str = ""):
    """Process with optional name."""
    if not name:
        typer.echo("No name provided!")
    else:
        typer.echo(f"Processing: {name}")

@app.command()
def optional_name(
    name: Annotated[str, typer.Argument()] = "",
):
    """Name can be empty."""
    if not name:
        typer.echo("Anonymous")
    else:
        typer.echo(f"Name: {name}")
```

## Unicode Input

Typer handles Unicode properly:

```python
import typer

app = typer.Typer()

@app.command()
def greet(name: str):
    """Greet with Unicode name."""
    typer.echo(f"Hello {name}!")

# python main.py greet "Japanese: 日本語"
# python main.py greet "French: Café"
# python main.py greet "German: Größe"
# python main.py greet "Emoji: 🎉"
```

## Very Long Arguments

Handle very long argument values:

```python
import typer

app = typer.Typer()

@app.command()
def analyze(text: str):
    """Analyze text input."""
    typer.echo(f"Length: {len(text)} characters")
    typer.echo(f"First 50 chars: {text[:50]}")
    typer.echo(f"Last 50 chars: {text[-50:]}")
```

## Special Characters in Arguments

```python
import typer

app = typer.Typer()

@app.command()
def search(query: str):
    """Search with special characters."""
    typer.echo(f"Searching for: {query}")
    typer.echo(f"Query repr: {query!r}")

# python main.py search "hello world"
# python main.py search 'hello "world"'
# python main.py search "hello's"
```

## Multiple Empty Arguments

```python
from typing import Annotated, Optional
import typer

app = typer.Typer()

@app.command()
def tags(
    tags: Annotated[Optional[list[str]], typer.Option("--tag")] = None,
):
    """Process tags."""
    tags = tags or []
    if not tags:
        typer.echo("No tags provided")
    else:
        for tag in tags:
            typer.echo(f"Tag: {tag}")

# python main.py tags --tag one --tag two
# python main.py tags                   # No tags
```

## Hyphen vs Dash in Paths

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def read(
    file: Annotated[typer.Path, typer.Argument()],
):
    """Read a file (hyphen in filename is literal)."""
    typer.echo(f"Reading: {file}")

# python main.py read my-file.txt  # Treats as literal "my-file.txt"
# python main.py read -            # Treated as stdin/stdout only with allow_dash=True
```

## Case Sensitivity

Options are case-sensitive by default:

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def config(
    level: Annotated[str, typer.Option("--level")] = "normal",
):
    """Case-sensitive option."""
    typer.echo(f"Level: {level}")

# python main.py config --level HIGH  # Sets level="HIGH"
# python main.py config --level high  # Sets level="low"
```

To make options case-insensitive:

```python
@app.command()
def config(
    level: Annotated[str, typer.Option("--level", case_sensitive=False)] = "normal",
):
    """Case-insensitive option."""
    level = level.lower()  # Normalize after parsing
    typer.echo(f"Level: {level}")

# python main.py config --level HIGH   # Sets level="high"
# python main.py config --level High   # Sets level="high"
```

## Zero as Default

```python
from typing import Annotated, Optional
import typer

app = typer.Typer()

@app.command()
def counter(
    count: Annotated[int, typer.Option("--count")] = 0,
):
    """Counter with zero default."""
    typer.echo(f"Count: {count}")
    for i in range(count):
        typer.echo(f"  Item {i}")

# python main.py counter                 # count = 0
# python main.py counter --count 5      # count = 5
```

## Negative Numbers

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def offset(
    value: Annotated[int, typer.Argument()],
    delta: Annotated[int, typer.Option("--delta")] = 0,
):
    """Handle negative numbers."""
    result = value + delta
    typer.echo(f"{value} + {delta} = {result}")

# python main.py offset -5 --delta -3
# -5 + -3 = -8
```

## Float Edge Cases

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def calculate(
    value: Annotated[float, typer.Argument()],
):
    """Handle float values."""
    typer.echo(f"Value: {value}")
    typer.echo(f"Is integer: {value.is_integer()}")
    typer.echo(f"Rounded: {round(value, 2)}")

# python main.py calculate 3.14159
# python main.py calculate .5          # 0.5
# python main.py calculate 5.         # 5.0
```

## Empty Files

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def validate(
    file: Annotated[typer.FileText, typer.Argument()],
):
    """Validate file content."""
    content = file.read()
    if not content:
        typer.echo("File is empty")
    else:
        typer.echo(f"Content length: {len(content)}")
```

## Key Points

- Dash `-` is treated as literal value unless `allow_dash=True`
- Empty strings are valid values, not `None`
- Typer handles Unicode correctly
- Use `case_sensitive=False` for case-insensitive options
- Negative numbers work correctly with `int` and `float` types
- Zero is a valid default value (not the same as not providing)
- Empty files return empty string content
