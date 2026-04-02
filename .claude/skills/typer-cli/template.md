# Typer CLI Development Skill — Template

**Date:** YYYY-MM-DD
**Status:** Draft

---

## Quick Usage

When building a Typer CLI application, invoke this skill for guidance on:
- App creation (`typer.Typer()` vs `typer.run()`)
- Arguments and options (required, optional, defaults)
- Commands and subcommands
- Callbacks and context handling
- Prompts and user input
- Output formatting with Rich
- Exit codes and error handling

## Overview

Typer CLI development covers the core patterns for building command-line interfaces using Python type hints. Typer automatically converts Python function signatures into CLI interfaces, handling argument parsing, type conversion, help text generation, and shell completion.

**Key concepts:**
- **Arguments** are positional parameters (required by default)
- **Options** are named flags starting with `--` (optional by default)
- **Commands** are functions decorated with `@app.command()`
- **Subcommands** group related commands using `add_typer()`
- **Callbacks** run before commands and can define app-level options
- **Context** provides access to CLI state and invoked subcommand

---

## Topic Structure

This skill is organized into modular topic files. Refer to the main [SKILL.md](./SKILL.md) for the complete index.

### Core Topics

| Topic | File | When to Use |
|-------|------|-------------|
| Arguments | [arguments.md](./arguments.md) | Positional parameters, required vs optional |
| Options | [options.md](./options.md) | Named flags, boolean flags, multiple values |
| Commands | [commands.md](./commands.md) | Command definition, name, help, epilog |
| Subcommands | [subcommands.md](./subcommands.md) | Command grouping, nested subcommands |
| Context | [context.md](./context.md) | CLI state, ctx.obj, ctx.params |
| Callbacks | [callbacks.md](./callbacks.md) | App-level options, invoke_without_command |
| Prompts | [prompts.md](./prompts.md) | Interactive user input, confirmations |
| Progress Bars | [progress-bars.md](./progress-bars.md) | Long-running operations, spinners |
| Rich Integration | [rich-integration.md](./rich-integration.md) | Tables, panels, styled output |

### Advanced Topics

| Topic | File | When to Use |
|-------|------|-------------|
| Help System | [help-system.md](./help-system.md) | pretty_exceptions, rich_help_panel |
| Completion | [completion.md](./completion.md) | Custom shell completion |
| Path Handling | [path-handling.md](./path-handling.md) | resolve_path, allow_dash, path_type |
| File Types | [file-types.md](./file-types.md) | FileText, FileBinary, lazy reading |
| DateTime | [datetime.md](./datetime.md) | Custom date format parsing |
| Environment | [environment.md](./environment.md) | envvar, show_envvar |
| Exit Codes | [exit-codes.md](./exit-codes.md) | Exit codes, termination |
| Edge Cases | [edge-cases.md](./edge-cases.md) | Unicode, empty strings, dash |

### Reference Topics

| Topic | File | Content |
|-------|------|---------|
| Anti-Patterns | [anti-patterns.md](./anti-patterns.md) | 15+ common mistakes |
| Best Practices | [best-practices.md](./best-practices.md) | Comprehensive checklist |
| Quick Reference | [quick-reference.md](./quick-reference.md) | Reference tables |

---

## Common Patterns

### Simple Single-Command CLI

```python
# TEMPLATE: Simple single-command CLI
import typer

def main(name: str):
    """Greet the user by name."""
    typer.echo(f"Hello {name}!")

if __name__ == "__main__":
    typer.run(main)
```

### Multi-Command CLI

```python
# TEMPLATE: Multi-command CLI with Typer
import typer
from typing import Annotated

app = typer.Typer()

@app.command()
def create(
    name: Annotated[str, typer.Argument(help="Resource name")],
    verbose: Annotated[bool, typer.Option("-v", "--verbose")] = False,
):
    """Create a new resource."""
    if verbose:
        typer.echo(f"Creating: {name}")
    typer.echo(f"Created: {name}")

@app.command()
def delete(
    name: Annotated[str, typer.Argument(help="Resource name")],
    force: Annotated[bool, typer.Option("--force")] = False,
):
    """Delete a resource."""
    if not force:
        if not typer.confirm(f"Delete {name}?"):
            typer.echo("Cancelled")
            raise typer.Abort()
    typer.echo(f"Deleted: {name}")

if __name__ == "__main__":
    app()
```

### Subcommand Group

```python
# TEMPLATE: Subcommand structure
# users.py
import typer

app = typer.Typer()

@app.command()
def create(name: str):
    """Create a user."""
    typer.echo(f"Creating user: {name}")

@app.command()
def delete(name: str):
    """Delete a user."""
    typer.echo(f"Deleting user: {name}")

if __name__ == "__main__":
    app()
```

```python
# TEMPLATE: Main app with subcommand
# main.py
import typer
import users

app = typer.Typer()
app.add_typer(users.app, name="users")

if __name__ == "__main__":
    app()
```

---

## Anti-Patterns Quick Reference

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| `Optional[str] = "default"` | Unnecessary Optional | `str = "default"` |
| `list = []` as default | Mutable default | `None` + create inside |
| `print()` instead of `typer.echo()` | Poor Rich handling | Use `typer.echo()` |
| Bare `return` on error | Silent failure | Use `typer.Exit(code=1)` |
| Global state | Testing difficulty | Use `ctx.obj` |
| Modifying `ctx.params` | Read-only | Use `ctx.obj` |

---

## Best Practices Checklist

- [ ] Use `typer.Typer()` for multi-command CLIs
- [ ] Use `Annotated` syntax for all arguments/options
- [ ] Provide help text for all parameters
- [ ] Use `typer.echo()` instead of `print()`
- [ ] Always check exit codes in tests
- [ ] Use `ctx.obj` for shared state
- [ ] Handle empty input explicitly in prompts
- [ ] Document environment variables in help

---

## Related Skills

- [typer-cli-testing](../typer-cli-testing/SKILL.md) - Testing Typer CLIs
- [typer-error-handling](../typer-error-handling/SKILL.md) - Error handling patterns
- [typer-cli-deployment](../typer-cli-deployment/SKILL.md) - Packaging and distribution
- [typer-test-quality-skill](../typer-test-quality-skill/SKILL.md) - Test quality evaluation
- [typer-advanced-params](../typer-advanced-params/SKILL.md) - Advanced parameters

---

## Senior Advice

> "The best CLI is one that users can navigate without thinking. Clear command names, consistent flags, and helpful error messages are the hallmarks of a well-designed interface."

> "Typer's type hints are not just for show. They generate help text, enable shell completion, and catch errors early. Invest time in proper type annotations."

> "When in doubt, err on the side of more structure. A CLI that starts simple but grows organically into a tangled mess is painful to maintain. Subcommands exist for a reason."

> "Exit codes matter for scripting. When a human runs your CLI interactively, errors are visible. When a script runs your CLI, exit codes are the only way to detect failure."

---

## Additional Resources

- Typer documentation: https://typer.tiangolo.com/
- Typer testing: https://typer.tiangolo.com/tutorial/testing/
- CliRunner API: https://typer.tiangolo.com/api/typer/testing/
- Rich library: https://rich.readthedocs.io/

### Rules
- [rules/typer.md](../../rules/typer.md) - Typer CLI syntax and patterns
- [rules/typer-testing.md](../../rules/typer-testing.md) - Typer testing patterns
