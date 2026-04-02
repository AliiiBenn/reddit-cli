# Coverage Configuration

**Date:** 2026-03-31

## pytest-cov Setup

### Command Line

```bash
# Basic coverage
pytest --cov=src --cov-report=term-missing

# Multiple reports
pytest --cov=src --cov-report=term-missing --cov-report=html --cov-report=xml

# Fail under threshold
pytest --cov=src --cov-fail-under=80
```

### pyproject.toml Configuration

```toml
[tool.pytest.ini_options]
addopts = "--cov=src --cov-report=term-missing --cov-report=html"

[tool.coverage.run]
source = ["src"]
omit = ["tests/*", "*/migrations/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
```

## Coverage with Typer

### Testing All Branches

```python
def test_all_branches(runner, app):
    # Branch 1: with --verbose
    result = runner.invoke(app, ["process", "--verbose"])
    assert result.exit_code == 0

    # Branch 2: without --verbose
    result = runner.invoke(app, ["process"])
    assert result.exit_code == 0

    # Branch 3: with invalid argument
    result = runner.invoke(app, ["process", "--unknown"])
    assert result.exit_code != 0
```

### Testing Error Coverage

```python
def test_error_coverage(runner, app):
    # Test each error type
    result = runner.invoke(app, ["create", "--email", "not-an-email"])
    assert result.exit_code == 2

    result = runner.invoke(app, ["create", "--name", ""])
    assert result.exit_code == 2

    result = runner.invoke(app, ["delete", "--name", "nonexistent"])
    assert result.exit_code == 1
```

## Coverage by Command

```bash
# Coverage per command
pytest --cov=src --cov=src/cli --cov-report=term-missing
```

## Excluding Code from Coverage

```python
# pragma: no cover
if os.getenv("CI"):  # pragma: no cover
    typer.echo("CI mode")
```

## See Also

- [pytest-configuration.md](pytest-configuration.md) - pytest configuration
