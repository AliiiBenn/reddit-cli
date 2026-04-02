# Basic Testing Patterns

**Date:** 2026-03-31

## Minimal Test Setup

```python
from typer.testing import CliRunner
from app.main import app

runner = CliRunner()

def test_basic():
    result = runner.invoke(app, ["arg1"])
    assert result.exit_code == 0
```

## Standard Test Patterns

### Minimal Test

```python
def test_hello():
    result = runner.invoke(app, ["Camila"])
    assert result.exit_code == 0
```

### Comprehensive Test

```python
def test_hello_with_output():
    result = runner.invoke(app, ["Camila"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.output
```

### Testing Arguments

```python
# Required argument only
def test_create_minimal():
    result = runner.invoke(app, ["create", "project-x"])
    assert result.exit_code == 0

# With optional arguments
def test_create_with_options():
    result = runner.invoke(app, [
        "create",
        "project-x",
        "--template", "django",
        "--python", "3.11"
    ])
    assert result.exit_code == 0
    assert "django" in result.output
```

### Testing Options/Flags

```python
# Boolean flag off
def test_verbose_off():
    result = runner.invoke(app, ["process", "data.csv"])
    assert result.exit_code == 0
    assert "DEBUG" not in result.output

# Boolean flag on
def test_verbose_on():
    result = runner.invoke(app, ["process", "data.csv", "--verbose"])
    assert result.exit_code == 0
    assert "DEBUG" in result.output

# Option with value
def test_output_format():
    result = runner.invoke(app, ["export", "--format", "json"])
    assert result.exit_code == 0
    assert ".json" in result.output
```

### Multiple Options Together

```python
def test_complex_options():
    result = runner.invoke(app, [
        "export",
        "--format", "csv",
        "--compress",
        "--output", "export.csv"
    ])
    assert result.exit_code == 0
```

## Test File Structure

```
tests/
├── test_main.py        # Tests for main app commands
├── test_users.py       # Tests for user-related commands
└── test_output.py     # Tests for output formatting

# pytest auto-discovery patterns
test_*.py               # Standard naming
*_test.py               # Alternative naming
```

## Test Function Naming

```
test_<command>_<scenario>

test_create_user_success
test_create_user_missing_name
test_create_user_invalid_email
```

## Class-Based Organization

```python
class TestAddCommand:
    """Tests for the 'add' command."""

    def test_add_task_minimal(self):
        """Test adding a task with only the required argument."""
        result = runner.invoke(app, ["add", "Buy groceries"])
        assert result.exit_code == 0
        assert "Added task" in result.output

    def test_add_task_with_priority(self):
        """Test adding a task with explicit priority."""
        result = runner.invoke(app, ["add", "Finish report", "--priority", "high"])
        assert result.exit_code == 0
        assert "priority: high" in result.output


class TestListCommand:
    """Tests for the 'list' command."""

    def test_list_empty(self):
        """Test listing when no tasks exist."""
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "No tasks found" in result.output
```

## See Also

- [exit-codes.md](exit-codes.md) - Exit code testing
- [output-verification.md](output-verification.md) - Output verification
- [prompts-testing.md](prompts-testing.md) - Testing prompts
- [subcommands-testing.md](subcommands-testing.md) - Testing subcommands
