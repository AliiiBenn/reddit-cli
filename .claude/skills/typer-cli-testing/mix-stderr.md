# mix_stderr Parameter

**Date:** 2026-03-31

## Overview

By default, `CliRunner()` uses `mix_stderr=True`, which means stderr is combined into `result.output` and `result.stderr` is **ALWAYS empty**.

## Default Behavior (mix_stderr=True)

```python
# Default: mix_stderr=True (stderr merged into output)
runner = CliRunner()  # or CliRunner(mix_stderr=True)
result = runner.invoke(app, ["invalid"])
result.stderr  # ALWAYS empty string!
result.output  # Contains stderr content
```

## Separate stderr Tracking (mix_stderr=False)

```python
# Separate stderr tracking
runner = CliRunner(mix_stderr=False)
result = runner.invoke(app, ["invalid"])
result.stderr  # Now contains actual stderr
result.stdout  # Contains actual stdout
```

## When to Use mix_stderr=False

- Testing error messages separately from stdout
- Verifying specific stderr content
- Debugging output routing issues

## Example

```python
def test_separate_stderr():
    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(app, ["invalid"])

    assert result.exit_code != 0
    assert "Error" in result.stderr
    assert result.stdout == ""
```

## Troubleshooting

### result.stderr is Always Empty

If you need `result.stderr` to contain actual content:

```python
runner = CliRunner(mix_stderr=False)
result = runner.invoke(app, ["bad"])
result.stderr  # Now contains actual stderr
```

## See Also

- [clirunner.md](clirunner.md) - CliRunner constructor
- [result-object.md](result-object.md) - Result object attributes
