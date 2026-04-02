---
name: python-test-quality
description: Evaluate Python test quality with pytest. Use when reviewing tests, assessing test suites, or asked "how good are our Python tests?". Checks coverage, requirement traceability, meaningful assertions, and business value alignment. Generates markdown report to reports/tests/python-test-report-<date>. Supports --path, --report, --focus flags.
disable-model-invocation: true
allowed-tools: Read,Grep,Glob,Bash
---

# Python Test Quality Review Skill

Evaluate Python test quality with pytest beyond simple coverage metrics.

## Quick Usage

```bash
/python-test-quality
/python-test-quality --path=src
/python-test-quality --report
/python-test-quality --focus=coverage
```

## Report Output

Reports are generated to: `reports/tests/python-test-report-YYYY-MM-DD.md`

```bash
# Generate report with today's date
/python-test-quality --report

# Generate for specific path
/python-test-quality --path=src/features/auth --report

# Generate with specific focus
/python-test-quality --path=src --focus=assertions --report
```

The report filename uses the current system date (not training data):
- Format: `python-test-report-YYYY-MM-DD.md`
- Example: `python-test-report-2026-03-31.md`

## Overview

Test quality is not about coverage percentage. It's about:

1. **Coverage** - Are all code paths tested?
2. **Requirement Traceability** - Do tests verify what the code is supposed to do?
3. **Meaningful Assertions** - Do tests verify behavior, not just implementation?
4. **Business Value** - Do tests ensure the solution answers the real problem?

**A test with 100% coverage that tests the wrong things is worthless.**

## Python Testing with pytest

### Key Differences from JavaScript Testing

| Aspect | JavaScript/Vitest | Python/pytest |
|--------|-------------------|---------------|
| Assertions | `expect(x).toBe(y)` | `assert x == y` |
| Setup | `beforeEach()` | `@pytest.fixture` |
| Skip | `test.skip()` | `@pytest.mark.skip` |
| Parametrize | `test.each(data)()` | `@pytest.mark.parametrize` |
| Coverage | vitest --coverage | pytest-cov |

### pytest Fixtures

```python
# Bad - implicit fixture dependency
def test_user_login():
    db = Database()
    user = db.create_user(...)
    # ...

# Good - explicit fixtures
@pytest.fixture
def db():
    return Database()

def test_user_login(db):
    user = db.create_user(...)
    # ...

# Great - fixture with setup/teardown
@pytest.fixture
def temp_dir(tmp_path):
    dir = tmp_path / "test_data"
    dir.mkdir()
    yield dir
    # cleanup happens automatically
```

### pytest Parametrize

```python
# Bad - duplicate tests for each case
def test_addition_positive():
    assert add(1, 2) == 3

def test_addition_negative():
    assert add(-1, -2) == -3

# Good - parameterized test
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (-1, -2, -3),
    (0, 0, 0),
])
def test_addition(a, b, expected):
    assert add(a, b) == expected
```

## Test Quality Dimensions

### 1. Requirement Traceability (30%)

Measures how well tests map to actual requirements.

| Check | Weight | Description |
|-------|--------|-------------|
| Business rules covered | 10 | Each business rule has explicit tests |
| User stories verified | 8 | Critical user flows have tests |
| Edge cases justified | 7 | Edge cases exist for a reason |
| Happy path verified | 5 | Basic functionality works |

### 2. Assertion Quality (25%)

Measures whether assertions verify meaningful behavior.

| Check | Weight | Description |
|-------|--------|-------------|
| Meaningful assertions | 10 | Tests verify outcomes, not types |
| Specific values tested | 8 | Tests use realistic data |
| Error conditions verified | 7 | Failures are tested |

### 3. Coverage Depth (20%)

Measures whether critical paths are covered.

| Check | Weight | Description |
|-------|--------|-------------|
| Branch coverage | 8 | All paths are tested |
| Error paths covered | 7 | Exception paths have tests |
| Integration points | 5 | External calls are mocked/stubbed |

### 4. Test Isolation (15%)

Measures whether tests can run independently.

| Check | Weight | Description |
|-------|--------|-------------|
| No shared state | 6 | Tests don't affect each other |
| Deterministic | 5 | Same result every time |
| Order independent | 4 | Tests can run in any order |

### 5. Maintainability (10%)

Measures whether tests can evolve with code.

