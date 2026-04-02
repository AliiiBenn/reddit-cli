# Template: Typer Error Handling Skill

**Date:** YYYY-MM-DD

**Author:** [Author Name]

**Status:** Draft / In Review / Approved

---

## Quick Usage

```bash
# Invoke this skill when working with:
# - Exception handling in Typer apps
# - Exit code management
# - User-friendly error messages
# - Debugging Typer errors

# Check exit codes in tests
grep -rn "exit_code" tests/ --include="*.py"

# Find exception handling patterns
grep -rn "typer.Exit\|typer.Abort\|raise" app/ --include="*.py"

# Find rich formatting in errors
grep -rn "typer.style\|rich\|富" app/ --include="*.py"
```

## Overview

[Describe error handling philosophy and approach for Typer CLI applications. What are the three complementary mechanisms? Why do they matter?]

## Topics

### Exit Codes
- [exit-codes.md](exit-codes.md) - Exit code conventions
- [typer-exit.md](typer-exit.md) - typer.Exit() usage
- [typer-abort.md](typer-abort.md) - typer.Abort() usage
- [typer-interrupt.md](typer-interrupt.md) - TyperInterrupt handling
- [system-exit.md](system-exit.md) - SystemExit vs typer.Exit

### Exceptions
- [exception-hierarchy.md](exception-hierarchy.md) - Exception hierarchy
- [click-compatibility.md](click-compatibility.md) - Click compatibility
- [custom-exceptions.md](custom-exceptions.md) - Custom exception classes
- [badparameter.md](badparameter.md) - BadParameter with param_hint
- [validation-patterns.md](validation-patterns.md) - converter vs callback vs validator
- [exception-chaining.md](exception-chaining.md) - raise ... from e

### Rich Formatting
- [rich-errors.md](rich-errors.md) - Rich error formatting
- [secho-style.md](secho-style.md) - typer.secho(), typer.style()

### Configuration
- [pretty-exceptions.md](pretty-exceptions.md) - pretty_exceptions configuration
- [environment-variables.md](environment-variables.md) - TYPER_STANDARD_TRACEBACK, etc.

### Best Practices
- [logging.md](logging.md) - Logging integration
- [context-managers.md](context-managers.md) - Resource cleanup

### Reference
- [reference-card.md](reference-card.md) - Reference card
- [examples/sample.md](examples/sample.md) - Complete example

## Quick Usage Patterns

```python
# Exit with error to stderr
raise typer.Exit("Error message", code=1, err=True)

# Abort (shows "Aborted!")
raise typer.Abort()

# BadParameter for validation
raise BadParameter("Invalid value", param_hint="param_name")

# Custom exception
class AppError(TyperError):
    def __init__(self, message: str, code: int = 1):
        super().__init__(message)
        self.code = code
```

## Good/Bad Code Examples

### Good: Explicit Exit Codes

```python
import typer

app = typer.Typer()

@app.command()
def create(name: str, email: str):
    if not name:
        typer.echo("Error: Name is required", err=True)
        raise typer.Exit(code=2)

    if not email or "@" not in email:
        typer.echo("Error: Valid email is required", err=True)
        raise typer.Exit(code=2)

    user = db.create(name=name, email=email)
    typer.echo(f"Created user {user.id}")
```

### Bad: Silent Failures

```python
@app.command()
def create(name: str, email: str):
    # Bad: No validation, silent failure if email invalid
    user = db.create(name=name, email=email)
    typer.echo("Done")
```

### Good: User-Friendly Error Messages

```python
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

@app.command()
def deploy(environment: str):
    valid_environments = ["dev", "staging", "production"]

    if environment not in valid_environments:
        panel = Panel(
            Text(f"Invalid environment: '{environment}'", style="red"),
            title="Deployment Error",
            subtitle=f"Valid options: {', '.join(valid_environments)}"
        )
        console.print(panel)
        raise typer.Exit(code=2)
```

### Bad: Cryptic Error Messages

