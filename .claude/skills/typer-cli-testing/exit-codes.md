# Exit Code Testing

**Date:** 2026-03-31

## Exit Code Reference

| Code | Meaning | Example |
|------|---------|---------|
| 0 | Success | Normal completion |
| 1 | General error | `typer.Abort()`, handled errors |
| 2 | Usage error | `BadParameter`, missing argument, unhandled exception |
| 125 | Unknown option | Click: unrecognized flag |
| 126 | Command not found | Click: subcommand not found |
| 127 | External command not found | `subprocess` failure |
| 128+N | Killed by signal N | `kill -9` = 137 |
| 130 | Interrupted | Ctrl+C (KeyboardInterrupt) |

## Testing Patterns

### Success Exit Code (0)

```python
def test_success():
    result = runner.invoke(app, ["create", "--name", "Alice"])
    assert result.exit_code == 0
    assert "User created" in result.output
```

### Failure Exit Code (non-zero)

```python
def test_failure():
    result = runner.invoke(app, ["delete", "--name", "nonexistent"])
    assert result.exit_code != 0
    assert "not found" in result.output.lower()
```

### Specific Exit Codes

```python
# Validation error (exit code 1)
def test_validation_error():
    result = runner.invoke(app, ["create", "--email", "invalid"])
    assert result.exit_code == 1
    assert "invalid email" in result.output.lower()

# BadParameter - exit code 2
def test_bad_parameter():
    result = runner.invoke(app, ["create", "--email", "invalid"])
    assert result.exit_code == 2
    assert result.exception is not None

# Missing required argument - exit code 2
def test_missing_argument():
    result = runner.invoke(app, ["create"])  # without name
    assert result.exit_code == 2

# Unknown option - exit code 125
def test_unknown_option():
    result = runner.invoke(app, ["--unknown-flag"])
    assert result.exit_code == 125

# TyperAbort - exit code 1
def test_abort():
    result = runner.invoke(app, ["abort"])
    assert result.exit_code == 1
```

### Exit Code Meanings Test

```python
def test_exit_code_meanings():
    # Success
    result = runner.invoke(app, ["success"])
    assert result.exit_code == 0

    # BadParameter - exit code 2
    result = runner.invoke(app, ["create", "--email", "invalid"])
    assert result.exit_code == 2
    assert isinstance(result.exception, typer.BadParameter)

    # Missing required arg - exit code 2
    result = runner.invoke(app, ["create"])  # without name
    assert result.exit_code == 2

    # TyperAbort - exit code 1
    result = runner.invoke(app, ["abort"])
    assert result.exit_code == 1

    # Unknown option - exit code 125 (Click)
    result = runner.invoke(app, ["--unknown-flag"])
    assert result.exit_code == 125
```

## Helper Function

```python
def assert_exit_code(result, expected_code, message=""):
    assert result.exit_code == expected_code, \
        f"{message}: expected {expected_code}, got {result.exit_code}. Output: {result.output}"
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
```

**Common causes:**
- Missing argument validation
- Unhandled exceptions in callbacks
- Type errors in argument parsing
- Missing imports or module errors

## See Also

- [result-object.md](result-object.md) - Result object attributes
- [exception-testing.md](exception-testing.md) - Testing exceptions
- [anti-patterns.md](anti-patterns.md) - Anti-patterns to avoid
