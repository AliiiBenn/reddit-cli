---
name: typer-cli
description: Build Typer CLI applications. Use when creating CLI apps, adding commands, handling arguments/options, prompts, subcommands, or organizing Typer projects.
disable-model-invocation: true
allowed-tools: Read,Grep,Glob,Bash
---

# Typer CLI Development Skill

Build Typer CLI applications with proper patterns for arguments, options, commands, subcommands, prompts, context handling, progress bars, Rich formatting, and advanced features.

## Quick Usage

This skill is invoked when users ask about:
- Creating a CLI application with Typer
- Adding commands, arguments, or options
- Building subcommand hierarchies
- Handling user prompts and confirmations
- Managing CLI context and callbacks
- Printing formatted output
- Handling exit codes
- Using Rich tables, panels, and progress bars
- Shell completion customization
- Path and file handling
- Environment variable configuration

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

## Topic Index

### Core Topics

| Topic | Description |
|-------|-------------|
| [arguments.md](./arguments.md) | Required and optional arguments, defaults, metavar, rich_help_panel |
| [options.md](./options.md) | Flags, required options, boolean flags, multiple values, shell_complete, parser |
| [commands.md](./commands.md) | @app.command(), name, help, epilog, deprecated |
| [subcommands.md](./subcommands.md) | add_typer(), nested subcommands, invoke_without_command |
| [context.md](./context.md) | ctx.obj, ctx.params, ctx.exit, resilient_parsing |
| [callbacks.md](./callbacks.md) | @app.callback(), precedence, is_eager |
| [prompts.md](./prompts.md) | typer.prompt, confirm, validation |
| [progress-bars.md](./progress-bars.md) | typer.progressbar, typer.track, spinners |
| [rich-integration.md](./rich-integration.md) | typer.echo, tables, panels, Console, typer.launch() |

### Advanced Topics

| Topic | Description |
|-------|-------------|
| [help-system.md](./help-system.md) | pretty_exceptions, rich_help_panel, suggest_commands |
| [completion.md](./completion.md) | CompletionItem, shell_complete, case-insensitive completion |
| [path-handling.md](./path-handling.md) | resolve_path, allow_dash, path_type |
| [file-types.md](./file-types.md) | FileText, FileBinary, lazy reading |
| [datetime.md](./datetime.md) | DateTime with custom formats |
| [environment.md](./environment.md) | envvar, show_envvar, multiple envvars fallback |
| [exit-codes.md](./exit-codes.md) | Exit codes, termination, TyperInterrupt |
| [edge-cases.md](./edge-cases.md) | Unicode, empty strings, dash handling |

### Reference Topics

| Topic | Description |
|-------|-------------|
| [anti-patterns.md](./anti-patterns.md) | 15+ anti-patterns to avoid |
| [best-practices.md](./best-practices.md) | Comprehensive checklist |
| [quick-reference.md](./quick-reference.md) | Quick reference tables |

---

## Core Patterns

### App Creation

Typer supports two approaches for creating CLI applications:

#### Implicit - `typer.run()`

For simple, single-command CLIs:

```python
import typer

def main(name: str):
    """Greet the user by name."""
    print(f"Hello {name}!")

if __name__ == "__main__":
    typer.run(main)
```

#### Explicit - `typer.Typer()`

For applications requiring subcommands, shell completion, or multiple commands:

```python
import typer

app = typer.Typer()

@app.command()
def main(name: str):
    """Greet the user by name."""
    print(f"Hello {name}!")

if __name__ == "__main__":
    app()
```

| Use Case | Approach |
|----------|----------|
| Single command, simple script | `typer.run()` |
| Multiple commands | `typer.Typer()` + `@app.command()` |
| Shell completion | `typer.Typer()` |
| Shared/installable package | `typer.Typer()` |

---

## Anti-Patterns

Common mistakes to avoid. See [anti-patterns.md](./anti-patterns.md) for detailed explanations and solutions.

