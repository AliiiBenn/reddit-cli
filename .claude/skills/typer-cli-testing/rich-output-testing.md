# Rich Output Testing

**Date:** 2026-03-31

## Overview

When testing styled output with Rich or typer.secho(), ANSI escape codes are included in the output.

## Testing Rich Markup

```python
import re

def test_rich_output():
    result = runner.invoke(app, ["greet", "--name", "Alice"])
    # Look for ANSI pattern or styled text
    assert "[bold]" in result.output or "Alice" in result.output
```

## Testing typer.secho()

```python
def test_secho():
    result = runner.invoke(app, ["warn"])
    # ANSI codes are in output
    assert "\x1b[" in result.output  # Contains ANSI codes
```

## Stripping ANSI Codes

```python
from typer.testing import CliRunner
import re

def test_plain_output():
    result = runner.invoke(app, ["styled"])
    # Strip ANSI codes
    plain = re.sub(r'\x1b\[[0-9;]*m', '', result.output)
    assert "Error" in plain

def test_no_ansi_in_plain_mode():
    result = runner.invoke(app, ["styled"])
    # Verify text is readable
    assert not re.search(r'\x1b\[[0-9;]*m', result.output) or "Error" in re.sub(r'\x1b\[[0-9;]*m', '', result.output)
```

## Using stripped_stderr Parameter

```python
def test_stripped():
    result = runner.invoke(app, ["styled"], stripped_stderr=True)
    plain_stderr = result.stderr
    # No ANSI codes in plain_stderr
```

## Checking for ANSI Codes Presence

```python
def test_has_styling():
    result = runner.invoke(app, ["greet", "--name", "Alice"])
    assert "\x1b[" in result.output  # Contains ANSI codes
```

## Unicode with Rich

```python
def test_unicode_rich():
    result = runner.invoke(app, ["greet", "--name", "日本語"])
    assert result.exit_code == 0
    assert "日本語" in result.output
```

## See Also

- [output-verification.md](output-verification.md) - Output verification
