---
name: typer-test-quality
description: Evaluate Typer CLI test quality. Use when reviewing Typer tests, assessing CLI test suites, or asked "how good are our Typer CLI tests?". Focuses on E2E command testing, exit codes, output verification, and prompt handling. Generates markdown report to reports/tests/typer-test-report-<date>. Supports --path, --report, --focus flags.
disable-model-invocation: true
allowed-tools: Read,Grep,Glob,Bash
---

# Typer CLI Test Quality Review Skill

Evaluate Typer CLI test quality with focus on E2E command testing.

## Quick Usage

```bash
/typer-test-quality
/typer-test-quality --path=src
/typer-test-quality --report
/typer-test-quality --focus=commands
```

## Report Output

Reports are generated to: `reports/tests/typer-test-report-YYYY-MM-DD.md`

```bash
# Generate report with today's date
/typer-test-quality --report

# Generate for specific path
/typer-test-quality --path=app/cli --report

# Focus on command coverage
/typer-test-quality --path=app --focus=commands --report
```

The report filename uses the current system date:
- Format: `typer-test-report-YYYY-MM-DD.md`
- Example: `typer-test-report-2026-03-31.md`

## Overview

Typer CLI testing is about verifying the actual command-line interface works correctly:

1. **Exit Codes** - Does the command succeed or fail as expected?
2. **Output** - Does the command print the right things?
3. **Prompts** - Does interactive input work correctly?
4. **Arguments** - Do all argument combinations work?
5. **Options** - Do flags and options modify behavior correctly?

**The goal is maximum E2E coverage - test the CLI, not just the underlying logic.**

## Typer CLI Testing Fundamentals

### CliRunner

```python
from typer.testing import CliRunner
from app.main import app

runner = CliRunner()

def test_basic():
    result = runner.invoke(app, ["name", "--city", "Berlin"])
```

### What to Verify

```python
def test_command():
    result = runner.invoke(app, ["arg1", "--option", "value"])

    # 1. Exit code (0 for success, non-zero for errors)
    assert result.exit_code == 0

    # 2. stdout output
    assert "expected text" in result.output

    # 3. Or check stdout/stderr separately
    assert "success" in result.stdout
    assert "error" not in result.stderr
```

## Test Quality Dimensions

### 1. Command Coverage (35%)

Measures whether all CLI commands are tested.

| Check | Weight | Description |
|-------|--------|-------------|
| Each command has tests | 15 | No untested commands |
| Argument combinations | 10 | Required + optional args |
| Option variations | 10 | Different flag combinations |

### 2. Exit Code Verification (20%)

Measures proper error handling.

| Check | Weight | Description |
|-------|--------|-------------|
| Success exits with 0 | 8 | Happy path returns 0 |
| Failures return non-zero | 7 | Errors return proper codes |
| Specific error codes | 5 | Different failures, different codes |

### 3. Output Verification (20%)

Measures whether output is tested.

| Check | Weight | Description |
|-------|--------|-------------|
| stdout checked | 8 | Correct output verified |
| stderr checked | 6 | Error messages verified |
| Exact output match | 6 | Precise output assertions |

### 4. Interactive Testing (15%)

Measures prompt handling coverage.

| Check | Weight | Description |
|-------|--------|-------------|
| Prompts with input | 8 | `input=` parameter used |
| Default values | 4 | Empty input handled |
| Invalid input | 3 | Bad input rejected |

### 5. Edge Cases (10%)

Measures boundary condition testing.

| Check | Weight | Description |
|-------|--------|-------------|
| Empty arguments | 4 | Missing required args |
| Invalid values | 3 | Wrong types handled |
| Boundary values | 3 | Min/max values tested |

## E2E Test Patterns

### Basic Command Test

```python
# Good - tests the actual command
def test_hello_command():
    result = runner.invoke(app, ["Camila"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.output

# Bad - tests underlying function, not the command
def test_hello_function():
    from app.main import hello
    assert hello("Camila") == "Hello Camila"
```

### Command with Options

```python
# Good - tests all option combinations
def test_greet_with_city():
    result = runner.invoke(app, ["Camila", "--city", "Berlin"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.output
    assert "coffee in Berlin" in result.output

def test_greet_without_city():
    result = runner.invoke(app, ["Camila"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.output
    assert "coffee" not in result.output
```