```python
@app.command()
def deploy(environment: str):
    # Bad: Non-descriptive error
    if environment not in ["dev", "staging", "production"]:
        raise typer.Exit("Invalid env")  # Unhelpful!
```

### Good: Graceful Degradation

```python
@app.command()
def fetch_data(url: str):
    try:
        data = remote_api.fetch(url)
        typer.echo(f"Fetched {len(data)} bytes")
    except ConnectionError:
        typer.echo("Warning: Could not connect to remote API", err=True)
        typer.echo("Using cached data instead...")
        data = local_cache.get(url)
        if data is None:
            typer.echo("Error: No cached data available", err=True)
            raise typer.Exit(code=1)
    except TimeoutError:
        typer.echo("Warning: Request timed out", err=True)
        typer.echo("Retrying with shorter timeout...")
        data = remote_api.fetch(url, timeout=5)
```

### Bad: Unhandled Exceptions

```python
@app.command()
def fetch_data(url: str):
    # Bad: No exception handling
    data = remote_api.fetch(url)  # Could raise unhandled exceptions
    typer.echo(f"Fetched {len(data)} bytes")
```

### Good: Structured Logging

```python
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)

@app.command()
def risky_operation(config_path: str):
    try:
        config = load_config(config_path)
        execute(config)
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        typer.echo("Error: Configuration file missing", err=True)
        raise typer.Exit(code=2)
    except PermissionError:
        logger.error(f"Permission denied: {config_path}")
        typer.echo("Error: Cannot read configuration", err=True)
        raise typer.Exit(code=2)
    except Exception as e:
        logger.exception("Unexpected error during execution")
        typer.echo("Error: An unexpected error occurred", err=True)
        raise typer.Exit(code=1)
```

### Bad: Exposing Internal Details

```python
@app.command()
def risky_operation(config_path: str):
    try:
        config = load_config(config_path)
        execute(config)
    except Exception as e:
        # Bad: Exposes internal implementation details
        typer.echo(f"Error in {__name__}.load_config: {e}")
        raise typer.Exit(code=1)
```

## Anti-Patterns

### 1. Exit Code 0 on Failure

```python
# Bad - Misleading exit code
@app.command()
def delete(name: str):
    if not exists(name):
        typer.echo("User not found")  # Still exits with 0!
    delete_user(name)

# Good - Proper non-zero exit code
@app.command()
def delete(name: str):
    if not exists(name):
        typer.echo("Error: User not found", err=True)
        raise typer.Exit(code=3)
    delete_user(name)
```

### 2. Generic Catch-All

```python
# Bad - Too broad exception handling
@app.command()
def process(data: str):
    try:
        result = complex_processing(data)
    except Exception:
        typer.echo("An error occurred")
        raise typer.Exit(code=1)
```

### 3. Swallowing Exceptions

```python
# Bad - Silent failure
@app.command()
def process(data: str):
    try:
        result = risky_operation(data)
    except Exception:
        pass  # Silent failure!
```

### 4. Inconsistent Error Messages

```python
# Bad - Inconsistent error formats
@app.command()
def create_user(name: str):
    if not name:
        raise typer.Exit("ERR: Name required")  # Mixed format
    if len(name) < 2:
        typer.echo("Error: Name too short")  # Different format

# Good - Consistent error format
@app.command()
def create_user(name: str):
    if not name:
        raise typer.Exit("Error: Name is required", code=2)
    if len(name) < 2:
        raise typer.Exit("Error: Name must be at least 2 characters", code=2)
```

### 5. Missing Error Context

```python
# Bad - No actionable information
@app.command()
def process_file(path: str):
    try:
        data = read_file(path)
    except Exception:
        typer.echo("Error reading file")
        raise typer.Exit(code=1)

# Good - Context and recovery suggestions
@app.command()
def process_file(path: str):
    try:
        data = read_file(path)
    except FileNotFoundError:
        typer.echo(f"Error: File not found: {path}", err=True)
        typer.echo("Hint: Verify the file exists and the path is correct")
        raise typer.Exit(code=2)
    except PermissionError:
        typer.echo(f"Error: Permission denied: {path}", err=True)
        typer.echo("Hint: Check file permissions with 'ls -la'")
        raise typer.Exit(code=2)
```

