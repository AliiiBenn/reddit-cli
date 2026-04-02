# Quick Reference

Quick reference tables for Typer CLI development.

## Argument/Option Attributes

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `help` | Help text shown in --help | `typer.Option(help="Output file")` |
| `default` | Default value if not provided | `typer.Option(default="out.txt")` |
| `default_factory` | Function called to get default | `typer.Option(default_factory=now)` |
| `envvar` | Environment variable name | `typer.Option(envvar="API_KEY")` |
| `hidden` | Hide from help text | `typer.Option(hidden=True)` |
| `show_default` | Show default in help | `typer.Option(show_default=False)` |
| `is_eager` | Parse before other options | `typer.Option(is_eager=True)` |
| `prompt` | Interactive prompt if not provided | `typer.Option(prompt=True)` |
| `nargs` | Number of values (for tuples) | `typer.Option(nargs=2)` |
| `completion` | Shell completion type | `typer.CompletionType.FILE` |
| `metavar` | Custom text in help | `typer.Argument(metavar="USERNAME")` |
| `rich_help_panel` | Organize help into panels | `typer.Option(rich_help_panel="Config")` |
| `show_envvar` | Show env var in help | `typer.Option(show_envvar=False)` |
| `shell_complete` | Custom completion function | `typer.Option(shell_complete=complete_fn)` |
| `case_sensitive` | Case-sensitive option names | `typer.Option(case_sensitive=False)` |
| `parser` | Custom type parser | `typer.Option(parser=parse_port)` |
| `prompt_required` | Always prompt even with value | `typer.Option(prompt_required=True)` |
| `resolve_path` | Resolve symlinks | `typer.Path(resolve_path=True)` |
| `allow_dash` | Accept stdin/stdout dash | `typer.Path(allow_dash=True)` |
| `path_type` | Return type for paths | `typer.Path(path_type=str)` |

## Option Flag Syntax

| Syntax | Behavior |
|--------|----------|
| `--flag` | Boolean flag (True when present) |
| `--flag/--no-flag` | Negatable flag |
| `-v, --verbose` | Short and long form |
| `--value TEXT` | Option with required value |
| `--name KEY=VALUE` | Key-value pair |

## Command Attributes

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `name` | CLI command name | `@app.command(name="create-user")` |
| `help` | Full help text | `@app.command(help="Create...")` |
| `short_help` | Brief help for main list | `@app.command(short_help="Create")` |
| `epilog` | Text after help | `@app.command(epilog="Version 2.0")` |
| `deprecated` | Mark as deprecated | `@app.command(deprecated=True)` |
| `hidden` | Hide from help | `@app.command(hidden=True)` |
| `no_args_is_help` | Show help if no args | `typer.Typer(no_args_is_help=True)` |
| `add_help_option` | Add --help option | `typer.Typer(add_help_option=False)` |
| `suggest_commands` | Suggest similar commands | `typer.Typer(suggest_commands=True)` |
| `rich_help_panel` | Organize help panels | `@app.command(rich_help_panel="User")` |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Usage error |
| 125 | Unknown option |
| 126 | Command not found |
| 127 | External command not found |
| 130 | Interrupted (Ctrl+C) |

## Context Attributes

| Attribute | Description |
|-----------|-------------|
| `ctx.invoked_subcommand` | Name of invoked subcommand or None |
| `ctx.args` | Extra raw arguments list |
| `ctx.params` | Parsed parameters dict |
| `ctx.command` | Command object being executed |
| `ctx.obj` | Custom object for passing state |
| `ctx.resilient_parsing` | True during shell completion |
| `ctx.exit(code=0)` | Exit early with code |
| `ctx.parent` | Parent context in nested subcommands |

## Callback Precedence

```
add_typer(callback=...) > @subapp.callback() > typer.Typer(callback=...)
```

## File Types

| Type | Purpose |
|------|---------|
| `typer.FileText` | Read text file |
| `typer.FileTextWrite` | Write text file |
| `typer.FileBinary` | Read binary file |
| `typer.FileBinaryWrite` | Write binary file |
| `typer.Path` | Path argument with validation |

