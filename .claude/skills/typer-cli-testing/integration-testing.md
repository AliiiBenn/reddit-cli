# Integration Testing

**Date:** 2026-03-31

## Overview

Integration tests verify the CLI works after installation using subprocess.

## Testing Installed CLI

```python
# test_installed.py - Test after installation
import subprocess
import sys
import os

def test_installed_cli():
    """Test the installed executable."""
    result = subprocess.run(
        [sys.executable, "-m", "myapp", "--help"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Usage:" in result.stdout

def test_entry_point():
    result = subprocess.run(
        ["myapp", "--version"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "1.0.0" in result.stdout
```

## Environment Variables

```python
def test_env_in_installed():
    env = {"MYAPP_VERBOSE": "1"}
    result = subprocess.run(
        ["myapp", "status"],
        capture_output=True,
        text=True,
        env={**os.environ, **env}
    )
    assert "Verbose mode" in result.stderr
```

## Stdin Input

```python
def test_stdin_input():
    result = subprocess.run(
        ["myapp", "create"],
        input="test@example.com\n",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
```

## Exit Codes

```python
def test_exit_codes():
    # Success
    result = subprocess.run(["myapp", "success"], capture_output=True)
    assert result.returncode == 0

    # Failure
    result = subprocess.run(["myapp", "fail"], capture_output=True)
    assert result.returncode != 0
```

## See Also

- [pytest-configuration.md](pytest-configuration.md) - pytest configuration
