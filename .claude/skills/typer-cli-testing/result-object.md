# Result Object

**Date:** 2026-03-31

## Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `exit_code` | `int` | 0 for success, non-zero for errors |
| `output` | `str` | Combined stdout and stderr (see `mix_stderr`) |
| `stdout` | `str` | Standard output only |
| `stderr` | `str` | Standard error only (empty if `mix_stderr=True`) |
| `exception` | `Exception` | Exception instance if command raised, `None` otherwise |
| `exception_info` | `tuple` | (type, value, traceback) for advanced debugging |

## exit_code Values

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error (`typer.Abort()`, handled errors) |
| 2 | Usage error (BadParameter, missing arguments, unhandled exception) |
| 125 | Unknown option (Click) |
| 126 | Command not found (Click) |
| 127 | External command not found |
| 128+N | Killed by signal N |
| 130 | Interrupted by Ctrl+C |

## Usage Examples

### Basic Attribute Access

```python
def test_result_attributes():
    result = runner.invoke(app, ["create", "--name", "Alice"])
    assert result.exit_code == 0
    assert "Hello Alice" in result.output
    assert result.exception is None
```

### Separate stdout/stderr (with mix_stderr=False)

```python
def test_separate_streams():
    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(app, ["invalid"])

    assert result.stdout == ""  # or actual stdout content
    assert "Error" in result.stderr
```

### Checking Exception

```python
def test_exception_check():
    result = runner.invoke(app, ["crash"])

    if result.exception:
        print(f"Exception: {result.exception}")
        print(f"Type: {type(result.exception)}")

    assert result.exception is None, f"Command raised: {result.exception}"
    assert result.exit_code == 1
```

### Using exception_info for Advanced Debugging

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
        traceback.print_exception(
            type(result.exception),
            result.exception,
            result.exception.__traceback__
        )
```

### Verifying Exception Type

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

## Debug Pattern

When a test fails unexpectedly:

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
        traceback.print_exception(
            type(result.exception),
            result.exception,
            result.exception.__traceback__
        )

    assert result.exit_code == 0
```

## See Also

- [exit-codes.md](exit-codes.md) - Exit code meanings
- [exception-testing.md](exception-testing.md) - Testing exceptions
- [mix-stderr.md](mix-stderr.md) - Understanding output vs stderr
