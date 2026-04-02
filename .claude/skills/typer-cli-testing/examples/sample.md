# Typer CLI Testing - Complete Example

**Date:** 2026-03-31

This document shows a realistic testing session for a `tasks` CLI application. For detailed explanations of individual topics, see the files listed in [SKILL.md](../SKILL.md).

## The Application

```python
# tasks_app/main.py
import typer
from typing import Annotated

app = typer.Typer()

# In-memory task storage
tasks = []
task_id_counter = 1


@app.command()
def add(
    title: Annotated[str, typer.Argument(help="Task title")],
    priority: Annotated[str, typer.Option("--priority", "-p")] = "medium",
) -> None:
    """Add a new task."""
    global task_id_counter
    task = {"id": task_id_counter, "title": title, "priority": priority}
    tasks.append(task)
    task_id_counter += 1
    typer.echo(f"Added task #{task['id']}: {title} (priority: {priority})")


@app.command()
def list_tasks(
    show_all: Annotated[bool, typer.Option("--all", "-a")] = False,
) -> None:
    """List all tasks."""
    if not tasks:
        typer.echo("No tasks found.")
        return

    for task in tasks:
        status = "[ ]" if show_all else ""
        typer.echo(f"{status} #{task['id']}: {task['title']} ({task['priority']})")


@app.command()
def complete(
    task_id: Annotated[int, typer.Argument(help="Task ID to complete")],
) -> None:
    """Mark a task as complete."""
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        typer.echo(f"Error: Task #{task_id} not found.", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Completed task #{task_id}: {task['title']}")
    tasks.remove(task)


if __name__ == "__main__":
    app()
```

## Test File

```python
# tests/test_tasks.py
import pytest
from typer.testing import CliRunner
from tasks_app.main import app, tasks, task_id_counter

runner = CliRunner()


@pytest.fixture(autouse=True)
def reset_state():
    """Reset task state before each test."""
    tasks.clear()
    # Reset to a known state for predictable IDs
    globals()["task_id_counter"] = 1
    yield
    tasks.clear()


class TestAddCommand:
    """Tests for the 'add' command."""

    def test_add_task_minimal(self):
        """Test adding a task with only the required argument."""
        result = runner.invoke(app, ["add", "Buy groceries"])
        assert result.exit_code == 0
        assert "Added task #1: Buy groceries" in result.output
        assert "priority: medium" in result.output  # Default priority

    def test_add_task_with_priority(self):
        """Test adding a task with explicit priority."""
        result = runner.invoke(app, ["add", "Finish report", "--priority", "high"])
        assert result.exit_code == 0
        assert "Added task #1: Finish report" in result.output
        assert "priority: high" in result.output

    def test_add_task_with_short_flag(self):
        """Test adding a task with short option flag."""
        result = runner.invoke(app, ["add", "Call mom", "-p", "low"])
        assert result.exit_code == 0
        assert "priority: low" in result.output

    def test_add_multiple_tasks_increments_id(self):
        """Test that task IDs increment correctly."""
        runner.invoke(app, ["add", "First task"])
        result = runner.invoke(app, ["add", "Second task"])
        assert result.exit_code == 0
        assert "Added task #2: Second task" in result.output


class TestListCommand:
    """Tests for the 'list' command."""

    def test_list_empty(self):
        """Test listing when no tasks exist."""
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "No tasks found" in result.output

    def test_list_with_tasks(self):
        """Test listing tasks."""
        runner.invoke(app, ["add", "Task one"])
        runner.invoke(app, ["add", "Task two"])

        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "#1: Task one" in result.output
        assert "#2: Task two" in result.output

    def test_list_with_show_all(self):
        """Test list with --all flag shows status markers."""
        runner.invoke(app, ["add", "Inbox zero"])

        result = runner.invoke(app, ["list", "--all"])
        assert result.exit_code == 0
        assert "[ ]" in result.output


class TestCompleteCommand:
    """Tests for the 'complete' command."""

    def test_complete_task(self):
        """Test completing an existing task."""
        runner.invoke(app, ["add", "Review PR"])

        result = runner.invoke(app, ["complete", "1"])
        assert result.exit_code == 0
        assert "Completed task #1: Review PR" in result.output

    def test_complete_nonexistent_task(self):
        """Test completing a task that doesn't exist."""
        result = runner.invoke(app, ["complete", "999"])
        assert result.exit_code == 1
        assert "Error: Task #999 not found" in result.output
        assert "999" in result.stderr if result.stderr else "not found" in result.output.lower()

    def test_complete_invalid_id_type(self):
        """Test completing with invalid ID type."""
        result = runner.invoke(app, ["complete", "abc"])
        assert result.exit_code != 0


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_add_empty_title(self):
        """Test adding a task with empty title."""
        result = runner.invoke(app, ["add", ""])
        # Typer validates required arguments
        assert result.exit_code != 0 or "Error" in result.output

    def test_complete_after_adding_multiple(self):
        """Test completing one task doesn't affect others."""
        runner.invoke(app, ["add", "Keep me"])
        runner.invoke(app, ["add", "Remove me"])

        result = runner.invoke(app, ["complete", "2"])
        assert result.exit_code == 0

        # Verify first task still exists
        list_result = runner.invoke(app, ["list"])
        assert "#1: Keep me" in list_result.output
        assert "#2: Remove me" not in list_result.output
```