### Command with Required Option

```python
# Good - tests the prompt interaction
def test_email_with_input():
    result = runner.invoke(
        app,
        ["Camila"],
        input="camila@example.com\n"
    )
    assert result.exit_code == 0
    assert "camila@example.com" in result.output
```

### Error Handling

```python
# Good - tests error cases
def test_missing_required_arg():
    result = runner.invoke(app, [])  # No args
    assert result.exit_code != 0

def test_invalid_option():
    result = runner.invoke(app, ["--invalid-flag"])
    assert result.exit_code != 0
    assert "Error" in result.output or "invalid" in result.output.lower()
```

### Subcommands

```python
# For apps with subcommands
def test_create_subcommand():
    result = runner.invoke(app, ["create", "--name", "project"])
    assert result.exit_code == 0

def test_list_subcommand():
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
```

## Anti-Patterns

### Testing Logic Instead of CLI

```python
# Bad - tests the function, not the CLI
def test_process_data():
    from app.commands import process
    result = process({"key": "value"})
    assert result == expected

# Good - tests the command invocation
def test_process_command():
    result = runner.invoke(app, ["process", "--key", "value"])
    assert result.exit_code == 0
    assert "success" in result.output
```

### Missing Exit Code Check

```python
# Bad - doesn't verify exit code
def test_command():
    result = runner.invoke(app, ["arg"])
    assert "expected" in result.output
    # Exit code not checked!

# Good - always check exit code
def test_command():
    result = runner.invoke(app, ["arg"])
    assert result.exit_code == 0
    assert "expected" in result.output
```

### Ignoring Failures

```python
# Bad - assumes success
def test_command():
    result = runner.invoke(app, ["arg"])
    assert "output" in result.output

# Good - explicit exit code
def test_command():
    result = runner.invoke(app, ["arg"])
    assert result.exit_code == 0, f"Command failed: {result.output}"
    assert "output" in result.output
```

### Only Testing Happy Path

```python
# Bad - only tests success
def test_all_commands():
    assert runner.invoke(app, ["start"]).exit_code == 0
    assert runner.invoke(app, ["stop"]).exit_code == 0

# Good - tests success AND failures
def test_start_success():
    result = runner.invoke(app, ["start"])
    assert result.exit_code == 0

def test_start_already_running():
    result = runner.invoke(app, ["start"])  # Second time
    assert result.exit_code != 0
    assert "already running" in result.output.lower()
```

### Not Testing Interactive Prompts

```python
# Bad - ignores prompt testing
def test_user_creation():
    # Missing input for prompt!
    result = runner.invoke(app, ["create-user"])
    # Result is unpredictable

# Good - provides all inputs
def test_user_creation():
    result = runner.invoke(
        app,
        ["create-user"],
        input="john@example.com\nJohn Doe\ny\n"
    )
    assert result.exit_code == 0
    assert "User created" in result.output
```

## Analyzing Typer Test Quality

### Stage 1: Find Test Files

```bash
# Find Typer test files
find . -name "test_*.py" -o -name "*_test.py" | xargs grep -l "CliRunner\|typer" 2>/dev/null

# List all test files in app
find app -name "test_*.py" -o -name "*_test.py"

# Count test functions
grep -r "def test_" --include="*.py" | wc -l
```

### Stage 2: Analyze Command Coverage

```bash
# Find all app definitions
grep -r "typer.Typer\|app = " --include="*.py" | grep -v test

# Find all @app.command or @app.command()
grep -r "@.*\.command\(\)" --include="*.py" | grep -v test

# List defined commands
grep -rh "invoke(app, \[" --include="*.py" | grep -oP '"\K[^"]+' | sort | uniq
```

### Stage 3: Check Exit Code Testing

```bash
# Find tests that check exit_code
grep -rn "exit_code" tests/ --include="*.py"

# Find tests that DON'T check exit_code
grep -rn "runner.invoke" tests/ --include="*.py" | while read line; do
    file=$(echo "$line" | cut -d: -f1)
    linenum=$(echo "$line" | cut -d: -f2)
    if ! sed -n "${linenum}p" "$file" | grep -q "exit_code"; then
        echo "$file:$linenum: missing exit_code check"
    fi
done
```

