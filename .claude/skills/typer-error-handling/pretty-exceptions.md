# pretty_exceptions Configuration

Typer (via Click) supports several `pretty_exceptions_*` options for controlling exception formatting.

## Exception Configuration Options

```python
app = typer.Typer(
    context_settings={
        "pretty_exceptions_enable": True,        # Enable pretty tracebacks
        "pretty_exceptions_show_locals": True,    # Show local variables (SECURITY RISK!)
        "pretty_exceptions_short": False,         # Show full traceback (vs short)
        "pretty_exceptions_chain": True,          # Enable exception chaining
    }
)
```

| Option | Default | Purpose |
|--------|---------|---------|
| `pretty_exceptions_enable` | True in dev | Enable Rich-formatted tracebacks |
| `pretty_exceptions_show_locals` | False | Show local variables (SECURITY RISK in prod) |
| `pretty_exceptions_short` | True | Show short traceback (vs full) |
| `pretty_exceptions_chain` | False | Preserve exception chains |

## Security: pretty_exceptions_show_locals Dangers

### The Danger (CRITICAL)

**Never enable `pretty_exceptions_show_locals` in production.**

```python
# INSECURE - Never use in production
app = typer.Typer(
    context_settings={"pretty_exceptions_show_locals": True}
)

@app.command()
def process_payment(amount: float, card_number: str, cvv: str):
    # These sensitive values would appear in tracebacks!
    typer.echo(f"Processing ${amount}")
```

When an exception occurs with this setting, the traceback shows all local variables including `card_number` and `cvv`.

## Secure Configuration

```python
import os
import typer

def is_production() -> bool:
    return os.getenv("ENV", "development") == "production"

context_settings = {}
if not is_production():
    # Only enable pretty exceptions in development
    context_settings["pretty_exceptions_show_locals"] = True
    context_settings["pretty_exceptions_chain"] = True

app = typer.Typer(context_settings=context_settings)
```

## Environment-Based Security

```python
import os
import typer

app = typer.Typer()

@app.command(
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    }
)
def main(ctx: typer.Context):
    # In production, use clean error messages
    if is_production():
        ctx.pretty_exceptions = False
    typer.echo("Running...")
```

## Disabling Pretty Exceptions

```python
# Disable completely
app = typer.Typer(pretty_exceptions_enable=False)

# Only show in certain contexts
app = typer.Typer(
    context_settings={
        "pretty_exceptions_enable": True,
        "pretty_exceptions_short": True,
    }
)
```

## Best Practices for Sensitive Data

1. **Never enable `pretty_exceptions_show_locals` in production**
2. **Scrub sensitive values from error messages**
3. **Log errors with full context server-side, not client-side**
4. **Use structured logging that excludes sensitive fields**

```python
import logging
import re

logger = logging.getLogger(__name__)

def sanitize_error_message(message: str) -> str:
    """Remove sensitive patterns from error messages."""
    patterns = [
        r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',  # Card numbers
        r'\b\d{3,4}\b',  # CVV
        r'password=["\'][^"\']+["\']',  # Passwords in URLs
    ]
    result = message
    for pattern in patterns:
        result = re.sub(pattern, "[REDACTED]", result)
    return result

@app.command()
def sensitive_operation(token: str, data: str):
    try:
        process(token, data)
    except Exception as e:
        safe_message = sanitize_error_message(str(e))
        logger.error(f"Operation failed: {safe_message}")
        typer.echo("An error occurred. Contact support with reference: ERR-1234")
        raise typer.Exit(code=1)
```

See also:
- [environment-variables.md](environment-variables.md) - For TYPER_STANDARD_TRACEBACK
- [rich-errors.md](rich-errors.md) - For Rich error formatting
