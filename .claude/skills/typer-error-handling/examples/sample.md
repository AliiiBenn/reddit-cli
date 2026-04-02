# Typer Error Handling Example

**Scenario:** A CLI tool for managing a todo list with comprehensive error handling.

**File:** `todo_cli.py`

## Complete Implementation

```python
"""
Todo CLI - A Typer CLI application demonstrating proper error handling.
"""

import os
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

app = typer.Typer()
console = Console()

# Application-specific exit codes
EXIT_SUCCESS = 0
EXIT_GENERAL_ERROR = 1
EXIT_USAGE_ERROR = 2
EXIT_NOT_FOUND = 3
EXIT_ALREADY_EXISTS = 4


class TodoError(Exception):
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


def get_todo_file() -> Path:
    """Get the path to the todo database file."""
    return Path(os.getenv("TODO_FILE", ".todos.json"))


def load_todos() -> list[dict]:
    """Load todos from the file."""
    todo_file = get_todo_file()
    if not todo_file.exists():
        return []
    import json
    with open(todo_file) as f:
        return json.load(f)


def save_todos(todos: list[dict]) -> None:
    """Save todos to the file."""
    import json
    todo_file = get_todo_file()
    with open(todo_file, "w") as f:
        json.dump(todos, f, indent=2)


def validate_priority(priority: str) -> str:
    """Validate that priority is one of the allowed values."""
    valid_priorities = ["low", "medium", "high", "urgent"]
    if priority.lower() not in valid_priorities:
        raise InvalidPriorityError(priority)
    return priority.lower()


@app.command()
def add(
    title: str,
    priority: str = "medium",
    description: Optional[str] = None,
) -> None:
    """
    Add a new todo item.

    Example:
        todo add "Buy groceries" --priority high
    """
    try:
        priority = validate_priority(priority)
        todos = load_todos()

        # Check for duplicates
        if any(t["title"].lower() == title.lower() for t in todos):
            raise TodoAlreadyExistsError(title)

        todo = {
            "id": max([t["id"] for t in todos], default=0) + 1,
            "title": title,
            "description": description or "",
            "priority": priority,
            "completed": False,
        }

        todos.append(todo)
        save_todos(todos)

        priority_color = {
            "low": "green",
            "medium": "yellow",
            "high": "red",
            "urgent": "bold red",
        }.get(priority, "white")

        console.print(
            Panel(
                Text(f"Created todo #{todo['id']}", style="green"),
                title=f"[{priority_color}]{priority.upper()}[/{priority_color}]",
                subtitle=title,
            )
        )

    except TodoError as e:
        console.print(f"[red]Error:[/red] {e.message}", err=True)
        raise typer.Exit(code=e.code)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {type(e).__name__}: {e}", err=True)
        raise typer.Exit(code=EXIT_GENERAL_ERROR)


@app.command()
def list_cmd(
    all_items: bool = typer.Option(False, "--all", "-a", help="Show completed items too"),
    priority_filter: Optional[str] = typer.Option(None, "--priority", "-p", help="Filter by priority"),
) -> None:
    """
    List all todo items.

    Examples:
        todo list
        todo list --all
        todo list --priority high
    """
    try:
        todos = load_todos()

        if not todos:
            console.print("[yellow]No todos found[/yellow]")
            return

        # Apply filters
        if not all_items:
            todos = [t for t in todos if not t["completed"]]
        if priority_filter:
            priority_filter = validate_priority(priority_filter)
            todos = [t for t in todos if t["priority"] == priority_filter]

        if not todos:
            console.print("[yellow]No matching todos found[/yellow]")
            return

        # Display todos
        table = Table(title="Todo List")
        table.add_column("ID", style="cyan", width=4)
        table.add_column("Priority", style="bold", width=8)
        table.add_column("Title", style="white")
        table.add_column("Status", style="dim", width=10)

        priority_colors = {
            "low": "green",
            "medium": "yellow",
            "high": "red",
            "urgent": "bold red",
        }

        for todo in sorted(todos, key=lambda t: ["urgent", "high", "medium", "low"].index(t["priority"])):
            status = "[green]Done[/green]" if todo["completed"] else "[ ]"
            priority_style = priority_colors.get(todo["priority"], "white")

            table.add_row(
                str(todo["id"]),
                f"[{priority_style}]{todo['priority'].upper()}[/{priority_style}]",
                todo["title"],
                status,
            )

        console.print(table)
        console.print(f"\n[dim]Showing {len(todos)} item(s)[/dim]")

    except InvalidPriorityError as e:
        console.print(f"[red]Error:[/red] {e.message}", err=True)
        raise typer.Exit(code=e.code)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {type(e).__name__}: {e}", err=True)
        raise typer.Exit(code=EXIT_GENERAL_ERROR)


@app.command()
def complete(todo_id: int) -> None:
    """
    Mark a todo item as completed.

    Example:
        todo complete 1
    """
    try:
        todos = load_todos()

        todo = next((t for t in todos if t["id"] == todo_id), None)
        if not todo:
            raise TodoNotFoundError(todo_id)

        todo["completed"] = True
        save_todos(todos)

        console.print(
            f"[green]Completed:[/green] {todo['title']} (was: {todo['priority']})"
        )

    except TodoError as e:
        console.print(f"[red]Error:[/red] {e.message}", err=True)
        raise typer.Exit(code=e.code)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {type(e).__name__}: {e}", err=True)
        raise typer.Exit(code=EXIT_GENERAL_ERROR)


@app.command()
def delete(
    todo_id: int,
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
) -> None:
    """
    Delete a todo item.

    Examples:
        todo delete 1
        todo delete 1 --force
    """
    try:
        todos = load_todos()

        todo = next((t for t in todos if t["id"] == todo_id), None)
        if not todo:
            raise TodoNotFoundError(todo_id)

        if not force:
            console.print(f"Delete '[bold]{todo['title']}[/bold]'? (y/N) ", end="")
            if input().lower() != "y":
                console.print("[yellow]Cancelled[/yellow]")
                raise typer.Exit(code=EXIT_SUCCESS)

        todos = [t for t in todos if t["id"] != todo_id]
        save_todos(todos)

        console.print(f"[red]Deleted:[/red] {todo['title']}")

    except TodoError as e:
        console.print(f"[red]Error:[/red] {e.message}", err=True)
        raise typer.Exit(code=e.code)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {type(e).__name__}: {e}", err=True)
        raise typer.Exit(code=EXIT_GENERAL_ERROR)


if __name__ == "__main__":
    app()
```