1. **Using `Optional` with Default Value** - Use direct type with default instead
2. **Mixing Annotated and Non-Annotated Syntax** - Be consistent with `Annotated`
3. **Mutable Default Arguments** - Use `None` + create inside
4. **Using `print()` Instead of `typer.echo()`** - Use `typer.echo()` for proper handling
5. **Not Checking `invoked_subcommand`** - Check when using `invoke_without_command=True`
6. **Missing Exit Code Checks in Tests** - Always assert `exit_code`
7. **Using Legacy Function Decorators** - Use modern `Annotated` style
8. **Bare `return` in Command** - Use `typer.Exit()` or `typer.Abort()`
9. **Using `sys.exit()` Instead of `typer.Exit()`** - Use Typer's exit functions
10. **Global State Mutation in Callbacks** - Use `ctx.obj` for state
11. **Modifying `ctx.params` Directly** - Use `ctx.obj` instead
12. **Bare return When Error Occurs** - Use explicit error handling
13. **Mutable List Default with Options** - Use `None` + create fresh list
14. **Not Using `rich_markup_mode`** - Enable for Rich formatting in help
15. **Forgetting to Handle Empty Input in Prompts** - Handle explicitly

---

## Best Practices Checklist

See [best-practices.md](./best-practices.md) for a comprehensive checklist covering:

- App Structure
- Arguments and Options
- Commands
- Subcommands
- Prompts
- Output
- Exit Codes
- Context and State
- Environment Variables
- Testing
- Performance
- Security
- Documentation

---

## Quick Reference

See [quick-reference.md](./quick-reference.md) for:

- Argument/Option attributes table
- Option flag syntax
- Command attributes
- Exit codes
- Context attributes
- Callback precedence
- File types
- App attributes
- Common DateTime formats
- Rich markup guide
- Shell completion types

---

## Senior Advice

> "The best CLI is one that users can navigate without thinking. Clear command names, consistent flags, and helpful error messages are the hallmarks of a well-designed interface."

> "Typer's type hints are not just for show. They generate help text, enable shell completion, and catch errors early. Invest time in proper type annotations."

> "When in doubt, err on the side of more structure. A CLI that starts simple but grows organically into a tangled mess is painful to maintain. Subcommands exist for a reason."

> "Exit codes matter for scripting. When a human runs your CLI interactively, errors are visible. When a script runs your CLI, exit codes are the only way to detect failure."

> "Rich markup modes let you add flair to help text, but remember: the goal is clarity, not decoration."

---

## Related Skills

### Testing
- [typer-cli-testing](../typer-cli-testing/SKILL.md) - How to write Typer CLI tests with CliRunner

### Error Handling
- [typer-error-handling](../typer-error-handling/SKILL.md) - Error handling and exit code patterns

### Deployment
- [typer-cli-deployment](../typer-cli-deployment/SKILL.md) - Package and distribute Typer applications

### Additional Skills
- [typer-test-quality-skill](../typer-test-quality-skill/SKILL.md) - Evaluate existing Typer test quality
- [typer-advanced-params](../typer-advanced-params/SKILL.md) - Advanced parameter handling

---

## Reference Documents

- Typer documentation: https://typer.tiangolo.com/
- Typer testing: https://typer.tiangolo.com/tutorial/testing/
- CliRunner API: https://typer.tiangolo.com/api/typer/testing/
- Rich library: https://rich.readthedocs.io/

### Rules
- [rules/typer.md](../../rules/typer.md) - Typer CLI syntax and patterns
- [rules/typer-testing.md](../../rules/typer-testing.md) - Typer testing patterns

---

## Examples

See [examples/sample.md](./examples/sample.md) for a complete project management CLI example demonstrating:
- Multi-file subcommand structure
- Confirmation prompts
- State management with callbacks
- Testing with CliRunner
- Command tree organization
