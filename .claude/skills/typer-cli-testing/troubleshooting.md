# Troubleshooting Guide

**Date:** 2026-03-31

## Debug Pattern

When a test fails unexpectedly, use this debug pattern:

```python
def test_debug_pattern():
    result = runner.invoke(app, ["your", "command"])
    print(f"exit_code: {result.exit_code}")
    print(f"output: {result.output}")
    print(f"stdout: {result.stdout}")
    print(f"stderr: {result.stderr}")
    print(f"exception: {result.exception}")
    if result.exception:
        import traceback
        traceback.print_exception(type(result.exception), result.exception, result.exception.__traceback__)
    # Then write your assertions
    assert result.exit_code == 0
```

## Exit Code 2 = Unhandled Python Exception

If you get `exit_code == 2`, it means the command crashed with an unhandled Python exception:

```python
def test_crash_debug():
    result = runner.invoke(app, ["crash-command"])
    if result.exit_code == 2:
        # Command crashed with unhandled exception
        assert result.exception is not None
        print(f"Crash: {result.exception}")
        # Fix the exception handling in your Typer app
```

**Common causes:**
- Missing argument validation
- Unhandled exceptions in callbacks
- Type errors in argument parsing
- Missing imports or module errors

## result.stderr is Always Empty

Remember: by default `CliRunner(mix_stderr=True)`, so `result.stderr` is ALWAYS empty:

```python
runner = CliRunner()  # mix_stderr=True (default)
result = runner.invoke(app, ["bad"])
result.stderr  # EMPTY! stderr is in result.output

# To get separate stderr:
runner = CliRunner(mix_stderr=False)
result = runner.invoke(app, ["bad"])
result.stderr  # Now contains actual stderr
```

## Prompts: Wrong Order in `input=`

If prompts seem to accept wrong values, check that `input=` order matches Typer prompt order:

```python
# Read your Typer code to determine prompt order
# Then match exactly:

# If app.py has:
# @app.command()
# def create_user(email: str = typer.prompt("Email"), name: str = typer.prompt("Name")):

result = runner.invoke(app, ["create-user"], input="email@test.com\nName\n")
# CORRECT order: email FIRST, then name
```

## Test Hangs or Times Out

If tests hang, you may have missed a prompt:

```python
# Missing prompt input causes hang
result = runner.invoke(app, ["create-user"])  # Hangs - waiting for email input!

# Always provide input for all prompts
result = runner.invoke(app, ["create-user"], input="test@test.com\n")
```

## Files Not Found in Tests

Use `isolated_filesystem()` for file operations:

```python
def test_file_handling():
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["export", "--output", "data.csv"])
        assert Path("data.csv").exists()  # Clean assertion
```

## Progress Bar Tests Block/Hang

Progress bars can cause tests to hang because they wait for completion:

```python
# Problem: Test blocks forever waiting for progress bar
def test_slow_process():
    result = runner.invoke(app, ["process", "--items", "a,b,c"])
    # This will block!

# Solution: Mock time.sleep to speed up
def test_slow_process_fast():
    import unittest.mock as mock
    with mock.patch("time.sleep", return_value=None):
        result = runner.invoke(app, ["process", "--items", "a,b,c"])
    assert result.exit_code == 0

# Solution: Mock tqdm completely
def test_progress_mock():
    with mock.patch("tqdm.tqdm") as mock_tqdm:
        mock_tqdm.return_value.__enter__ = mock.Mock(return_value=mock_tqdm)
        mock_tqdm.return_value.__exit__ = mock.Mock(return_value=None)
        result = runner.invoke(app, ["batch-process"])
```

## Rich Output / ANSI Codes in Tests

When testing styled output, ANSI codes can complicate assertions:

