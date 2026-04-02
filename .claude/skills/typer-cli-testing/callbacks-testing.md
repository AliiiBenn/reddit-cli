# Callbacks Testing

**Date:** 2026-03-31

## Testing invoke_without_command

```python
# Test callback alone - the callback should execute when no subcommand is specified
def test_callback_alone():
    result = runner.invoke(app, [])
    assert "Initializing..." in result.output

# Test callback with subcommand - callback also executes if invoke_without_command=True
def test_callback_with_subcommand():
    result = runner.invoke(app, ["users", "create", "--name", "Alice"])
    assert "Initializing..." in result.output
    assert "Creating Alice" in result.output

# Test callback without subcommand and without invoke_without_command=True
def test_callback_no_subcommand_no_flag():
    # If invoke_without_command=False (default), callback doesn't execute alone
    result = runner.invoke(app, [])
    # "Initializing..." may NOT be in output
```

## App with invoke_without_command=True

```python
def test_callback_with_invoke_without_command():
    app = typer.Typer()

    @app.callback(invoke_without_command=True)
    def callback(ctx: typer.Context):
        typer.echo("Global init")

    @app.command()
    def create(name: str):
        typer.echo(f"Creating {name}")

    runner = CliRunner()
    result = runner.invoke(app, [])
    assert "Global init" in result.output
```

## Callback Chain

```python
def test_callback_chain():
    """Test chained callback execution"""
    result = runner.invoke(app, ["--verbose", "--debug", "status"])
    assert "Verbose mode enabled" in result.output
    assert "Debug mode enabled" in result.output
```

## Callback Patterns

```python
# Callback runs before subcommand executes
def test_callback_invoked_with_command():
    result = runner.invoke(app, ["--verbose", "create", "--name", "Alice"])
    assert "Initializing..." in result.output
    assert "Creating user: Alice" in result.output

# Callback runs when no subcommand is specified
def test_callback_invoked_alone():
    result = runner.invoke(app, ["--verbose"])
    assert "Verbose mode enabled" in result.output
    assert "No command specified" in result.output

# Callback chain with multiple options
def test_callback_chain():
    result = runner.invoke(app, ["--verbose", "--debug", "status"])
    assert "Verbose mode enabled" in result.output
    assert "Debug mode enabled" in result.output
```

## See Also

- [subcommands-testing.md](subcommands-testing.md) - Testing subcommands
- [context-testing.md](context-testing.md) - Testing Context
