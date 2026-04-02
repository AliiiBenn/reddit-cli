# pytest.mark.parametrize

**Date:** 2026-03-31

## Basic Parametrization

```python
import pytest
from typer.testing import CliRunner

runner = CliRunner()

@pytest.mark.parametrize("name,expected_exit", [
    ("Alice", 0),
    ("", 1),
    ("admin", 1),
])
def test_create(runner, app, name, expected_exit):
    result = runner.invoke(app, ["create", name])
    assert result.exit_code == expected_exit
```

## Multiple Parameters

```python
@pytest.mark.parametrize("flag,verbose", [
    ("--verbose", True),
    ("--debug", True),
    ("", False),
])
def test_flags(runner, app, flag, verbose):
    args = ["run"] + ([flag] if flag else [])
    result = runner.invoke(app, args)
    assert result.exit_code == 0
```

## Parametrize with IDs

```python
@pytest.mark.parametrize("input_value,expected", [
    pytest.param("yes", True, id="confirm-yes"),
    pytest.param("no", False, id="confirm-no"),
    pytest.param("", False, id="confirm-default"),
],)
def test_confirm(runner, app, input_value, expected):
    input_str = input_value + "\n" if input_value else "\n"
    result = runner.invoke(app, ["confirm"], input=input_str)
    assert result.exit_code == 0
```

## Complex Parametrization

```python
@pytest.mark.parametrize("name,email,expected_exit", [
    pytest.param("Alice", "alice@example.com", 0, id="valid"),
    pytest.param("", "alice@example.com", 2, id="missing-name"),
    pytest.param("Bob", "invalid-email", 1, id="invalid-email"),
])
def test_user_creation(runner, app, name, email, expected_exit):
    result = runner.invoke(app, ["create", "--name", name, "--email", email])
    assert result.exit_code == expected_exit
```

## See Also

- [pytest-configuration.md](pytest-configuration.md) - pytest configuration