| Check | Weight | Description |
|-------|--------|-------------|
| Clear intent | 4 | Test purpose is obvious |
| Self-documenting | 3 | Name describes what/why |
| Minimal setup | 3 | No 50-line fixtures |

## The Test Quality Checklist

### Requirement Traceability

- [ ] Each business rule has at least one explicit test
- [ ] Critical user flows have end-to-end tests
- [ ] Edge cases are documented (why does this edge case exist?)
- [ ] Happy path is verified (does basic functionality work?)

### Assertion Quality

**Good assertions verify outcomes:**

```python
# Verifies what happens, not what type it is
assert order.total == 1080
assert user.is_active is True
assert payment.status == 'APPROVED'
```

**Bad assertions verify implementation:**

```python
# Only proves the code runs, not that it works
assert isinstance(result, int)
assert result is not None
assert len(result) > 0
```

### pytest-Specific Checks

**Good fixture usage:**

```python
# Proper fixture scope
@pytest.fixture(scope="module")
def db_connection():
    """Connection shared across module tests."""
    conn = create_connection()
    yield conn
    conn.close()

# Fixture with clear purpose
@pytest.fixture
def sample_user():
    """Returns a user dict for testing."""
    return {"id": 1, "name": "Test User", "email": "test@example.com"}
```

**Good marker usage:**

```python
# Skip with reason
@pytest.mark.skip(reason="waiting for API v2")
def test_api_v2_feature():
    pass

# Conditional skip
@pytest.mark.skipif(sys.version_info < (3, 11), reason="requires 3.11+")
def test_exception_notes():
    pass

# Mark for selective runs
@pytest.mark.integration
def test_full_pipeline():
    pass
```

### Coverage Questions

Ask these questions:

1. **What business rule does this line implement?**
2. **Is there a test that proves this rule works?**
3. **If this line is deleted, which test would fail?**

If you can't answer question 3, the line isn't really covered.

## Analyzing Test Quality

### Stage 1: Collect Coverage Data

```bash
# Get line and branch coverage
pytest --cov=src --cov-report=term-missing --cov-report=html

# Get coverage with branch analysis
pytest --cov=src --cov-branch --cov-report=term-missing

# Get detailed coverage report
pytest --cov=src --cov-report=term-missing --cov-report=json coverage.json
```

### Stage 2: Analyze Test Structure

```bash
# List all test files
find . -name "test_*.py" -o -name "*_test.py" | head -20

# Count test functions
grep -r "def test_" --include="*.py" | wc -l

# Find parametrized tests
grep -r "@pytest.mark.parametrize" --include="*.py" -l

# Find fixtures
grep -r "@pytest.fixture" --include="*.py" -l

# Find skipped tests
grep -r "@pytest.mark.skip" --include="*.py" -l
```

### Stage 3: Analyze Assertions

```bash
# Find all assert statements in tests
grep -rn "assert " tests/ --include="*.py" | head -50

# Find weak assertions (only checks type/existence)
grep -rn "isinstance\|type(\|is not None\|is None" tests/ --include="*.py"

# Find assertTrue/assertFalse (often too vague)
grep -rn "assertTrue\|assertFalse" tests/ --include="*.py"

# Find comparison assertions
grep -rn "assert.*==\|assert.*!=" tests/ --include="*.py"
```

### Stage 4: Check Isolation

```bash
# Find tests that modify global state
grep -rn "global \|monkeypatch\|mock" tests/ --include="*.py"

# Find database operations in tests
grep -rn "db\.\|session\.\|commit\|rollback" tests/ --include="*.py"

# Find file system operations
grep -rn "open(\|tmp_path\|Path(" tests/ --include="*.py"
```

### Stage 5: Check pytest Best Practices

```bash
# Check for proper fixture usage
grep -rn "@pytest.fixture" tests/ --include="*.py"

# Check for module-scoped fixtures (potential shared state)
grep -rn "@pytest.fixture(scope=\"module\")" tests/ --include="*.py"

# Check for proper conftest.py usage
ls tests/conftest.py 2>/dev/null && echo "conftest.py exists"
```

## Anti-Patterns

### The Type Checker Test

```python
# Bad - proves nothing about behavior
def test_calculate_total_returns_int():
    result = calculate_total([])
    assert isinstance(result, int)

# Good - verifies actual behavior
def test_calculate_total_with_discount():
    order = {"items": [{"price": 600, "quantity": 2}]}
    result = calculate_total(order)
    assert result == 1080  # 1200 - 10% discount
```

