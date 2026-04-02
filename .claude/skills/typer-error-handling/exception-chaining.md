# Exception Chaining with `raise ... from`

Preserve exception chains to maintain the full traceback context.

## Why Exception Chaining Matters

When re-raising exceptions, using `raise ... from e` preserves the original exception's traceback, which is critical for debugging.

## Anti-Pattern: Losing Traceback

```python
# BAD - Lose the exception context
try:
    risky_operation()
except SomeError:
    raise typer.Exit("Failed")  # Original traceback lost!

# Also BAD - bare raise loses context
try:
    risky_operation()
except SomeError:
    raise  # Loses context if not re-raising same exception
```

## Good Pattern: Preserve with `from`

```python
# GOOD - Preserve context with `from e`
try:
    risky_operation()
except SomeError as e:
    raise typer.Exit(f"Failed: {e}") from e  # Traceback preserved

# GOOD - For parameter errors, use BadParameter
try:
    validate_email(email)
except ValueError as e:
    raise typer.BadParameter(
        f"Invalid email: {e}",
        param_hint="email"
    ) from e
```

## Complete Example

```python
try:
    config = load_config(path)
except FileNotFoundError as e:
    raise typer.Exit(f"Config not found: {path}") from e

# More complete example with logging
try:
    config = load_config(config_path)
except FileNotFoundError as e:
    logger.error(f"Configuration file not found: {config_path}")
    raise typer.Exit(
        f"Error: Config '{config_path}' not found. "
        f"Use --config to specify a different location."
    ) from e
```

## Chaining with Custom Exceptions

```python
class AppError(TyperError):
    def __init__(self, message: str, code: int = 1):
        self.code = code
        super().__init__(message)

try:
    risky_operation()
except SomeError as e:
    raise AppError(f"Operation failed: {e}") from e

# Then catch and convert
try:
    do_work()
except AppError as e:
    raise typer.Exit(f"Error: {e}", code=e.code, err=True) from e
```

## Displaying Chained Exceptions

When using Rich for error display, you can show the full chain:

```python
from rich.console import Console

console = Console()

try:
    risky_operation()
except Exception as e:
    console.print(f"[red]Error:[/red] {e}")
    if e.__cause__:
        console.print(f"[dim]Caused by:[/dim] {e.__cause__}")
    raise typer.Exit(code=1)
```

## Best Practices

1. **Always use `raise ... from e`** when catching and re-raising with a different exception type
2. **Include the original error message** in the new exception when possible
3. **Log the original exception** before re-raising if you need to preserve it for debugging
4. **Use `raise ... from None`** to suppress the cause chain when the cause is not meaningful

```python
# Suppress the cause chain
try:
    risky_operation()
except SomeError:
    raise typer.Exit("Failed") from None
```

See also:
- [custom-exceptions.md](custom-exceptions.md) - For custom exception classes
- [logging.md](logging.md) - For logging integration