## Usage Examples

### Adding a Todo

```bash
$ python todo_cli.py add "Buy groceries" --priority high
# Output: Rich-formatted panel showing todo creation
```

### Adding with Duplicate Title

```bash
$ python todo_cli.py add "Buy groceries"
# Error: Todo with title 'Buy groceries' already exists
# Exit code: 4
```

### Listing Todos

```bash
$ python todo_cli.py list
# Output: Rich table with all active todos
```

### Listing with Priority Filter

```bash
$ python todo_cli.py list --priority high
# Output: Rich table filtered to high priority todos
```

### Completing a Todo

```bash
$ python todo_cli.py complete 1
# Success message
```

### Completing Non-existent Todo

```bash
$ python todo_cli.py complete 999
# Error: Todo with ID 999 not found
# Exit code: 3
```

### Deleting with Confirmation

```bash
$ python todo_cli.py delete 1
# Delete 'Buy groceries'? (y/N)
# n
# Cancelled
```

### Deleting with Force Flag

```bash
$ python todo_cli.py delete 1 --force
# Deleted: Buy groceries
```

## Testing Error Handling

```python
"""tests/test_todo_cli.py"""
import pytest
from typer.testing import CliRunner
from todo_cli import app, EXIT_NOT_FOUND, EXIT_ALREADY_EXISTS, EXIT_USAGE_ERROR

runner = CliRunner()

def test_add_todo_success():
    result = runner.invoke(app, ["add", "Test todo", "--priority", "low"])
    assert result.exit_code == 0
    assert "Created todo" in result.output

def test_add_duplicate_returns_error_code():
    runner.invoke(app, ["add", "Duplicate test"])
    result = runner.invoke(app, ["add", "Duplicate test"])
    assert result.exit_code == EXIT_ALREADY_EXISTS
    assert "already exists" in result.output

def test_complete_nonexistent_returns_error():
    result = runner.invoke(app, ["complete", "9999"])
    assert result.exit_code == EXIT_NOT_FOUND
    assert "not found" in result.output

def test_invalid_priority_returns_usage_error():
    result = runner.invoke(app, ["add", "Test", "--priority", "invalid"])
    assert result.exit_code == EXIT_USAGE_ERROR
    assert "Invalid priority" in result.output

def test_list_empty_returns_success():
    result = runner.invoke(app, ["list"], env={"TODO_FILE": "/nonexistent/.todos"})
    assert result.exit_code == 0
    assert "No todos" in result.output

def test_delete_with_force_skips_confirmation():
    # First add a todo
    runner.invoke(app, ["add", "To delete"])
    # Delete with force
    result = runner.invoke(app, ["delete", "1", "--force"])
    assert result.exit_code == 0
    assert "Deleted" in result.output
```

## Error Flow Diagram

```
User Command
    │
    ▼
┌─────────────────┐
│ Parse Arguments │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Validate Input  │◄──── Invalid priority, missing args
└────────┬────────┘
         │ Valid
         ▼
┌─────────────────┐
│ Load Todos      │◄──── FileNotFoundError, PermissionError
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Execute Action  │◄──── TodoNotFoundError, TodoAlreadyExistsError
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Save Todos      │◄──── PermissionError, DiskFull
└────────┬────────┘
         │
         ▼
    Exit Code 0
```

## Key Error Handling Patterns Demonstrated

1. **Custom Exception Hierarchy** — `TodoError` base class with specific subclasses
2. **Application-Specific Exit Codes** — Defined constants for different error types
3. **Rich-Formatted Output** — Colored panels and tables for user-friendly errors
4. **Graceful Degradation** — Handles file not found, permission errors
5. **Security** — No sensitive data exposed in error messages
6. **Confirmation Prompts** — Destructive actions require explicit confirmation
7. **Testable Errors** — Each error case returns a specific, testable exit code