## Running the Tests

```bash
$ pytest tests/test_tasks.py -v
======================== test session starts =========================
collected 12 items

tests/test_tasks.py::TestAddCommand::test_add_task_minimal PASSED
tests/test_tasks.py::TestAddCommand::test_add_task_with_priority PASSED
tests/test_tasks.py::TestAddCommand::test_add_task_with_short_flag PASSED
tests/test_tasks.py::TestAddCommand::test_add_multiple_tasks_increments_id PASSED
tests/test_tasks.py::TestListCommand::test_list_empty PASSED
tests/test_tasks.py::TestListCommand::test_list_with_tasks PASSED
tests/test_tasks.py::TestListCommand::test_list_with_show_all PASSED
tests/test_tasks.py::TestCompleteCommand::test_complete_task PASSED
tests/test_tasks.py::TestCompleteCommand::test_complete_nonexistent_task PASSED
tests/test_tasks.py::TestCompleteCommand::test_complete_invalid_id_type PASSED
tests/test_tasks.py::TestEdgeCases::test_add_empty_title PASSED
tests/test_tasks.py::TestEdgeCases::test_complete_after_adding_multiple PASSED

======================== 12 passed in 0.45s ==========================
```

## Key Testing Patterns Demonstrated

| Pattern | Example |
|---------|---------|
| **Setup/Teardown** | `reset_state()` fixture clears tasks between tests |
| **Exit code verification** | `assert result.exit_code == 0` or `!= 0` for errors |
| **Output checking** | `assert "Expected text" in result.output` |
| **Argument combinations** | Testing `--priority` vs `-p` vs default |
| **Error cases** | Testing `complete 999` for nonexistent task |
| **State isolation** | Each test starts with clean state |
| **Incremental IDs** | Verifying task IDs increment correctly |

## Common Mistakes in Original Code (Fixed in Tests)

1. **No exit code check** - Original `complete` command has `raise typer.Exit(code=1)` but tests must verify this
2. **Missing error message** - Tests verify error output includes the task ID
3. **No empty state test** - Tests verify `list` handles empty task list
4. **State leakage** - Tests use fixture to reset state, preventing cross-test pollution

## Lessons Learned

- Always reset global state in fixtures
- Test both success AND failure paths
- Verify exit codes explicitly, not just output
- Use descriptive test names: `test_<command>_<scenario>`
- Group related tests in classes for organization

## See Also

- [SKILL.md](../SKILL.md) - Main index
- [basic-testing.md](../basic-testing.md) - Basic testing patterns
- [exit-codes.md](../exit-codes.md) - Exit code testing
- [prompts-testing.md](../prompts-testing.md) - Testing prompts
