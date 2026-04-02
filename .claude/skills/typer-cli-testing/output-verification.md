# Output Verification

**Date:** 2026-03-31

## Checking stdout

```python
def test_output():
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0
    assert "Service is running" in result.stdout
```

## Checking stderr Separately

Requires `mix_stderr=False`:

```python
def test_error_message():
    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(app, ["invalid-command"])
    assert result.exit_code != 0
    assert "Error" in result.stderr
```

## Checking Combined Output

```python
def test_combined_output():
    result = runner.invoke(app, ["process", "--verbose"])
    assert result.exit_code == 0
    # result.output includes both stdout and stderr (if mix_stderr=True)
    assert "Starting process" in result.output
    assert "Completed" in result.output
```

## Unicode and Special Characters

```python
def test_unicode_input():
    """Test handling of Unicode characters"""
    result = runner.invoke(app, ["create-user"], input="日本語\n")
    assert result.exit_code == 0

def test_emoji_in_names():
    """Test emoji characters in user names"""
    result = runner.invoke(app, ["create", "--name", "Alice 👋"])
    assert result.exit_code == 0
    assert "Alice 👋" in result.output

def test_special_characters():
    """Test special characters in arguments"""
    result = runner.invoke(app, ["search", "--query", "hello & world | test"])
    assert result.exit_code == 0
```

## See Also

- [rich-output-testing.md](rich-output-testing.md) - Rich markup and ANSI codes
- [mix-stderr.md](mix-stderr.md) - mix_stderr parameter behavior
