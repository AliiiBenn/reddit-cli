---
name: typer-cli-testing
description: Learn to write Typer CLI tests. Use when asked "how do I test a Typer app?", or when writing tests for Typer commands, prompts, or exit codes.
disable-model-invocation: true
allowed-tools: Read,Grep,Glob,Bash
---

# Typer CLI Testing Skill

**Date:** 2026-03-31

Learn to write effective Typer CLI tests using CliRunner. This skill teaches *how to write* tests. For *evaluating* existing tests, see [typer-test-quality-skill](../typer-test-quality-skill/SKILL.md).

## Quick Usage

```bash
# Basic test invocation
pytest tests/test_cli.py -v

# Run tests matching pattern
pytest -k "test_user" -v

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/test_main.py::test_create_user -v
```

## Overview

Typer CLI testing verifies the actual command-line interface works correctly. Unlike unit tests that test individual functions, CLI tests verify:

- **Exit Codes** - Does the command succeed (0) or fail (non-zero) as expected?
- **Output** - Does the command print the correct text to stdout/stderr?
- **Prompts** - Does interactive input work when `typer.prompt()` is used?
- **Arguments** - Do all argument combinations produce correct results?
- **Options** - Do flags modify behavior correctly?

The goal is **maximum E2E coverage** - test the CLI interface, not just the underlying logic.

## Topics Index

### Getting Started
- [clirunner.md](clirunner.md) - CliRunner constructor, parameters
- [invocation.md](invocation.md) - runner.invoke() parameters
- [result-object.md](result-object.md) - Result object attributes (exit_code, output, stdout, stderr, exception, exception_info)
- [basic-testing.md](basic-testing.md) - Basic testing patterns

### Core Testing Topics
- [exit-codes.md](exit-codes.md) - Exit code testing (0, 1, 2, 125, 126, 127, 130)
- [output-verification.md](output-verification.md) - stdout/stderr verification
- [prompts-testing.md](prompts-testing.md) - Testing prompts (input, order, retry)
- [subcommands-testing.md](subcommands-testing.md) - Testing subcommands and nested commands
- [callbacks-testing.md](callbacks-testing.md) - Testing callbacks, invoke_without_command
- [context-testing.md](context-testing.md) - Testing Context (ctx.obj, ctx.params)

### Advanced Topics
- [isolated-filesystem.md](isolated-filesystem.md) - isolated_filesystem() usage
- [file-operations.md](file-operations.md) - Testing file operations
- [exception-testing.md](exception-testing.md) - Testing result.exception, exception_info
- [mix-stderr.md](mix-stderr.md) - mix_stderr parameter and behavior
- [progressbar-testing.md](progressbar-testing.md) - Testing progress bars
- [rich-output-testing.md](rich-output-testing.md) - Testing Rich markup output

### Testing Infrastructure
- [mocking.md](mocking.md) - Mocking patterns (os.getenv, typer.launch, Path)
- [pytest-configuration.md](pytest-configuration.md) - conftest.py, fixtures, pytest.ini
- [parametrization.md](parametrization.md) - pytest.mark.parametrize
- [integration-testing.md](integration-testing.md) - Integration tests (subprocess)
- [coverage.md](coverage.md) - pytest-cov configuration
- [parallel-tests.md](parallel-tests.md) - Parallel testing with isolated_filesystem

### Reference
- [troubleshooting.md](troubleshooting.md) - Troubleshooting guide
- [anti-patterns.md](anti-patterns.md) - Anti-patterns
- [common-mistakes.md](common-mistakes.md) - Common mistakes checklist

### Examples
- [examples/sample.md](examples/sample.md) - Complete sample application and tests

## Related Skills

| Skill | Purpose |
|-------|---------|
| [typer-cli](../typer-cli/SKILL.md) | Build Typer CLI applications (basic patterns) |
| [typer-test-quality](../typer-test-quality/SKILL.md) | Evaluate existing test quality |
| [typer-error-handling](../typer-error-handling/SKILL.md) | Handle errors and exit codes |
| [python-test-quality](../python-test-quality/SKILL.md) | General Python test quality |

## Testing Workflow

1. **Write the test first** - TDD approach for CLI development
2. **Run the test** - Verify it fails for the right reason
3. **Implement the feature** - Make the test pass
4. **Add edge cases** - Test failure modes
5. **Refactor** - Ensure tests still pass

## Senior Advice

> "Test the CLI interface, not the implementation. If you refactor the internals, your tests should still pass."

> "Every `runner.invoke()` without an `exit_code` check is a silent failure waiting to happen. Be explicit."

> "If a command has a prompt, it MUST have a test with `input=`. No exceptions. A prompt without a test is untested user input."

> "The difference between a test that catches bugs and one that doesn't often comes down to checking the failure case, not just the happy path."

> "When writing CLI tests, think from the user's perspective: What could go wrong? What should happen then? Write tests for those scenarios."

> "A test that doesn't verify exit codes is like a test that doesn't assert anything - it gives you false confidence."

## External Resources

- Typer Testing Documentation: https://typer.tiangolo.com/tutorial/testing/
- CliRunner API: https://typer.tiangolo.com/api/typer/testing/
- pytest Documentation: https://docs.pytest.org/

---

**Note:** This skill teaches *how to write* tests. The existing `typer-test-quality-skill` *evaluates* existing tests. Use both together: write tests with this skill, then evaluate them with the quality skill.
