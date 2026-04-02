# Custom Exception Classes

For application-specific exceptions, inherit from `TyperError` to integrate properly with Typer's error handling.

## Basic Custom Exception

```python
from typer import TyperError

# The base class for Typer exceptions
class AppError(TyperError):
    """Base exception for my app. Inherits from TyperError!"""
    def __init__(self, message: str, exit_code: int = 1):
        self.exit_code = exit_code
        super().__init__(message)
```

## Application-Specific Exceptions

```python
from typer import TyperError

class AppError(TyperError):
    """Base exception for mon app. Herite de TyperError!"""
    def __init__(self, message: str, exit_code: int = 1):
        self.exit_code = exit_code
        super().__init__(message)

class ValidationError(AppError):
    """Erreurs de validation."""
    def __init__(self, field: str, message: str):
        super().__init__(f"{field}: {message}", exit_code=2)

class NotFoundError(AppError):
    """Ressource non trouvee."""
    def __init__(self, resource: str, identifier: str):
        super().__init__(f"{resource} '{identifier}' not found", exit_code=3)

class AlreadyExistsError(AppError):
    """Ressource deja existante."""
    def __init__(self, resource: str, identifier: str):
        super().__init__(f"{resource} '{identifier}' already exists", exit_code=4)
```

## Important: Custom Exceptions Do NOT Auto-Exit

**Note:** These exceptions do NOT automatically call `SystemExit`! You must catch them and convert to `typer.Exit`:

```python
# Using custom exceptions properly
try:
    risky_operation()
except ValidationError as e:
    raise typer.Exit(f"Validation failed: {e}", code=e.exit_code, err=True)
```

## Complete Example with Custom Exceptions

```python
from typer import TyperError
import typer

app = typer.Typer()

# Application-specific exit codes
EXIT_SUCCESS = 0
EXIT_GENERAL_ERROR = 1
EXIT_USAGE_ERROR = 2
EXIT_NOT_FOUND = 3
EXIT_ALREADY_EXISTS = 4


class TodoError(TyperError):
    """Base exception for Todo CLI errors."""

    def __init__(self, message: str, code: int = EXIT_GENERAL_ERROR):
        self.message = message
        self.code = code
        super().__init__(message)


class TodoNotFoundError(TodoError):
    """Raised when a todo item is not found."""

    def __init__(self, todo_id: int):
        super().__init__(f"Todo with ID {todo_id} not found", code=EXIT_NOT_FOUND)


class TodoAlreadyExistsError(TodoError):
    """Raised when attempting to create a duplicate todo."""

    def __init__(self, title: str):
        super().__init__(f"Todo with title '{title}' already exists", code=EXIT_ALREADY_EXISTS)


class InvalidPriorityError(TodoError):
    """Raised when an invalid priority value is provided."""

    def __init__(self, priority: str):
        valid = ["low", "medium", "high", "urgent"]
        super().__init__(
            f"Invalid priority '{priority}'. Must be one of: {', '.join(valid)}",
            code=EXIT_USAGE_ERROR
        )


@app.command()
def add(title: str, priority: str = "medium"):
    try:
        if priority.lower() not in ["low", "medium", "high", "urgent"]:
            raise InvalidPriorityError(priority)

        todos = load_todos()

        if any(t["title"].lower() == title.lower() for t in todos):
            raise TodoAlreadyExistsError(title)

        # Create todo...
        typer.echo(f"Created: {title}")

    except TodoError as e:
        typer.echo(f"Error: {e.message}", err=True)
        raise typer.Exit(code=e.code)
```

## Using with Exception Chaining

```python
try:
    risky_operation()
except SomeError as e:
    raise TodoError(f"Operation failed: {e}") from e
```

See also:
- [exception-hierarchy.md](exception-hierarchy.md) - For TyperError hierarchy
- [exception-chaining.md](exception-chaining.md) - For exception chaining patterns
