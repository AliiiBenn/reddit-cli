# Typer Exception Hierarchy

## Two Distinct Hierarchies

Typer has two separate exception hierarchies that serve different purposes:

### SystemExit Hierarchy (Terminating)

```
Exception (base)
└── SystemExit
    ├── typer.Exit        # Program termination (code=0 by default)
    └── typer.Abort       # Fatal termination (code=1)
```

These bypass normal exception handling and directly terminate the program.

### TyperError Hierarchy (Parameter/Validation)

```
TyperError (base class for parameter/validation errors)
├── BadParameter          # Invalid parameter value
├── MissingOption         # Required option not provided
├── MissingArgument       # Required argument not provided
├── NoSuchOption          # Unknown option
├── ValidationError       # General validation failure
└── TyperInterrupt        # User interrupted (Ctrl+C) - exit code 130
```

## TyperError Base Class

`TyperError` is the base class for all parameter and validation errors in Typer:

```python
from typer import TyperError

class AppError(TyperError):
    """Base exception for application errors."""
    def __init__(self, message: str, code: int = 1):
        self.code = code
        super().__init__(message)
```

## Built-in Exceptions

### BadParameter

Raised when a parameter value is invalid:

```python
from typer import BadParameter

@app.command()
def validate_email(email: str):
    if "@" not in email:
        raise BadParameter(
            "Invalid email format",
            param_hint="email"
        )
```

### MissingOption

Raised when a required option is not provided:

```python
# python main.py create --name test
# MissingOption: 'email' option is required
# Exit code: 2
```

### MissingArgument

Raised when a required argument is not provided:

```python
@app.command()
def create(name: str):  # name is REQUIRED
    pass

# python main.py create
# MissingArgument: 'name' is a required argument
# Exit code: 2
```

### NoSuchOption

Raised when an unknown option is used:

```python
# python main.py create --invalid-flag
# NoSuchOption: 'invalid-flag'
# Exit code: 125
```

### ValidationError

Raised for general validation failures:

```python
from typer import ValidationError

@app.command()
def validate_age(age: int):
    if age < 0 or age > 150:
        raise ValidationError(f"Age must be between 0 and 150, got {age}")
```

## Exit Code Mapping

| Exception | Exit Code | Use Case |
|-----------|-----------|----------|
| `typer.Exit` | configurable | Clean exit with code |
| `typer.Abort` | 1 | Fatal error, shows "Aborted!" |
| `TyperInterrupt` | 130 | Ctrl+C |
| `TyperError` (base) | - | Base for custom errors |
| `BadParameter` | 2 | Invalid parameter value |
| `MissingOption` | 2 | Required option not provided |
| `MissingArgument` | 2 | Required argument not provided |
| `NoSuchOption` | 125 | Unknown option |
| `ValidationError` | 2 | General validation failure |

See also:
- [badparameter.md](badparameter.md) - For BadParameter with param_hint
- [custom-exceptions.md](custom-exceptions.md) - For creating custom exceptions
- [click-compatibility.md](click-compatibility.md) - For Click exception compatibility
