# runner.invoke() Parameters

**Date:** 2026-03-31

## Full Signature

```python
runner.invoke(
    app,
    args=None,              # CLI arguments (list or str)
    input=None,             # Input for prompts (str)
    env=None,              # Environment variables override
    catch_exceptions=True, # False = exception propagates
    mixing=True,           # For mix_stderr (deprecated)
    input_stream=None,      # InputStream for complex prompts
    stripped_stderr=False   # Strip ANSI codes from stderr
)
```

## Parameter Details

| Parameter | Type | Description |
|-----------|------|-------------|
| `app` | `Typer` | The Typer application instance |
| `args` | `list` or `str` | Command-line arguments |
| `input` | `str` | Input for interactive prompts (newline-separated) |
| `env` | `dict` | Environment variables override |
| `catch_exceptions` | `bool` | If `False`, exceptions propagate (exit_code != 2) |
| `input_stream` | `IO` | Alternative input stream for complex prompts |

## Usage Examples

### Basic Invocation

```python
def test_basic():
    result = runner.invoke(app, ["create", "--name", "Alice"])
    assert result.exit_code == 0
```

### String Arguments (instead of list)

```python
def test_string_args():
    result = runner.invoke(app, "create --name Alice --verbose")
    assert result.exit_code == 0
```

### With Input for Prompts

```python
def test_with_prompt():
    result = runner.invoke(
        app,
        ["create-user"],
        input="john@example.com\n"
    )
    assert result.exit_code == 0
```

### Multiple Prompts

```python
def test_multiple_prompts():
    result = runner.invoke(
        app,
        ["create-user"],
        input="john@example.com\nJohn Doe\ny\n"
    )
    assert result.exit_code == 0
    assert "User created" in result.output
```

### Environment Variables Override

```python
def test_env_override():
    result = runner.invoke(app, ["config"], env={"API_KEY": "test-key"})
    assert "test-key" in result.output
```

### Exception Propagation (catch_exceptions=False)

```python
def test_unhandled_exception():
    result = runner.invoke(app, ["crash"], catch_exceptions=False)
    assert isinstance(result.exception, RuntimeError)
```

### Complex Input Stream

```python
import io

def test_with_stream():
    stream = io.StringIO("input1\ninput2\n")
    result = runner.invoke(app, ["prompt_cmd"], input_stream=stream)
```

### Stripped ANSI Codes

```python
def test_stripped_ansi():
    result = runner.invoke(app, ["styled"], stripped_stderr=True)
    plain_stderr = result.stderr
    # No ANSI codes in plain_stderr
```

## See Also

- [clirunner.md](clirunner.md) - CliRunner constructor
- [result-object.md](result-object.md) - Result object attributes
- [prompts-testing.md](prompts-testing.md) - Testing prompts
