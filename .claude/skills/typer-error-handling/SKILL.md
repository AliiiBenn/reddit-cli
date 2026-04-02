---
name: typer-error-handling
description: Typer error handling best practices. Use when handling exceptions in CLI apps, creating user-friendly error messages, managing exit codes, or debugging Typer errors.
disable-model-invocation: true
allowed-tools: Read,Grep,Glob,Bash
---

# Typer Error Handling Skill

Handle exceptions, exit codes, and user-friendly errors in Typer CLI applications.

## Quick Usage

```bash
# Invoke this skill when working with:
# - Exception handling in Typer apps
# - Exit code management
# - User-friendly error messages
# - Debugging Typer errors

# Check exit codes in tests
grep -rn "exit_code" tests/ --include="*.py"

# Find exception handling patterns
grep -rn "typer.Exit\|typer.Abort\|raise" app/ --include="*.py"

# Find rich formatting in errors
grep -rn "typer.style\|rich" app/ --include="*.py"
```

## Overview

Typer CLI applications must handle errors gracefully to provide good user experience and proper Unix integration. Error handling in Typer involves three complementary mechanisms:

1. **Exit Codes** - Unix convention for program success/failure status
2. **Exception Handling** - Python's try/except for catching and responding to errors
3. **Rich Formatting** - User-friendly, colored error messages using the Rich library

Proper error handling ensures your CLI integrates correctly with scripts, CI/CD pipelines, and other command-line tools.

## Topics

### Exit Codes

- [exit-codes.md](exit-codes.md) - Complete exit code reference (0, 1, 2, 125, 126, 127, 128+N, 130)
- [typer-exit.md](typer-exit.md) - `typer.Exit()` - err=True, message, code
- [typer-abort.md](typer-abort.md) - `typer.Abort()` - usage, differences with Exit
- [typer-interrupt.md](typer-interrupt.md) - TyperInterrupt - Ctrl+C handling, exit 130
- [system-exit.md](system-exit.md) - SystemExit vs typer.Exit

### Exceptions

- [exception-hierarchy.md](exception-hierarchy.md) - TyperError, BadParameter, MissingOption, etc.
- [click-compatibility.md](click-compatibility.md) - Click exceptions compatibility
- [custom-exceptions.md](custom-exceptions.md) - Custom exception classes (TyperError inheritance)
- [badparameter.md](badparameter.md) - BadParameter with param_hint
- [validation-patterns.md](validation-patterns.md) - converter vs callback vs validator
- [exception-chaining.md](exception-chaining.md) - `raise ... from e`

### Rich Error Formatting

- [rich-errors.md](rich-errors.md) - Rich error formatting (panels, tables, Console)
- [secho-style.md](secho-style.md) - typer.secho(), typer.style()

### Configuration & Debugging

- [pretty-exceptions.md](pretty-exceptions.md) - pretty_exceptions_enable/show_locals/short
- [environment-variables.md](environment-variables.md) - TYPER_STANDARD_TRACEBACK, TYPER_USE_RICH, etc.

### Best Practices

- [logging.md](logging.md) - Logging integration with stderr
- [context-managers.md](context-managers.md) - Resource cleanup with try/finally

### Reference

- [reference-card.md](reference-card.md) - Reference card - exit codes, exceptions
- [examples/sample.md](examples/sample.md) - Complete example with error handling

## Quick Usage Patterns

### Exit with Error to stderr

```python
raise typer.Exit("Error message", code=1, err=True)
```

### Abort (shows "Aborted!")

```python
raise typer.Abort()  # No custom message allowed!
```

### BadParameter for Validation

```python
raise BadParameter("Invalid value", param_hint="param_name")
```

### Custom Exception

```python
class AppError(TyperError):
    def __init__(self, message: str, code: int = 1):
        super().__init__(message)
        self.code = code
```

### Exception Chaining

```python
raise typer.Exit(f"Failed: {e}") from e
```

## Best Practices Checklist

### Exit Codes
- [ ] Use 0 for success, never return 0 for error conditions
- [ ] Use 1 for general errors
- [ ] Use 2 for usage errors (invalid arguments)
- [ ] Use 130 for user interruption (Ctrl+C)
- [ ] Be consistent - same error should always return same code

### Error Messages
- [ ] Be specific - include actual values that caused the error
- [ ] Be actionable - tell users what to do to fix it
- [ ] Use Rich formatting - color and structure aid comprehension
- [ ] Use `err=True` - send errors to stderr, not stdout

### Exception Handling
- [ ] Handle exceptions at appropriate levels
- [ ] Preserve exception context with `raise ... from`
- [ ] Clean up resources with `finally` or context managers
- [ ] Don't expose sensitive data in error messages
- [ ] Test error paths - verify exit codes and messages in tests
- [ ] Inherit from TyperError for custom exceptions

### Security
- [ ] Never enable `pretty_exceptions_show_locals` in production
- [ ] Scrub sensitive values from error messages
- [ ] Log errors server-side, show brief summary to user

## Senior Advice

> "Error handling is not about preventing all errors - it is about handling them gracefully when they occur and providing meaningful feedback to users and operators."

> "The exit code is the API contract between your CLI and the world. Violate it, and every script, CI job, and operator that calls your tool will eventually break in mysterious ways."

> "Security and usability are not opposites. A good error message tells the user what went wrong without revealing implementation details that could aid an attacker."

> "The difference between a professional CLI tool and a script is how it handles the unexpected. Professional tools fail gracefully and informatively."

---

## Reference Card

See [reference-card.md](reference-card.md) for the complete reference card with exit codes, exceptions, and quick decision guides.

---

## Additional Resources

- [Typer Exceptions Documentation](https://typer.tiangolo.com/tutorial/exceptions/)
- [Typer Terminating Documentation](https://typer.tiangolo.com/tutorial/terminating/)
- [Click Exception Handling](https://click.palletsprojects.com/en/stable/exceptions/)
- [Rich Console Errors](https://rich.readthedocs.io/en/latest/console.html#console-print)
- [CLI Error Handling Best Practices](https://clig.dev/#error-handling)
- For testing error handling, see [typer-cli-testing](../typer-cli-testing/SKILL.md)
- For core Typer patterns, see [typer-cli](../typer-cli/SKILL.md)
