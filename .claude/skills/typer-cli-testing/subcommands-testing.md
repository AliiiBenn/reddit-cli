# Subcommands Testing

**Date:** 2026-03-31

## Testing Subcommands

Test each subcommand independently and in combination:

```python
# Test root-level command
def test_base_command():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0

# Test users subcommand group
def test_users_create():
    result = runner.invoke(app, ["users", "create", "--name", "Alice"])
    assert result.exit_code == 0
    assert "Creating user: Alice" in result.output

def test_users_list():
    result = runner.invoke(app, ["users", "list"])
    assert result.exit_code == 0
    assert "Alice" in result.output

def test_users_delete():
    result = runner.invoke(app, ["users", "delete", "--name", "Alice"])
    assert result.exit_code == 0
    assert "Deleted user: Alice" in result.output
```

## Nested Subcommands

```python
# Test nested subcommands
def test_admin_users_list():
    result = runner.invoke(app, ["admin", "users", "list", "--filter", "active"])
    assert result.exit_code == 0
    assert "Listing users" in result.output

# Test deeper nesting
def test_nested_subcommand():
    result = runner.invoke(app, ["admin", "users", "list"])
    assert result.exit_code == 0
```

## Subcommand with Prompts

```python
def test_users_create_with_prompts():
    result = runner.invoke(app, ["users", "create"], input="alice@example.com\n")
    assert result.exit_code == 0
    assert "User created" in result.output
```

## Callback with Subcommands

```python
# Test parent callback with child command
def test_parent_callback_with_child_command():
    result = runner.invoke(app, ["parent", "child", "--arg", "value"])
    assert "Parent init" in result.output or "Initializing" in result.output

# Test subapp callback
def test_subapp_callback():
    # The subapp callback executes with the command
    result = runner.invoke(app, ["users", "create", "--name", "Alice"])
    # Verify the callback was executed
    assert "Users management" in result.output or "Verbose" in result.output

# Test subcommand without callback
def test_subcommand_no_callback():
    result = runner.invoke(app, ["simple", "subcommand"])
    assert result.exit_code == 0
```

## See Also

- [callbacks-testing.md](callbacks-testing.md) - Testing callbacks
- [context-testing.md](context-testing.md) - Testing Context
