# Validation Patterns

Typer provides three mechanisms for parameter validation: `converter`, `callback`, and `parser`.

## converter - Simple Input Transformation

The `converter` parameter transforms input and can raise `BadParameter`:

```python
def lowercase(value: str) -> str:
    """Convert to lowercase."""
    return value.lower()

@app.command()
def create(
    name: Annotated[str, typer.Option(converter=lowercase)],
):
    """Converter is called automatically."""
    typer.echo(f"Name: {name}")

# python main.py create --name "ALICE"
# name = "alice"
```

## callback - Complex Validation with Context

The `callback` parameter allows complex validation with access to the Typer context:

```python
def validate_env(env: str, ctx: typer.Context) -> str:
    """Validate and can access context."""
    if ctx.resilient_parsing:
        return env  # Skip during completion
    if env not in ("dev", "prod", "staging"):
        raise BadParameter(
            f"Must be dev/prod/staging, got '{env}'",
            param_hint="env"
        )
    return env

@app.command()
def deploy(
    env: Annotated[str, typer.Option(callback=validate_env)],
):
    """Deploy to environment."""
```

## parser - Custom Type Parsing

The `parser` parameter is similar to `callback` but specifically for type conversion:

```python
def parse_port(value: str) -> int:
    """Parse and validate a port number."""
    try:
        port = int(value)
    except ValueError:
        raise BadParameter("Port must be a number", param_hint="port")
    if not 1 <= port <= 65535:
        raise BadParameter(
            f"Port must be 1-65535, got {port}",
            param_hint="port"
        )
    return port

@app.command()
def serve(
    port: Annotated[int, typer.Option(parser=parse_port)] = 8080,
):
    """Start server on port."""
```

## Comparison Table

| Feature | converter | callback | parser |
|---------|-----------|----------|--------|
| Type transformation | Yes | Yes | Yes |
| Access to context | No | Yes | No |
| Access to parameter info | No | Yes | No |
| Can raise BadParameter | Yes | Yes | Yes |
| Called during completion | Yes | Only if resilient_parsing | Yes |
| Recommended for | Simple transforms | Complex validation | Type parsing |

## validator - Pure Validation

Similar to `callback` but intended for pure validation logic:

```python
def validate_port(port: int) -> int:
    """Validate port range."""
    if port < 1 or port > 65535:
        raise BadParameter(
            f"Port must be 1-65535, got {port}",
            param_hint="port"
        )
    return port

@app.command()
def serve(
    port: Annotated[int, typer.Option(callback=validate_port)],
):
    """Start server on port."""
```

## When to Use Each

### Use converter when:
- Simple lowercase/uppercase transformation
- Stripping whitespace
- Simple type conversions

### Use callback when:
- Validation depends on other parameters
- Access to context is needed
- Complex validation logic
- Need to check `ctx.resilient_parsing`

### Use parser when:
- Custom type parsing from string
- Combined parsing and validation

## Complete Example

```python
from typing import Annotated
import typer
from typer import BadParameter

app = typer.Typer()


def normalize_name(name: str) -> str:
    """Normalize name input."""
    return name.strip().lower()


def validate_email(email: str, ctx: typer.Context) -> str:
    """Validate email with context access."""
    if ctx.resilient_parsing:
        return email
    if "@" not in email:
        raise BadParameter(
            f"Invalid email format: {email}",
            param_hint="email"
        )
    return email.lower()


@app.command()
def create(
    name: Annotated[str, typer.Option(converter=normalize_name)],
    email: Annotated[str, typer.Option(callback=validate_email)],
):
    """Create a new user."""
    typer.echo(f"Created user: {name} ({email})")
```

See also:
- [badparameter.md](badparameter.md) - For BadParameter with param_hint
- [exception-chaining.md](exception-chaining.md) - For preserving exception context
