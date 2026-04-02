# Exit Codes

Exit codes are the primary mechanism for Unix programs to communicate success or failure to calling processes.

## Exit Code Reference (Complete)

| Exit Code | Meaning | Use Case |
|-----------|---------|----------|
| `0` | Success | Normal completion |
| `1` | General error | Catch-all for errors, `typer.Abort()` |
| `2` | Usage error | Invalid arguments, `BadParameter`, `MissingOption` |
| `125` | Unknown option | `NoSuchOption` (Click) |
| `126` | Command not executable | `Invoke` failure |
| `127` | Command not found | Missing executable (subprocess) |
| `128+N` | Killed by signal N | `128 + 15 = SIGTERM` |
| `130` | Interrupted | `TyperInterrupt`, `KeyboardInterrupt`, Ctrl+C |

## Typer Exit Code Mapping

```python
# Typer.BadParameter -> exit code 2 (usage error)
# Typer.MissingOption -> exit code 2
# Typer.NoSuchOption -> exit code 125
# Typer.ValidationError -> exit code 2
# typer.Abort() -> exit code 1
# TyperInterrupt -> exit code 130
# SystemExit(0) -> exit code 0
# SystemExit(1) -> exit code 1
```

## Exit Code 127: Command Not Found

For CLIs that invoke other executables (like linting tools, formatters, etc.):

```python
import subprocess

@app.command()
def lint_files(files: list[str]):
    result = subprocess.run(["flake8"] + files, capture_output=True)
    if result.returncode == 127:
        typer.echo("Error: flake8 not installed", err=True)
        typer.echo("Install with: pip install flake8", err=True)
        raise typer.Exit(code=127)
    elif result.returncode != 0:
        typer.echo(result.stdout.decode(), err=True)
        raise typer.Exit(code=1)
    typer.echo("Lint passed!")
```

## Exit vs Return

In Typer commands, returning a value does not set the exit code. Only `typer.Exit()`, `typer.Abort()`, or unhandled exceptions affect the exit code:

```python
@app.command()
def bad_example(value: int):
    if value < 0:
        return "Negative not allowed"  # Still exits with 0!
    return f"Value: {value}"

@app.command()
def good_example(value: int):
    if value < 0:
        raise typer.BadParameter("Negative not allowed", param_hint="value")
    typer.echo(f"Value: {value}")
```

## Application-Specific Exit Codes

For application-specific errors, use codes 3 and above:

```python
# Application-specific exit codes
EXIT_SUCCESS = 0
EXIT_GENERAL_ERROR = 1
EXIT_USAGE_ERROR = 2
EXIT_NOT_FOUND = 3
EXIT_ALREADY_EXISTS = 4

@app.command()
def delete(name: str):
    if not exists(name):
        typer.echo(f"Error: '{name}' not found", err=True)
        raise typer.Exit(code=EXIT_NOT_FOUND)
    delete_user(name)
```

## Reference: Exit Codes Quick Reference

| Code | Name | Common Cause |
|------|------|--------------|
| 0 | Success | Normal completion |
| 1 | General error | `typer.Abort()`, unspecified |
| 2 | Usage error | `BadParameter`, `MissingOption`, `MissingArgument` |
| 125 | Unknown option | `NoSuchOption` |
| 126 | Not executable | Command `Invoke` failure |
| 127 | Not found | Missing executable (subprocess) |
| 130 | Interrupted | `TyperInterrupt`, `KeyboardInterrupt` |