## Best Practices

### Exit Code Best Practices

- **Use 0 for success** - Never return 0 for error conditions
- **Use 1 for general errors** - Catch-all for unexpected failures
- **Use 2 for usage errors** - Invalid arguments or command misuse
- **Use 125 for unknown options** - `NoSuchOption`
- **Use 127 for missing executables** - subprocess not found
- **Use 130 for user interruption** - `TyperInterrupt`, Ctrl+C
- **Use 3+ for application-specific errors** - Document your codes
- **Be consistent** - Same error should always return same code

### Error Message Best Practices

1. **Be specific** - Include the actual values that caused the error
2. **Be actionable** - Tell users what to do to fix it
3. **Be proportionate** - Don't overwhelm with technical details
4. **Use Rich formatting** - Color and structure aid comprehension
5. **Log everything, show summary** - Full details to logs, brief to user
6. **Use `err=True`** - Send errors to stderr, not stdout

### Exception Handling Best Practices

1. **Handle exceptions at appropriate levels** - Don't catch what you can't handle
2. **Preserve exception context** - Use `raise ... from` when re-raising
3. **Clean up resources** - Use `finally` or context managers
4. **Don't expose sensitive data** - Scrub credentials from messages
5. **Test error paths** - Verify exit codes and messages in tests
6. **Inherit from TyperError** - For custom exceptions that integrate with Typer

## Testing Error Handling

```python
from typer.testing import CliRunner

runner = CliRunner()

def test_missing_required_argument():
    result = runner.invoke(app, [])
    assert result.exit_code == 2
    assert "required" in result.output.lower()

def test_invalid_option():
    result = runner.invoke(app, ["--invalid-flag"])
    assert result.exit_code == 2
    assert "no such option" in result.output.lower()

def test_validation_error():
    result = runner.invoke(app, ["create", "--email", "invalid"])
    assert result.exit_code == 2
    assert "email" in result.output.lower()

def test_not_found_error():
    result = runner.invoke(app, ["delete", "nonexistent"])
    assert result.exit_code == 3  # Custom code for not found
    assert "not found" in result.output.lower()

def test_permission_error():
    result = runner.invoke(app, ["read", "/root/restricted"])
    assert result.exit_code == 2
    assert "permission" in result.output.lower()

def test_user_interrupt():
    result = runner.invoke(app, [], input="\x03")  # Ctrl+C
    assert result.exit_code == 130
```

## Environment-Aware Error Handling

```python
import os
import typer

app = typer.Typer()

def is_verbose() -> bool:
    return os.getenv("VERBOSE", "").lower() in ("1", "true", "yes")

@app.command()
def process(data: str):
    try:
        result = risky_operation(data)
        typer.echo(f"Result: {result}")
    except AppError as e:
        if is_verbose():
            typer.echo(f"[verbose] Full error: {e}", err=True)
        else:
            typer.echo(f"Error: {e.user_message}", err=True)
        raise typer.Exit(code=e.code)
    except Exception as e:
        logger.exception("Unexpected error")
        typer.echo("An unexpected error occurred", err=True)
        if is_verbose():
            typer.echo(f"[verbose] {type(e).__name__}: {e}", err=True)
        raise typer.Exit(code=1)
```

## Senior Advice

> "[Quote about error handling]"

> "[Quote about exit codes]"

> "[Quote about security and usability]"

## Additional Resources

- [Typer Exceptions Documentation](https://typer.tiangolo.com/tutorial/exceptions/)
- [Typer Terminating Documentation](https://typer.tiangolo.com/tutorial/terminating/)
- [Click Exception Handling](https://click.palletsprojects.com/en/stable/exceptions/)
- [Rich Console Errors](https://rich.readthedocs.io/en/latest/console.html#console-print)
- [CLI Error Handling Best Practices](https://clig.dev/#error-handling)
