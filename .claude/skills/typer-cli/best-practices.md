# Best Practices Checklist

Use this checklist when building Typer CLI applications.

## App Structure

- [ ] Use `typer.Typer()` for multi-command CLIs
- [ ] Use `typer.run()` only for simple, single-command scripts
- [ ] Group related commands into subcommands using `add_typer()`
- [ ] Separate command modules into different files for large CLIs
- [ ] Use `__main__.py` for `python -m package` entry points
- [ ] Define clear command hierarchy (max 2-3 levels deep)
- [ ] Use meaningful subcommand names (e.g., `users`, `items`)

## Arguments and Options

- [ ] Use `Annotated` syntax for all arguments and options
- [ ] Provide help text for all parameters with `help=`
- [ ] Use appropriate defaults to avoid `Optional` when possible
- [ ] Avoid mutable default arguments (use `None` + create inside)
- [ ] Name options clearly: `--verbose`, `--force`, `--output`
- [ ] Use `metavar` to customize help display
- [ ] Use `rich_help_panel` to organize complex command help
- [ ] Use `show_envvar` to control env var visibility
- [ ] Use `show_default` when defaults are important
- [ ] Use `hidden=True` for internal options (not meant for users)

## Commands

- [ ] Each command has a clear, single responsibility
- [ ] Use descriptive command names (underscores become dashes in CLI)
- [ ] Include docstrings for help text
- [ ] Validate inputs and return appropriate exit codes
- [ ] Use `name` parameter when CLI name differs from function name
- [ ] Add `short_help` for main help listing
- [ ] Use `epilog` for additional help information
- [ ] Mark deprecated commands with `deprecated=True`
- [ ] Use `no_args_is_help=True` when appropriate
- [ ] Enable `suggest_commands=True` to help users with typos

## Subcommands

- [ ] Use `add_typer()` for composable command groups
- [ ] Name subcommand groups meaningfully (e.g., `users`, `items`)
- [ ] Use callbacks for shared options across subcommands
- [ ] Keep subcommand depth to 2-3 levels maximum
- [ ] Use `invoke_without_command=True` for subapp callbacks that need to run
- [ ] Consider multi-file structure for large CLI applications

## Prompts

- [ ] Use `typer.Option(prompt=True)` for simple confirmations
- [ ] Use `typer.prompt()` for complex user input
- [ ] Provide sensible defaults in prompts
- [ ] Always validate prompt input
- [ ] Use `hide_input=True` for password-like input
- [ ] Use `typer.confirm()` for yes/no decisions
- [ ] Handle empty input explicitly

## Output

- [ ] Use `typer.echo()` instead of `print()`
- [ ] Use Rich for formatted tables, panels, and styled output
- [ ] Send errors to stderr using `typer.echo(..., err=True)`
- [ ] Provide clear, actionable error messages
- [ ] Use `typer.launch()` for opening URLs and files
- [ ] Use `rich_markup_mode` for formatted help text
- [ ] Keep output consistent across commands

## Exit Codes

- [ ] Exit with code 0 on success
- [ ] Exit with non-zero code on errors
- [ ] Use `typer.Exit(code=N)` for explicit exit codes
- [ ] Use `typer.Abort()` for unrecoverable errors
- [ ] Use `ctx.exit()` for early command exit
- [ ] Handle `TyperInterrupt` for graceful Ctrl+C handling
- [ ] Use standard exit code conventions (1 = error, 2 = usage error)

## Context and State

- [ ] Use `ctx.obj` for sharing state between commands
- [ ] Never modify `ctx.params` directly
- [ ] Use `ctx.resilient_parsing` in validation callbacks for shell completion
- [ ] Check `ctx.invoked_subcommand` when using `invoke_without_command=True`
- [ ] Use `ctx.parent` to access parent context in nested subcommands

## Environment Variables

- [ ] Document environment variables in help text
- [ ] Use `show_envvar=False` for internal/implementation env vars
- [ ] Support fallback environment variables when appropriate
- [ ] Follow precedence: CLI > env var > default

## Testing

- [ ] Test commands using `CliRunner.invoke()`
- [ ] Always assert `exit_code` in tests
- [ ] Verify both stdout and stderr output
- [ ] Test prompt interactions with `input=` parameter
- [ ] Test with valid, invalid, and edge case inputs
- [ ] For testing guidance, see [typer-cli-testing](../typer-cli-testing/SKILL.md)

## Performance

- [ ] Use lazy imports for heavy dependencies
- [ ] Keep startup time minimal for frequently-called CLIs
- [ ] Consider `typer-slim` for minimal dependencies
- [ ] Use `typer.track()` for long-running operations
- [ ] Use `console.status()` for indeterminate progress

## Security

- [ ] Never expose sensitive data in help text
- [ ] Use `hidden=True` for secret options
- [ ] Sanitize user input before using in file operations
- [ ] Handle `pretty_exceptions_show_locals` with care (never in production)
- [ ] Use `TyperInterrupt` to clean up sensitive state on Ctrl+C

## Documentation

- [ ] Write clear docstrings for all commands
- [ ] Provide `short_help` for main help display
- [ ] Use `epilog` for additional context
- [ ] Document all options with `help=`
- [ ] Provide usage examples in docstrings or epilog
- [ ] Cross-reference related skills (testing, deployment, error handling)
