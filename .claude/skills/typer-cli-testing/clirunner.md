# CliRunner Constructor

**Date:** 2026-03-31

## CliRunner Parameters

```python
from typer.testing import CliRunner

runner = CliRunner(
    mix_stderr=True,        # Combine stderr into output (default)
    cache_size=64,          # Cache for completions
    interpolations={},       # String interpolations
    env=None,               # Environment variables
    catch_exceptions=True,  # Catch exceptions (default)
    isolated_filesystem=True # Filesystem isolation (default)
)
```

## Parameter Details

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `mix_stderr` | `bool` | `True` | Combine stderr into `result.output`; if `False`, `result.stderr` contains actual stderr |
| `cache_size` | `int` | `64` | Cache size for completions (rarely used) |
| `interpolations` | `dict` | `{}` | String interpolations (rarely used) |
| `env` | `dict` | `None` | Environment variables passed to tests |
| `catch_exceptions` | `bool` | `True` | Catch exceptions and return exit_code=2 |
| `isolated_filesystem` | `bool` | `True` | Each test gets an isolated temp directory |

## Common Configurations

```python
# Default configuration
runner = CliRunner()

# Separate stderr tracking
runner = CliRunner(mix_stderr=False)
result = runner.invoke(app, ["invalid"])
result.stderr  # Now contains actual stderr
result.stdout  # Contains actual stdout

# With environment variables
runner = CliRunner(env={"TEST_MODE": "1"})

# Without filesystem isolation (share filesystem between tests)
runner = CliRunner(isolated_filesystem=False)

# Don't catch exceptions (for debugging)
runner = CliRunner(catch_exceptions=False)
```

## Usage Pattern

```python
from typer.testing import CliRunner
from app.main import app

# Create runner once per test session (module-level)
runner = CliRunner()

def test_basic_command():
    result = runner.invoke(app, ["arg1", "--option", "value"])
    assert result.exit_code == 0
```

## See Also

- [invocation.md](invocation.md) - runner.invoke() parameters
- [result-object.md](result-object.md) - Result object attributes
- [mix-stderr.md](mix-stderr.md) - mix_stderr parameter behavior