### The Happy Path Only Test

```python
# Bad - only tests the happy path
def test_divide_numbers():
    assert divide(10, 2) == 5

# Good - also tests error cases
@pytest.mark.parametrize("a,b,expected", [
    (10, 2, 5),
    (0, 5, 0),
    (-10, 2, -5),
])
def test_divide_numbers(a, b, expected):
    assert divide(a, b) == expected

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
```

### The No Assertions Test

```python
# Bad - no real verification
def test_process_data():
    process_data({"key": "value"})
    # Nothing asserted!

# Good - clear verification
def test_process_data():
    result = process_data({"key": "value"})
    assert result.status == "success"
    assert result.data == {"processed": True}
```

### The Brittle Test

```python
# Bad - tests implementation, not behavior
def test_sorts_list_in_place():
    original = [3, 1, 2]
    sorted_list = sort_in_place(original)
    assert sorted_list is original  # Brittle! Tests memory address

# Good - tests behavior
def test_sorts_list_correctly():
    result = sort_in_place([3, 1, 2])
    assert result == [1, 2, 3]
```

### The Overly Broad Fixture

```python
# Bad - massive fixture that sets up everything
@pytest.fixture
def app():
    db = setup_database()
    cache = setup_cache()
    queue = setup_queue()
    api = setup_api()
    user = create_user(db)
    # ... 50 lines of setup!
    yield app
    # ... 50 lines of teardown!

# Good - focused fixtures
@pytest.fixture
def db():
    return TestDatabase()

@pytest.fixture
def sample_user(db):
    return db.create_user(name="Test")
```

## Test Report Format

**Output:** `reports/tests/python-test-report-YYYY-MM-DD.md`

```markdown
# Python Test Quality Report

**Generated:** YYYY-MM-DD
**Path Analyzed:** /path/to/code
**Report Location:** reports/tests/python-test-report-YYYY-MM-DD.md

## Overall Score: 72/100 (Good)

| Dimension | Score | Weight | Weighted | Status |
|-----------|-------|--------|----------|--------|
| Requirement Traceability | 24/30 | 30% | 24.0 | Good |
| Assertion Quality | 18/25 | 25% | 18.0 | Warning |
| Coverage Depth | 14/20 | 20% | 14.0 | Good |
| Test Isolation | 12/15 | 15% | 12.0 | Good |
| Maintainability | 4/10 | 10% | 4.0 | Warning |

**Grade: C+ (Average)**

---

## Executive Summary

| Metric | Value | Status |
|--------|-------|--------|
| Test files | 23 | Good |
| Test functions | 156 | Good |
| Coverage | 78% | Good |
| Branch coverage | 65% | Warning |
| Parametrized tests | 12 | Good |
| Skipped tests | 8 | Acceptable |
| fixtures | 34 | Good |

---

## Coverage Analysis

### Overall Coverage

| Metric | Value | Status |
|-------|-------|--------|
| Line coverage | 78% | Good |
| Branch coverage | 65% | Warning |
| Function coverage | 85% | Good |

### Missing Coverage

| File | Missing Lines | Missing Branches |
|------|---------------|------------------|
| src/api/client.py | 23, 45, 67 | 24, 46 |
| src/services/parser.py | 12, 34 | None |
| src/utils/validation.py | 8, 9, 10 | 8, 11 |

---

## Requirement Traceability

### Business Rules with Tests

| Rule | Test File | Status |
|------|-----------|--------|
| 10% discount for orders > $1000 | test_order.py | Good |
| User must verify email | test_user.py | Good |
| API rate limit: 100/min | test_api.py | Missing |

### User Flows with Tests

| Flow | Test File | Status |
|------|-----------|--------|
| User registration | test_auth.py | Good |
| Order checkout | test_order.py | Good |
| Password reset | Missing | **Critical** |

---

## Assertion Quality Issues

### Weak Assertions Found

| File | Line | Issue | Suggestion |
|------|------|-------|------------|
| tests/unit/test_calc.py | 23 | `assert isinstance(r, int)` | Assert actual value |
| tests/api/test_user.py | 45 | `assert result is not None` | Check specific fields |
| tests/core/test_parser.py | 67 | `assert len(items) > 0` | Verify item contents |

### Tests Without Assertions

| File | Line | Issue |
|------|------|-------|
| tests/integration/test_api.py | 34 | No assertions |
| tests/unit/test_utils.py | 56 | Empty test |

---

## Fixture Analysis

### Well-Designed Fixtures

| Fixture | Scope | Purpose |
|---------|-------|---------|
| `db` | function | Test database |
| `sample_user` | function | User fixture |
| `temp_dir` | function | Temp directory |

### Shared State Risks

| Fixture | Scope | File | Risk |
|---------|-------|------|------|
| `db_connection` | module | conftest.py | Shared across tests |
| `app_config` | module | conftest.py | May leak state |

---

## pytest Best Practices

### Proper Practices Found

- Parametrized tests used for data-driven cases
- Fixtures with clear, single purposes
- Proper use of `pytest.raises` for exceptions
- Descriptive test names with `test_` prefix

### Issues Found

| Issue | Count | Files |
|-------|-------|-------|
| Bare `assert` without message | 12 | test_calc.py, test_user.py |
| Overly broad fixtures | 3 | conftest.py |
| Missing `@pytest.mark.parametrize` | 5 | test_order.py |

---

## Recommendations

### Critical Priority

1. **Add password reset tests**
   - Currently no coverage for password reset flow
   - Critical for security

2. **Fix 3 tests without assertions**
   - tests/integration/test_api.py:34
   - tests/unit/test_utils.py:56
   - tests/core/test_parser.py:89

3. **Replace weak assertions**
   - 12 assertions only check type/existence
   - Should verify actual behavior

### Medium Priority

4. **Increase branch coverage**
   - Current: 65%
   - Target: 80%

5. **Add more parametrized tests**
   - Reduce duplicate test code
   - Increase test data variety

6. **Document fixture responsibilities**
   - Some fixtures do too much
   - Split into focused units

---

## GitHub Issue Draft

```markdown
## Improve Python test quality

