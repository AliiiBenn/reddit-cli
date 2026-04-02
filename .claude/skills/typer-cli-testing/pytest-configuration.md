# Pytest Configuration

**Date:** 2026-03-31

## conftest.py - Shared Fixtures

```python
# conftest.py
import pytest
from typer.testing import CliRunner

@pytest.fixture
def runner():
    """Runner partagÃ© entre tests."""
    return CliRunner(mix_stderr=False)

@pytest.fixture
def app():
    """App fixture."""
    from myapp import app
    return app

@pytest.fixture
def runner_with_env():
    """Runner avec variables d'environnement."""
    return CliRunner(env={"TEST_MODE": "1"})

# Fixture avec isolated_filesystem
@pytest.fixture
def isolated_runner():
    runner = CliRunner()
    return runner

# Fixture pour app avec callback
@pytest.fixture
def app_with_callback():
    import typer
    app = typer.Typer()

    @app.callback(invoke_without_command=True)
    def callback(ctx: typer.Context, verbose: bool = False):
        if verbose:
            typer.echo("Verbose mode")

    @app.command()
    def create(name: str):
        typer.echo(f"Creating {name}")

    return app
```

## Fixture Reset Pattern

```python
@pytest.fixture(autouse=True)
def reset_state():
    """Reset task state before each test."""
    tasks.clear()
    # Reset to a known state for predictable IDs
    globals()["task_id_counter"] = 1
    yield
    tasks.clear()
```

## pytest.ini Configuration

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --strict-markers --tb=short
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
```

## pyproject.toml Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--strict-markers",
    "--tb=short",
]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]

[tool.pytest.ini_options]
# Coverage options
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

## See Also

- [parametrization.md](parametrization.md) - pytest.mark.parametrize