```python
# Problem: ANSI codes in output
def test_styled_output():
    result = runner.invoke(app, ["greet", "--name", "Alice"])
    # result.output contains "\x1b[1mHello Alice\x1b[0m"

# Solution 1: Strip ANSI codes
def test_styled_output_plain():
    result = runner.invoke(app, ["greet", "--name", "Alice"])
    import re
    plain = re.sub(r'\x1b\[[0-9;]*m', '', result.output)
    assert "Hello Alice" in plain

# Solution 2: Check for ANSI codes presence
def test_has_styling():
    result = runner.invoke(app, ["greet", "--name", "Alice"])
    assert "\x1b[" in result.output  # Contains ANSI codes

# Solution 3: Use stripped_stderr parameter
def test_stripped():
    result = runner.invoke(app, ["styled"], stripped_stderr=True)
```

## exception_info for Advanced Debugging

```python
def test_debug_exception_info():
    result = runner.invoke(app, ["crash"])
    if result.exception:
        exc_type, exc_value, exc_tb = result.exception_info
        print(f"Exception type: {exc_type}")
        print(f"Exception value: {exc_value}")
        print(f"Traceback object: {exc_tb}")

# Full traceback printing
import traceback
def test_full_traceback():
    result = runner.invoke(app, ["buggy"])
    if result.exception:
        traceback.print_exception(
            type(result.exception),
            result.exception,
            result.exception.__traceback__
        )
```

## Mocking - Common Issues

### Mock Not Being Called

```python
# Problem: Mock not working
def test_mock_not_working(monkeypatch):
    mock_func = mock.Mock()
    # Make sure to patch the correct module path
    monkeypatch.setattr("myapp.module.func", mock_func)
    result = runner.invoke(app, ["call-func"])
    mock_func.assert_called_once()  # Will fail if wrong path

# Solution: Verify the correct import path
# from myapp.module import func  # Patch myapp.module.func
# import myapp.module; myapp.module.func  # Patch myapp.module.func
```

## Tests in Parallel - Mysterious Errors

```python
# Problem: Tests interfere with each other
def test_shared_state():
    # Both tests modify same global state
    result = runner.invoke(app, ["modify-global", "--value", "1"])
    assert result.exit_code == 0

# Solution 1: Use isolated_filesystem (default)
runner = CliRunner(isolated_filesystem=True)  # Default

# Solution 2: Session-scoped fixtures with locks
@pytest.fixture(scope="session")
def lock():
    return threading.Lock()

# Solution 3: pytest-xdist with proper isolation
# pytest -n auto  # Works with isolated_filesystem
```

## Environment Variables Not Applied

If environment variables don't seem to work:

```python
# Problem: env in invoke() not working
def test_env_override():
    result = runner.invoke(app, ["config"], env={"API_KEY": "secret"})
    assert "secret" not in result.output  # Fails!

# Solution 1: Pass env in constructor
runner = CliRunner(env={"API_KEY": "secret"})
result = runner.invoke(app, ["config"])

# Solution 2: Mock at the right time
def test_env_at_runtime(monkeypatch):
    monkeypatch.setenv("API_KEY", "runtime-secret")
    result = runner.invoke(app, ["config"])
    assert "runtime-secret" in result.output
```

## Context (`ctx.obj`) Not Shared

Each `runner.invoke()` creates a new context:

```python
# Problem: ctx.obj not shared between invocations
def test_context_not_shared():
    result1 = runner.invoke(app, ["init", "--registry", "alice,bob"])
    result2 = runner.invoke(app, ["list"])
    # result2 won't see "alice,bob" from result1!

# Solution: Use file-based persistence
def test_persistence():
    with runner.isolated_filesystem():
        # First command writes to file
        result1 = runner.invoke(app, ["init", "--registry", "alice,bob"])
        assert result1.exit_code == 0

        # Second command reads from file
        result2 = runner.invoke(app, ["list"])
        assert "alice" in result2.output
```

## catch_exceptions=False for Debugging

To see uncaught exceptions:

```python
# By default, exceptions are caught and exit_code=2
def test_default_behavior():
    result = runner.invoke(app, ["crash"])
    assert result.exit_code == 2
    assert result.exception is not None

# With catch_exceptions=False, exception is raised directly
def test_uncaught_exception():
    result = runner.invoke(app, ["crash"], catch_exceptions=False)
    # If app raises RuntimeError, it will be raised here!
```
