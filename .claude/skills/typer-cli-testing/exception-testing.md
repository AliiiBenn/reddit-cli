# Exception Testing

**Date:** 2026-03-31

## Overview

Always check `result.exception` when debugging test failures. **Exit code 2 typically means an unhandled Python exception.**

## Testing Patterns

### Check Exception for Better Debugging

```python
def test_with_exception_check():
    """Check exception when command fails unexpectedly"""
    result = runner.invoke(app, ["crash", "--arg", "value"])

    # Check exception first for better debugging
    if result.exception:
        print(f"Exception raised: {result.exception}")
    assert result.exception is None, f"Command raised: {result.exception}"
    assert result.exit_code == 1
```

### Expected Errors (No Exception)

```python
def test_handled_error():
    """Expected errors (exit_code != 0) usually have no exception"""
    result = runner.invoke(app, ["validate", "--email", "invalid"])
    assert result.exception is None  # Error was handled gracefully
    assert result.exit_code == 1
    assert "invalid email" in result.output
```

### Python Crash (Unhandled Exception)

```python
def test_python_crash():
    """Exit code 2 = unhandled Python exception"""
    result = runner.invoke(app, ["crash"])
    assert result.exit_code == 2
    assert result.exception is not None
    assert isinstance(result.exception, TypeError)
```

## Advanced Debugging with exception_info

```python
def test_exception_info():
    result = runner.invoke(app, ["buggy"])

    if result.exception:
        exc_type, exc_value, exc_tb = result.exception_info
        print(f"Type: {exc_type}")
        print(f"Value: {exc_value}")
        print(f"Traceback: {exc_tb}")

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

## Verifying Exception Type

```python
def test_exception_type():
    result = runner.invoke(app, ["crash"])

    if result.exception:
        exc_type, _, _ = result.exception_info
        assert exc_type == ValueError

def test_no_exception():
    result = runner.invoke(app, ["success"])
    assert result.exception is None
    assert result.exception_info is None
```

## Using catch_exceptions=False

```python
def test_uncaught_exception():
    result = runner.invoke(app, ["crash"], catch_exceptions=False)
    # If app raises RuntimeError, it will be raised here!
    # Useful for testing that exceptions are properly handled
```

## See Also

- [result-object.md](result-object.md) - Result object attributes
- [exit-codes.md](exit-codes.md) - Exit code meanings