### Stage 4: Check Output Verification

```bash
# Find output checks
grep -rn "result.output\|result.stdout\|result.stderr" tests/ --include="*.py"

# Find assertions on output
grep -rn 'assert.*in.*output\|assert.*output' tests/ --include="*.py"
```

### Stage 5: Check Prompt Testing

```bash
# Find tests with input parameter
grep -rn 'input=' tests/ --include="*.py"

# Find tests that SHOULD have input but don't
grep -rn "prompt=True" app/ --include="*.py" | while read line; do
    cmd=$(echo "$line" | grep -oP '\w+\(' | head -1 | tr -d '(')
    file=$(echo "$line" | cut -d: -f1)
    if ! grep -q "input=" tests/"$(basename ${file%.py}_test.py)" 2>/dev/null; then
        echo "Prompt found in $file but no input= in tests"
    fi
done
```

## Test Report Format

**Output:** `reports/tests/typer-test-report-YYYY-MM-DD.md`

```markdown
# Typer CLI Test Quality Report

**Generated:** YYYY-MM-DD
**Path Analyzed:** /path/to/app
**Report Location:** reports/tests/typer-test-report-YYYY-MM-DD.md

## Overall Score: 68/100 (Good)

| Dimension | Score | Weight | Weighted | Status |
|-----------|-------|--------|----------|--------|
| Command Coverage | 28/35 | 35% | 28.0 | Good |
| Exit Code Verification | 12/20 | 20% | 12.0 | Warning |
| Output Verification | 14/20 | 20% | 14.0 | Good |
| Interactive Testing | 6/15 | 15% | 6.0 | Critical |
| Edge Cases | 8/10 | 10% | 8.0 | Good |

**Grade: C+ (Average)**

---

## Executive Summary

| Metric | Value | Status |
|--------|-------|--------|
| CLI commands | 8 | - |
| Commands with tests | 6 | Good |
| Test functions | 45 | Good |
| Exit code checks | 32/45 (71%) | Warning |
| Output verifications | 40/45 (89%) | Good |
| Prompt tests | 3 | Critical |
| E2E coverage | 75% | Good |

---

## Command Coverage

### Commands and Test Status

| Command | Args | Options | Tests | Status |
|---------|------|---------|-------|--------|
| `start` | 1 | 2 | 4 | Good |
| `stop` | 0 | 0 | 3 | Good |
| `restart` | 0 | 1 | 0 | **Missing** |
| `status` | 0 | 1 | 2 | Good |
| `create-user` | 0 | 2 | 1 | Warning |
| `delete-user` | 1 | 1 | 0 | **Missing** |
| `list-users` | 0 | 2 | 3 | Good |
| `config` | 0 | 3 | 0 | **Missing** |

### Missing Command Tests

| Command | Priority | Reason |
|---------|----------|--------|
| `restart` | High | Critical operation |
| `delete-user` | Critical | Data loss risk |
| `config` | Medium | User configuration |

---

## Exit Code Analysis

### Proper Exit Code Testing

| File | Test | Checks Exit Code |
|------|------|------------------|
| test_main.py | test_start | Yes |
| test_main.py | test_stop | Yes |
| test_users.py | test_list | Yes |

### Missing Exit Code Checks

| File | Test | Issue |
|------|------|-------|
| test_main.py | test_status | No exit_code check |
| test_users.py | test_create | Only output checked |
| test_config.py | test_set | Missing assertion |

---

## Output Verification Analysis

### Good Output Tests

```python
# test_main.py:test_start
result = runner.invoke(app, ["start"])
assert result.exit_code == 0
assert "Starting..." in result.output
assert "Service started" in result.output
```

### Weak Output Tests

| File | Test | Issue |
|------|------|-------|
| test_users.py | test_delete | Only checks "deleted", not full output |
| test_config.py | test_get | No output assertion |

---

## Interactive Testing (Prompts)

### Prompts Found

| Command | Parameter | Prompt For |
|---------|-----------|------------|
| `create-user` | email | Email address |
| `create-user` | name | Full name |
| `config-set` | value | Config value |

### Prompt Test Coverage

| Command | Has input= Test | Status |
|---------|-----------------|--------|
| `create-user` | Yes (1 test) | Good |
| `config-set` | No | **Missing** |

### Missing Prompt Tests

| Command | Prompt | Recommended Input |
|---------|--------|-------------------|
| `config-set` | value | "new_value\n" |

---

## Edge Case Testing

### Good Edge Case Tests

| Test | Edge Case |
|------|-----------|
| test_start_twice | Already running |
| test_delete_nonexistent | Missing user |
| test_invalid_email | Bad email format |

### Missing Edge Cases

| Edge Case | Command | Priority |
|-----------|---------|----------|
| Empty arguments | create-user | High |
| Special characters | create-user | Medium |
| Very long input | config-set | Low |

---

## Recommendations

### Critical Priority

1. **Add tests for restart command**
   - Critical operation with no tests
   - Need to verify restart behavior

2. **Add delete-user tests**
   - Data loss risk without tests
   - Should verify confirmation prompt

3. **Add exit code checks to 13 tests**
   - 13 tests don't verify exit_code
   - Silent failures could go unnoticed

4. **Add prompt tests for config-set**
   - Interactive command without input= test
   - User may not know what to enter

### Medium Priority

5. **Add edge cases for create-user**
   - Empty name, invalid email format
   - Special characters in input

6. **Add tests for config command**
   - All subcommands untested
   - User configuration is important

7. **Verify stderr output**
   - Only stdout is being checked
   - Errors should go to stderr

---

## GitHub Issue Draft

```markdown
## Improve Typer CLI test coverage