## App Attributes

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `rich_markup_mode` | Markup mode for help | `typer.Typer(rich_markup_mode="markdown")` |
| `pretty_exceptions_enable` | Pretty print exceptions | `typer.Typer(pretty_exceptions_enable=False)` |
| `pretty_exceptions_show_locals` | Show local vars in traceback | Use carefully in prod |
| `no_args_is_help` | Show help when no args | `typer.Typer(no_args_is_help=True)` |
| `suggest_commands` | Suggest similar commands | `typer.Typer(suggest_commands=True)` |
| `add_help_option` | Enable --help | `typer.Typer(add_help_option=False)` |
| `context_settings` | Context configuration | `typer.Typer(context_settings={...})` |

## Additional Features Summary

| Feature | Category | Description |
|---------|----------|-------------|
| `metavar` | Arguments | Customize text in help display |
| `rich_help_panel` | Arguments | Organize arguments into visual panels |
| `show_envvar` | Arguments/Options | Control env var visibility in help |
| `shell_complete` | Options | Custom completion with CompletionItem |
| `case_sensitive` | Options | Case-insensitive option names |
| `parser` | Options | Custom type validation function |
| `prompt_required` | Options | Force prompt even with CLI value |
| `ctx.obj` | Context | Share state between commands |
| `resilient_parsing` | Context | Skip validation during completion |
| `ctx.exit()` | Context | Early exit without exception |
| `ctx.command` | Context | Access command object info |
| `name` | Commands | Custom CLI command name |
| `short_help` | Commands | Brief help for main listing |
| `epilog` | Commands | Text at end of help |
| `deprecated` | Commands | Mark command as deprecated |
| `no_args_is_help` | App | Show help when no arguments |
| `suggest_commands` | App | Suggest similar command names |
| `typer.track()` | Progress | Progress bar for generators |
| `console.status()` | Progress | Custom spinner with Rich |
| `typer.launch()` | Rich | Open URLs, files, browsers |
| `Console(stderr=True)` | Rich | Output to stderr |
| `rich_markup_mode` | App | Markdown or Rich markup in help |
| `pretty_exceptions_*` | Help | Control exception formatting |
| `resolve_path` | Path | Resolve symbolic links |
| `allow_dash` | Path | Accept stdin/stdout dash |
| `path_type` | Path | Control return type (str/Path) |
| `FileTextWrite` | Files | Write text files |
| `FileBinaryWrite` | Files | Write binary files |
| `DateTime` with formats | Types | Custom date format parsing |
| Multiple envvars | Options | Fallback env var chain |
| `err=True` | Exit | Write to stderr |
| `BadParameter` with param_hint | Exit | Parameter-aware validation errors |
| `TyperInterrupt` | Exit | Handle Ctrl+C gracefully |
| `__main__.py` | Structure | Entry point for `python -m` |
| `add_typer()` without name | Subcommands | Merge commands at top level |
| `CallbackParam` | Callbacks | Access parameter metadata |

## Common DateTime Formats

| Format | Example | Description |
|--------|---------|-------------|
| `%Y-%m-%d` | 2024-12-25 | ISO date |
| `%d/%m/%Y` | 25/12/2024 | European date |
| `%m/%d/%Y` | 12/25/2024 | US date |
| `%Y-%m-%d %H:%M:%S` | 2024-12-25 14:30:00 | Date with time |
| `%Y-%m-%dT%H:%M:%S` | 2024-12-25T14:30:00 | ISO 8601 |

## Rich Markup

| Markup | Effect |
|--------|--------|
| `[bold]text[/bold]` | Bold text |
| `[italic]text[/italic]` | Italic text |
| `[cyan]text[/cyan]` | Cyan color |
| `[green]text[/green]` | Green color |
| `[red]text[/red]` | Red color |
| `[yellow]text[/yellow]` | Yellow color |

## Shell Completion Types

| Type | Purpose |
|------|---------|
| `typer.CompletionType.FILE` | File path completion |
| `typer.CompletionType.DIR` | Directory completion |
| Custom `CompletionItem` | Custom completion with help |
