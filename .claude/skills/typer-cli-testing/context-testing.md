# Context Testing

**Date:** 2026-03-31

## Testing Context-Dependent Behavior

When using `typer.Context` in your commands, test that context-dependent behavior works:

```python
def test_verbose_callback():
    """Test that global --verbose option affects command output"""
    result = runner.invoke(app, ["--verbose", "create", "--name", "Alice"])
    assert result.exit_code == 0
    assert "Verbose mode enabled" in result.output

def test_context_propagates():
    """Test that context is properly passed to subcommands"""
    result = runner.invoke(app, ["--debug", "process", "data.csv"])
    assert result.exit_code == 0
    assert "DEBUG" in result.output
```

## Testing ctx.obj

```python
# Test that ctx.obj is shared
def test_context_obj_shared():
    # First, a command that modifies ctx.obj
    result1 = runner.invoke(app, ["init", "--registry", "alice,bob"])
    assert result1.exit_code == 0

    # Then a command that reads ctx.obj
    result2 = runner.invoke(app, ["list"])
    assert "alice" in result2.output
    assert "bob" in result2.output
```

## Testing ctx.params

```python
def test_context_params():
    result = runner.invoke(app, ["create", "--verbose", "--name", "Alice"])
    assert result.exit_code == 0
    # ctx.params contains the parsed values
```

## Context Persistence Between Invocations

Each `runner.invoke()` creates a new context - `ctx.obj` is NOT shared between invocations:

```python
# Problem: ctx.obj not shared between invocations
def test_context_not_shared():
    result1 = runner.invoke(app, ["init", "--registry", "alice,bob"])
    result2 = runner.invoke(app, ["list"])
    # result2 won't see "alice,bob" from result1!

# Solution: Use file-based persistence
def test_persistence():
    with runner.isolated_filesystem():
        # First command writes to file
        result1 = runner.invoke(app, ["init", "--registry", "alice,bob"])
        assert result1.exit_code == 0

        # Second command reads from file
        result2 = runner.invoke(app, ["list"])
        assert "alice" in result2.output
```

## Nested Context

```python
def test_nested_context():
    result = runner.invoke(app, ["admin", "setup", "--level", "5"])
    assert result.exit_code == 0
```

## See Also

- [callbacks-testing.md](callbacks-testing.md) - Testing callbacks
- [subcommands-testing.md](subcommands-testing.md) - Testing subcommands
