# Reference Card: Typer Error Handling

## Exit Codes

| Code | Name | Common Cause |
|------|------|--------------|
| 0 | Success | Normal completion |
| 1 | General error | `typer.Abort()`, unspecified |
| 2 | Usage error | `BadParameter`, `MissingOption`, `MissingArgument` |
| 125 | Unknown option | `NoSuchOption` |
| 126 | Not executable | Command `Invoke` failure |
| 127 | Not found | Missing executable (subprocess) |
| 130 | Interrupted | `TyperInterrupt`, `KeyboardInterrupt` |

## Typer Exceptions

| Exception | Base | Exit Code | Use Case |
|-----------|------|-----------|----------|
| `typer.Exit` | `SystemExit` | configurable | Clean exit with code |
| `typer.Abort` | `SystemExit` | 1 | Fatal error, shows "Aborted!" |
| `TyperInterrupt` | `BaseException` | 130 | Ctrl+C |
| `TyperError` | `Exception` | - | Base for custom errors |
| `BadParameter` | `TyperError` | 2 | Invalid parameter value |
| `MissingOption` | `TyperError` | 2 | Required option not provided |
| `MissingArgument` | `TyperError` | 2 | Required argument not provided |
| `NoSuchOption` | `TyperError` | 125 | Unknown option |
| `ValidationError` | `TyperError` | 2 | General validation failure |

## Key Patterns

### Exit with error to stderr
```python
raise typer.Exit("Error message", code=1, err=True)
```

### Exit with error to stdout (usually wrong)
```python
raise typer.Exit("Error message", code=1)  # Goes to stdout!
```

### Abort (shows "Aborted!")
```python
raise typer.Abort()  # No custom message allowed!
```

### BadParameter for parameter validation
```python
raise BadParameter("Invalid value", param_hint="param_name")
```

### Custom error inheriting from TyperError
```python
class AppError(TyperError):
    def __init__(self, message: str, code: int = 1):
        super().__init__(message)
        self.code = code
```

### Exception chaining
```python
raise typer.Exit(f"Failed: {e}") from e
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `TYPER_STANDARD_TRACEBACK` | Full traceback mode |
| `TYPER_USE_RICH` | Disable Rich |
| `TYPER_COLOR_SYSTEM` | Force color output |
| `TYPER_terminal_columns` | Override terminal width |
| `TYPER_terminal_rows` | Override terminal height |

## pretty_exceptions Options

| Option | Default | Purpose |
|--------|---------|---------|
| `pretty_exceptions_enable` | True in dev | Enable Rich tracebacks |
| `pretty_exceptions_show_locals` | False | Show local variables (SECURITY RISK!) |
| `pretty_exceptions_short` | True | Short vs full traceback |
| `pretty_exceptions_chain` | False | Preserve exception chains |

## Quick Decision Guide

### Which exit mechanism to use?

| Scenario | Use |
|----------|-----|
| Clean success | `return` or `raise typer.Exit(code=0)` |
| Error with message | `raise typer.Exit("msg", code=X, err=True)` |
| Fatal error, no message | `raise typer.Abort()` |
| Ctrl+C handling | `raise typer.TyperInterrupt()` |

### Which validation to use?

| Need | Use |
|------|-----|
| Simple transformation | `converter=` |
| Complex validation | `callback=` |
| Type parsing | `parser=` |
| Parameter hint | `BadParameter(..., param_hint="name")` |
