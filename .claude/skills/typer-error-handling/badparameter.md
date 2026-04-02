# BadParameter with param_hint

Use `BadParameter` with `param_hint` to indicate which parameter failed validation.

## Basic Usage

```python
from typer import BadParameter

@app.command()
def validate_email(email: str):
    if "@" not in email:
        raise BadParameter(
            "Invalid email format",
            param_hint="email"
        )
    typer.echo(f"Email: {email}")
```

## The param_hint Parameter

The `param_hint` parameter indicates which parameter failed validation:

```python
def validate_email(email: str):
    if "@" not in email:
        raise BadParameter(
            f"Invalid email format: {email}",
            param_hint="email"  # Shows which parameter
        )
    return email

# Without param_hint:
# Error: Invalid email format: bad-email

# With param_hint:
# Error: Invalid email format: bad-email
# Parameter: email
```

## Multiple Parameters

When validation involves multiple parameters:

```python
raise BadParameter("Invalid combination", param_hint=["start", "end"])
```

## Displaying BadParameter Errors

```python
try:
    raise BadParameter("Invalid", param_hint="field")
except BadParameter as e:
    typer.echo(f"Error: {e}", err=True)
    if e.param_hint:
        typer.echo(f"Parameter: {e.param_hint}", err=True)
```

## Using in Callbacks

```python
def validate_env(env: str, ctx: typer.Context) -> str:
    """Validate environment parameter."""
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

## Using with Custom Parsers

```python
def parse_port(value: str) -> int:
    """Parse and validate a port number."""
    try:
        port = int(value)
    except ValueError:
        raise BadParameter("Port must be a number", param_hint="port")
    if not 1 <= port <= 65535:
        raise BadParameter(
            f"Port must be between 1 and 65535, got {port}",
            param_hint="port"
        )
    return port

@app.command()
def serve(
    port: Annotated[int, typer.Option(parser=parse_port)] = 8080,
):
    """Start the server on a specific port."""
```

## Validation with Age Example

```python
def validate_age(age: str, ctx: typer.Context, param: typer.Parameter):
    """Validate age parameter."""
    try:
        age_int = int(age)
    except ValueError:
        raise typer.BadParameter("Age must be a number", param_hint="age")
    if not 0 <= age_int <= 150:
        raise typer.BadParameter("Age must be between 0 and 150", param_hint="age")
    return age_int

@app.command()
def register(
    age: Annotated[int, typer.Option(callback=validate_age)],
):
    """Register a user."""
    typer.echo(f"Registering user with age: {age}")
```

See also:
- [validation-patterns.md](validation-patterns.md) - For converter vs callback vs validator patterns
- [exception-chaining.md](exception-chaining.md) - For preserving exception context
