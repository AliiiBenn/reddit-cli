# Prompts Testing

**Date:** 2026-03-31

## Basic Prompt Testing

```python
def test_email_prompt():
    result = runner.invoke(
        app,
        ["create-user"],
        input="john@example.com\n"
    )
    assert result.exit_code == 0
    assert "john@example.com" in result.output
```

## Multiple Prompts

```python
def test_user_creation_with_prompts():
    result = runner.invoke(
        app,
        ["create-user"],
        input="john@example.com\nJohn Doe\ny\n"
    )
    assert result.exit_code == 0
    assert "User created" in result.output
```

## Default Value (Just Press Enter)

```python
def test_email_with_default():
    result = runner.invoke(
        app,
        ["create-user"],
        input="\n"  # Accept default for email prompt
    )
    assert result.exit_code == 0
```

## typer.confirm() Testing

```python
def test_confirm_yes():
    result = runner.invoke(app, ["delete", "--name", "Alice"], input="y\n")
    assert result.exit_code == 0
    assert "Deleting Alice" in result.output

def test_confirm_no():
    result = runner.invoke(app, ["delete", "--name", "Alice"], input="n\n")
    assert result.exit_code == 0
    assert "Cancelled" in result.output
```

## Prompt Validation and Retry

```python
# Test with retry - user enters invalid value then valid
def test_prompt_retry():
    # input=: first entry (invalid), second (valid)
    result = runner.invoke(app, ["create"], input="invalid\nvalid@example.com\n")
    assert result.exit_code == 0
    assert "valid@example.com" in result.output

# Test confirmation with retry
def test_prompt_validation():
    # User refuses 3 times then accepts
    result = runner.invoke(app, ["confirm"], input="no\nno\nyes\n")
    assert result.exit_code == 0
    assert "Confirmed" in result.output
```

## Prompt Order Matters

If prompts seem to accept wrong values, check that `input=` order matches Typer prompt order:

```python
# Read your Typer code to determine prompt order
# Then match exactly:

# If app.py has:
# @app.command()
# def create_user(email: str = typer.prompt("Email"), name: str = typer.prompt("Name")):

result = runner.invoke(app, ["create-user"], input="email@test.com\nName\n")
# CORRECT order: email FIRST, then name
```

## Debugging Prompts

If tests hang or timeout, you may have missed a prompt:

```python
# Problem: Missing prompt input causes hang
result = runner.invoke(app, ["create-user"])  # Hangs - waiting for email input!

# Always provide input for all prompts
result = runner.invoke(app, ["create-user"], input="test@test.com\n")
```

## See Also

- [invocation.md](invocation.md) - runner.invoke() parameters
- [basic-testing.md](basic-testing.md) - Basic testing patterns
