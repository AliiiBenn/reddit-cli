# Parallel Tests

**Date:** 2026-03-31

## Overview

`isolated_filesystem()` is thread-safe and sufficient for most parallel testing scenarios.

## Basic Parallel Testing

```bash
# pytest-xdist - tests can run in parallel
pytest -n auto  # Use all CPUs
pytest -n 4     # Use 4 CPUs
```

## Shared Resource Handling

```python
# conftest.py with lock
import pytest
import threading

@pytest.fixture(scope="session")
def shared_resource():
    lock = threading.Lock()
    resource = {"counter": 0}
    yield resource

def test_increment(runner, app, shared_resource):
    with lock:  # Serialize access
        shared_resource["counter"] += 1
        result = runner.invoke(app, ["inc"])
    assert result.exit_code == 0
```

## isolated_filesystem() for Parallel Tests

```python
# isolated_filesystem() is thread-safe by default
def test_file_isolation(runner, app):
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["export", "--format", "csv"])
        assert result.exit_code == 0
        assert Path("export.csv").exists()
```

## Common Parallel Issues

### Tests Interfering with Each Other

```python
# Problem: Tests modify same global state
def test_shared_state():
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

### Warning: Do Not Mock Same Resource in Parallel

Do not mock the same resource in parallel without proper synchronization.

## See Also

- [isolated-filesystem.md](isolated-filesystem.md) - isolated_filesystem() usage
