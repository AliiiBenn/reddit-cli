# Typer CLI Testing Template

**Date:** 2026-03-31

This document provides a template and structure reference for Typer CLI testing documentation. For actual testing content, see the individual topic files listed in [SKILL.md](SKILL.md).

## File Structure

```
typer-cli-testing/
├── SKILL.md                    # Index global + overview + redirections
├── clirunner.md                # CliRunner constructor, parameters
├── invocation.md               # runner.invoke() parameters
├── result-object.md            # Result object (exit_code, output, stdout, stderr, exception, exception_info)
├── basic-testing.md            # Basic testing patterns
├── exit-codes.md               # Exit code testing (0, 1, 2, 125, 126, 127, 130)
├── output-verification.md      # stdout/stderr verification, Rich output
├── prompts-testing.md           # Testing prompts (input, order, retry)
├── subcommands-testing.md       # Testing subcommands and nested commands
├── callbacks-testing.md         # Testing callbacks, invoke_without_command
├── context-testing.md          # Testing Context (ctx.obj, ctx.params)
├── isolated-filesystem.md      # isolated_filesystem() usage
├── file-operations.md          # Testing file operations
├── exception-testing.md         # Testing result.exception, exception_info
├── mix-stderr.md               # mix_stderr parameter and behavior
├── progressbar-testing.md       # Testing progress bars
├── rich-output-testing.md       # Testing Rich markup output
├── mocking.md                  # Mocking patterns (os.getenv, typer.launch, Path)
├── pytest-configuration.md      # conftest.py, fixtures, pytest.ini
├── parametrization.md           # pytest.mark.parametrize
├── integration-testing.md       # Integration tests (subprocess)
├── coverage.md                  # pytest-cov configuration
├── parallel-tests.md            # Parallel testing with isolated_filesystem
├── troubleshooting.md            # Troubleshooting guide
├── anti-patterns.md             # Anti-patterns
├── common-mistakes.md           # Common mistakes checklist
└── examples/
    └── sample.md               # Complete sample application and tests
```

## Quick Reference

### Minimal Test

```python
from typer.testing import CliRunner
from app.main import app

runner = CliRunner()

def test_basic():
    result = runner.invoke(app, ["arg1", "--option", "value"])
    assert result.exit_code == 0
    assert "expected output" in result.output
```

### With Prompts

```python
def test_with_prompt():
    result = runner.invoke(
        app,
        ["create-user"],
        input="john@example.com\n"
    )
    assert result.exit_code == 0
```

### With Isolated Filesystem

```python
def test_file_operation():
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["export", "--format", "csv"])
        assert result.exit_code == 0
        assert Path("export.csv").exists()
```

## Topic File Format

Each topic file should follow this format:

```markdown
# Topic Title

**Date:** YYYY-MM-DD

## Overview
Brief description of the topic.

## Content
Detailed explanations and code examples.

## See Also
Related topic files.
```

## See Also

- [SKILL.md](SKILL.md) - Main index
- [examples/sample.md](examples/sample.md) - Complete example
