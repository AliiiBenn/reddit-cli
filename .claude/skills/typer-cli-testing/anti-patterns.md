# Anti-Patterns

**Date:** 2026-03-31

## Testing Logic Instead of CLI

```python
# Bad - tests the function directly, bypasses CLI
def test_create_user():
    from app.commands import create_user
    result = create_user("Alice")
    assert result == "User created"

# Good - tests the CLI invocation
def test_create_user():
    result = runner.invoke(app, ["create", "--name", "Alice"])
    assert result.exit_code == 0
    assert "User created" in result.output
```

## Missing Exit Code Check

```python
# Bad - doesn't verify exit code
def test_command():
    result = runner.invoke(app, ["arg"])
    assert "expected" in result.output
    # Exit code not checked!

# Good - always check exit code
def test_command():
    result = runner.invoke(app, ["arg"])
    assert result.exit_code == 0
    assert "expected" in result.output
```

## Only Testing Happy Path

```python
# Bad - only tests success
def test_all_commands():
    assert runner.invoke(app, ["start"]).exit_code == 0
    assert runner.invoke(app, ["stop"]).exit_code == 0

# Good - also tests failure cases
def test_start_already_running():
    runner.invoke(app, ["start"])  # First time - OK
    result = runner.invoke(app, ["start"])  # Second time - should fail
    assert result.exit_code != 0
    assert "already running" in result.output.lower()
```

## Not Testing Interactive Prompts

```python
# Bad - ignores prompt testing
def test_user_creation():
    # Missing input for prompt!
    result = runner.invoke(app, ["create-user"])
    # Result is unpredictable

# Good - provides all inputs
def test_user_creation():
    result = runner.invoke(
        app,
        ["create-user"],
        input="john@example.com\nJohn Doe\ny\n"
    )
    assert result.exit_code == 0
    assert "User created" in result.output
```

## Silent Failure Assumption

```python
# Bad - assumes success without verification
def test_command():
    result = runner.invoke(app, ["arg"])
    assert "output" in result.output

# Good - explicit exit code with message
def test_command():
    result = runner.invoke(app, ["arg"])
    assert result.exit_code == 0, f"Command failed: {result.output}"
    assert "output" in result.output
```

## Testing typer.run() Functions Directly

```python
# Bad - for typer.run() apps, testing the function directly
def test_main():
    from app.main import main
    # This bypasses the CLI interface

# Good - use CliRunner even for simple apps
def test_main():
    app = typer.Typer()
    app.command()(main)  # Wrap the function
    result = runner.invoke(app, ["--name", "Alice"])
    assert result.exit_code == 0
```

## See Also

- [common-mistakes.md](common-mistakes.md) - Common mistakes checklist