### Problem

Test coverage is 78% but assertion quality is poor:
- 12 tests only check types, not behavior
- 3 tests have no assertions
- Password reset flow has no tests

### Impact

- High coverage but low confidence
- Bugs can slip through
- Critical flows untested

### Current State

- Line coverage: 78%
- Branch coverage: 65%
- Assertion quality: Warning
- Requirement traceability: Good

### Proposed Changes

1. Replace 12 weak assertions with behavior checks
2. Add assertions to 3 empty tests
3. Create password reset test coverage
4. Increase branch coverage to 80%

### Effort

~4 hours across 8 files
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
| Requirement Traceability | 30% | 30 |
| Assertion Quality | 25% | 25 |
| Coverage Depth | 20% | 20 |
| Test Isolation | 15% | 15 |
| Maintainability | 10% | 10 |
| **Total** | **100%** | **100** |

### Grade Scale

| Grade | Score | Interpretation |
|-------|-------|----------------|
| A+ | 95-100 | Exceptional - comprehensive tests |
| A | 90-94 | Excellent - minimal gaps |
| A- | 85-89 | Very Good - minor improvements |
| B+ | 80-84 | Good - solid foundation |
| B | 75-79 | Good - some gaps |
| B- | 70-74 | Acceptable - improvements needed |
| C+ | 65-69 | Average - significant gaps |
| C | 60-64 | Below Average - major issues |
| D | 50-59 | Poor - critical gaps |
| F | <50 | Failing - tests don't verify behavior |

## pytest Commands Reference

### Coverage

```bash
# Run with coverage
pytest --cov=src --cov-report=term-missing

# HTML report
pytest --cov=src --cov-report=html

# Fail if coverage drops
pytest --cov=src --cov-fail-min=80

# Branch coverage
pytest --cov=src --cov-branch
```

### Selective Runs

```bash
# Run only tests with specific marker
pytest -m "not integration"

# Run tests matching pattern
pytest -k "test_user"

# Run specific file
pytest tests/test_user.py
```

### Debugging

```bash
# Stop on first failure
pytest -x

# Show local variables
pytest -l

# Capture output
pytest -s
```

## Additional Resources

- pytest documentation: https://docs.pytest.org/
- pytest-cov: https://pytest-cov.readthedocs.io/
- For exception handling, see [python-exception-skill](../python-exception-skill/SKILL.md)
- For general test quality principles, see [test-quality-skill](../test-quality-skill/SKILL.md)