### Problem

CLI tests are incomplete:
- 2 commands have no tests (restart, delete-user)
- 13 tests don't check exit_code
- Prompt tests missing for config-set

### Impact

- Silent failures in CI
- delete-user could lose data without notice
- restart behavior untested

### Current State

- Command coverage: 75% (6/8 commands)
- Exit code checks: 71%
- Prompt coverage: 50%

### Proposed Changes

1. Add restart command tests
2. Add delete-user tests with confirmation
3. Add exit_code checks to 13 tests
4. Add input= for config-set prompt

### Effort

~3 hours across 5 files
```

---

## Confirmation

**This skill will NOT modify any code.** It only analyzes and reports findings.

**This skill will NOT create issues without your confirmation.**

---

## Scoring System

### Score Calculation

| Dimension | Weight | Max Score |
|-----------|--------|-----------|
| Command Coverage | 35% | 35 |
| Exit Code Verification | 20% | 20 |
| Output Verification | 20% | 20 |
| Interactive Testing | 15% | 15 |
| Edge Cases | 10% | 10 |
| **Total** | **100%** | **100** |

### Grade Scale

| Grade | Score | Interpretation |
|-------|-------|----------------|
| A+ | 95-100 | Exceptional - comprehensive E2E |
| A | 90-94 | Excellent - minimal gaps |
| A- | 85-89 | Very Good - minor improvements |
| B+ | 80-84 | Good - solid foundation |
| B | 75-79 | Good - some gaps |
| B- | 70-74 | Acceptable - improvements needed |
| C+ | 65-69 | Average - significant gaps |
| C | 60-64 | Below Average - major issues |
| D | 50-59 | Poor - critical gaps |
| F | <50 | Failing - untested CLI |

## Best Practices Checklist

### Must Have (E2E Minimum)

- [ ] Every command has at least one test
- [ ] Every test checks `exit_code`
- [ ] Every test verifies output
- [ ] Error cases return non-zero exit codes

### Should Have (Good Coverage)

- [ ] All argument combinations tested
- [ ] All options/flags tested
- [ ] Interactive prompts have `input=`
- [ ] Edge cases covered

### Nice to Have (Excellent)

- [ ] Subcommands tested
- [ ] stderr checked separately
- [ ] Environment variables tested
- [ ] Exit code values verified

## Additional Resources

- Typer testing: https://typer.tiangolo.com/tutorial/testing/
- CliRunner docs: https://typer.tiangolo.com/api/typer/testing/
- For Python test quality, see [python-test-quality-skill](../python-test-quality-skill/SKILL.md)
- For general test principles, see [test-quality-skill](../test-quality-skill/SKILL.md)
