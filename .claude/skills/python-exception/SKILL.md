---
name: python-exception
description: Analyze Python exception handling patterns. Use when evaluating exception handling quality, auditing error management, or asked "how are exceptions handled in this project?". Checks exception classes, chaining, groups, notes, and cleanup patterns. Generates markdown report to reports/exceptions/exception-report-<date>. Supports --path, --report, --focus flags.
disable-model-invocation: true
allowed-tools: Read,Grep,Glob,Bash
---

# Python Exception Handling Analysis Skill

Analyze Python exception handling patterns and report on advanced features usage.

## Quick Usage

```bash
/python-exception
/python-exception --path=src
/python-exception --report
/python-exception --focus=chaining
```

## Report Output

Reports are generated to: `reports/exceptions/exception-report-YYYY-MM-DD.md`

```bash
# Generate report for current directory
/python-exception --report

# Analyze specific path
/python-exception --path=src/api --report

# Focus on exception chaining
/python-exception --path=src --focus=chaining --report
```

## Overview

Python exception handling has evolved significantly. This skill analyzes how well a project uses modern Python exception features.

**Why Exception Handling Matters:**

| Poor Exception Handling | Good Exception Handling |
|------------------------|------------------------|
| Generic except clauses catch everything | Specific exception types caught |
| No context on why failures occurred | add_note() provides context |
| Swallowed exceptions hide problems | Exception chaining preserves trace |
| Resource leaks from unclosed handles | Context managers ensure cleanup |
| Single exceptions lose parallel errors | ExceptionGroup captures all failures |

## Advanced Features Checklist

### Exception Chaining (Python 3)

```python
# Bad - loses original exception context
try:
    risky_operation()
except SomeError:
    raise OtherError("failed")  # Original trace lost

# Good - preserves cause with 'from'
try:
    risky_operation()
except SomeError as exc:
    raise OtherError("failed") from exc  # Shows both traces

# Explicit suppression when needed
raise RuntimeError("msg") from None  # Hides implementation detail
```

### Exception Groups (Python 3.11+)

```python
# Bad - only catches first error
for task in tasks:
    task.run()  # Stops at first failure

# Good - collects all failures
excs = []
for task in tasks:
    try:
        task.run()
    except Exception as e:
        excs.append(e)

if excs:
    raise ExceptionGroup("task failures", excs)

# Selective handling with except*
try:
    run_all_tasks()
except* OSError as e:
    print(f"OS errors: {e.exceptions}")
except* ValueError as e:
    print(f"Value errors: {e.exceptions}")
```

### Exception Notes (Python 3.11+)

```python
# Bad - no context about where/why
raise ValidationError("invalid")

# Good - adds provenance with add_note
try:
    validate(data)
except ValidationError as e:
    e.add_note(f"Input: {data}")
    e.add_note(f"Timestamp: {datetime.now()}")
    raise

# Useful in loops for iteration context
for item in items:
    try:
        process(item)
    except Exception as e:
        e.add_note(f"Processing item: {item.id}")
        excs.append(e)
```

### Context Managers for Cleanup

```python
# Bad - finally required, easy to forget
f = None
try:
    f = open(file)
    data = f.read()
finally:
    if f:
        f.close()

# Good - automatic cleanup with 'with'
with open(file) as f:
    data = f.read()

# Bad - nested finally for multiple resources
try:
    conn = get_connection()
finally:
    try:
        conn.close()
    finally:
        if f:
            f.close()

# Good - separate context managers
with get_connection() as conn, open(file) as f:
    data = f.read()
```

### User-Defined Exceptions

```python
# Bad - string-based error
raise Exception("something went wrong")

# Good - structured exception with attributes
class ProcessingError(Exception):
    def __init__(self, message, operation, item_id=None):
        super().__init__(message)
        self.operation = operation
        self.item_id = item_id

raise ProcessingError("failed", operation="validate", item_id=123)

# Better - uses add_note for context
class PipelineError(Exception):
    def __init__(self, message, **kwargs):
        super().__init__(message)
        self.context = kwargs

# Best - rich exception with notes
class APIError(Exception):
    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        if status_code:
            self.add_note(f"Status: {status_code}")
        if response:
            self.add_note(f"Response: {response[:200]}")
```

## Analysis Dimensions

### 1. Exception Class Design (25%)

Measures quality of custom exception definitions.

| Check | Weight | Description |
|-------|--------|-------------|
| Inherits from Exception | 8 | Proper exception hierarchy |
| Descriptive class name | 5 | Ends with Error suffix |
| Meaningful attributes | 7 | Stores relevant context |
| __str__ override | 5 | Clean error messages |

### 2. Exception Chaining (20%)

Measures proper use of `raise ... from`.

| Check | Weight | Description |
|-------|--------|-------------|
| Preserves cause | 8 | Uses `from exc` properly |
| Suppresses when needed | 6 | Uses `from None` appropriately |
| No silent exception loss | 6 | No bare except that swallow |

### 3. Exception Groups (15%)

Measures parallel error collection.

| Check | Weight | Description |
|-------|--------|-------------|
| Collects multiple errors | 6 | Uses ExceptionGroup when appropriate |
| except* selective handling | 5 | Handles subgroups correctly |
| Proper exception instances | 4 | Exceptions not types in groups |

### 4. Exception Notes (15%)

Measures contextual annotation.

| Check | Weight | Description |
|-------|--------|-------------|
| add_note() usage | 8 | Adds context to exceptions |
| Meaningful notes | 4 | Notes provide useful info |
| Note placement | 3 | Notes added before raise |

### 5. Cleanup Patterns (15%)

Measures resource management.

| Check | Weight | Description |
|-------|--------|-------------|
| Context managers used | 8 | with statement for resources |
| finally when needed | 4 | For non-context-manager cleanup |
| No empty except | 3 | All catches handle or re-raise |

### 6. Specificity (10%)

Measures exception handler precision.

| Check | Weight | Description |
|-------|--------|-------------|
| Specific exception types | 5 | No bare except Exception |
| Exception tuples | 3 | Multiple types per handler |
| Proper exception hierarchy | 2 | Catches parent classes correctly |

## Anti-Patterns

### Bare except Clause

```python
# Bad - catches everything including KeyboardInterrupt
try:
    do_something()
except:
    pass

# Good - catches specific types
try:
    do_something()
except ValueError:
    pass

# Acceptable when re-raising
try:
    do_something()
except Exception:
    logger.error("failed")
    raise
```

### Swallowed Exceptions

```python
# Bad - exception disappears
try:
    risky()
except SomeError:
    pass  # Silent failure!

# Good - log and re-raise
try:
    risky()
except SomeError:
    logger.warning("handled gracefully")
    raise

# Good - convert with context
try:
    risky()
except SomeError as exc:
    raise CustomError("operation failed") from exc
```

### Resource Leaks

```python
# Bad - file never closed on exception
f = open(file)
data = f.read()
f.close()

# Good - context manager handles all cases
with open(file) as f:
    data = f.read()

# Bad - complex nested cleanup
conn = None
f = None
try:
    conn = get_conn()
    f = open_file()
finally:
    if f:
        f.close()
    if conn:
        conn.close()

# Good - each resource in own context
with get_conn() as conn, open_file() as f:
    data = f.read()
```

### Catching Too Broad

```python
# Bad - catches everything
try:
    int(user_input)
except Exception:  # Too broad!
    print("invalid")

# Good - catch what's expected
try:
    int(user_input)
except ValueError:  # Only what can fail
    print("invalid")

# Acceptable - catching multiple specific types
try:
    risky()
except (ValueError, TypeError) as e:
    handle(e)
```

### Lost Exception Context

```python
# Bad - original trace lost
try:
    do_something()
except Error as e:
    raise NewError("failed")  # No context!

# Good - chaining preserves history
try:
    do_something()
except Error as e:
    raise NewError("failed") from e

# Good - explicit suppression
try:
    do_something()
except SensitiveError:
    raise PublicError("operation failed") from None
```

## Analyzing Exception Handling

### Stage 1: Find Exception Classes

```bash
# Find custom exception definitions
grep -rn "class.*Exception" --include="*.py" | grep -v "ExceptionGroup"

# Find exception class hierarchies
grep -rn "class.*Error" --include="*.py"

# Find exception imports
grep -rn "from.*import.*Exception" --include="*.py"
```

### Stage 2: Analyze Exception Raising

```bash
# Find raise statements
grep -rn "raise" --include="*.py"

# Find exception chaining
grep -rn "raise.*from" --include="*.py"
grep -rn "raise.*from None" --include="*.py"

# Find add_note usage (Python 3.11+)
grep -rn "add_note" --include="*.py"

# Find ExceptionGroup usage
grep -rn "ExceptionGroup" --include="*.py"
grep -rn "except\*" --include="*.py"
```

### Stage 3: Analyze Exception Catching

```bash
# Find except clauses
grep -rn "except" --include="*.py"

# Find bare except (bad!)
grep -rn "except:" --include="*.py"

# Find specific exception patterns
grep -rn "except.*as" --include="*.py"

# Count except clauses per function
```

### Stage 4: Analyze Cleanup

```bash
# Find context managers
grep -rn "with " --include="*.py"

# Find finally clauses
grep -rn "finally:" --include="*.py"

# Check for resource leaks (files without context manager)
grep -rn "open(" --include="*.py" | grep -v "with open"
```

## Exception Report Format

**Output:** `reports/exceptions/exception-report-YYYY-MM-DD.md`

```markdown
# Python Exception Handling Report

**Generated:** YYYY-MM-DD
**Path Analyzed:** /path/to/code
**Report Location:** reports/exceptions/exception-report-YYYY-MM-DD.md

## Overall Score: 72/100 (Good)

| Dimension | Score | Weight | Weighted | Status |
|-----------|-------|--------|----------|--------|
| Exception Class Design | 22/25 | 25% | 22.0 | Good |
| Exception Chaining | 14/20 | 20% | 14.0 | Warning |
| Exception Groups | 8/15 | 15% | 8.0 | Warning |
| Exception Notes | 6/15 | 15% | 6.0 | Critical |
| Cleanup Patterns | 12/15 | 15% | 12.0 | Good |
| Specificity | 6/10 | 10% | 6.0 | Warning |

**Grade: C+ (Average)**

---

## Executive Summary

| Metric | Value | Status |
|--------|-------|--------|
| Custom exception classes | 12 | Good |
| Properly chained exceptions | 8/15 (53%) | Warning |
| Uses ExceptionGroup | 2 | Needs Implementation |
| Uses add_note() | 3 | Critical |
| Context managers used | 45 | Good |
| Bare except clauses | 4 | **Critical** |
| Swallowed exceptions | 7 | Warning |

---

## Exception Class Analysis

### Well-Designed Exceptions

| Class | File | Inherits | Attributes | Status |
|-------|------|----------|-------------|--------|
| ValidationError | errors.py | Exception | field, reason | Good |
| APIError | api.py | Exception | status_code, url | Good |
| ProcessingError | pipeline.py | Exception | operation, item_id | Good |

### Issues Found

| Class | File | Issue |
|-------|------|-------|
| GenericError | utils.py | Too generic name |
| XError | legacy.py | Poor naming |
| CustomError | old.py | No attributes |

### Missing Base Classes

| Class | Should Inherit |
|-------|----------------|
| HTTPError | APIError or Exception |
| ConfigError | Exception |

---

## Exception Chaining Analysis

### Proper Chaining

| File | Line | Pattern |
|------|------|---------|
| api/client.py | 45 | `raise APIError from exc` |
| services/parser.py | 78 | `raise ParseError from e` |
| core/validate.py | 112 | `raise ValidationError from err` |

### Missing Chaining

| File | Line | Issue |
|------|------|-------|
| api/client.py | 89 | `raise ClientError` - no from |
| services/parser.py | 145 | `raise ParseError` - loses context |
| utils/convert.py | 67 | Original exception ignored |

### Suppression with from None

| File | Line | Context |
|------|------|---------|
| auth/oauth.py | 34 | Internal error hidden appropriately |
| config/loader.py | 56 | Implementation detail suppressed |

---

## Exception Groups Analysis

### ExceptionGroup Usage

```python
# Found in: workers/pool.py
raise ExceptionGroup("task failures", excs)
```

### Missing Parallel Error Collection

| File | Function | Issue |
|------|----------|-------|
| workers/batch.py | process_all() | Stops at first error |
| api/webhook.py | handle_events() | Should collect failures |
| tests/runner.py | run_suite() | Only reports first failure |

### except* Usage

**Status:** Not found - Python 3.11+ feature not used

---

## Exception Notes Analysis

### add_note() Usage Found

| File | Line | Note Content |
|------|------|--------------|
| api/client.py | 67 | "Request URL: {url}" |
| pipeline/validate.py | 89 | "Field: {field}" |
| workers/task.py | 34 | "Task ID: {id}" |

### Missing add_note()

| File | Function | Recommendation |
|------|----------|----------------|
| auth/login.py | authenticate() | Add note with user context |
| api/request.py | fetch() | Add note with URL and method |
| db/transaction.py | commit() | Add note with transaction ID |

---

## Cleanup Pattern Analysis

### Good Context Manager Usage

```python
# File: api/client.py
with get_session() as session:
    result = session.query()

# File: config/loader.py
with open(path) as f:
    data = yaml.safe_load(f)
```

### Resource Leak Risks

| File | Line | Issue |
|------|------|-------|
| legacy/parser.py | 23 | open() without context manager |
| old/api.py | 67 | Connection without context manager |
| tests/mocks.py | 45 | File handle possibly leaked |

### finally Usage

| File | Function | Purpose |
|------|----------|---------|
| core/worker.py | run() | Ensures flag reset |
| api/client.py | connect() | Connection cleanup |
| db/pool.py | acquire() | Return to pool |

---

## Anti-Patterns Found

### Bare except Clauses

| File | Line | Risk |
|------|------|------|
| utils/helpers.py | 34 | Catches KeyboardInterrupt |
| old/parser.py | 89 | Too broad |
| legacy/api.py | 123 | Silent failure likely |

### Swallowed Exceptions

| File | Line | Issue |
|------|------|-------|
| services/notify.py | 56 | except with pass |
| workers/task.py | 78 | Exception disappears |
| api/webhook.py | 145 | Errors silently ignored |

### Overly Broad Catching

| File | Line | Caught | Should Catch |
|-------|------|--------|--------------|
| api/client.py | 67 | Exception | (ValueError, TypeError) |
| utils/parse.py | 34 | BaseException | Exception |
| legacy/handler.py | 89 | Exception | Specific types |

---

## Recommendations

### Critical Priority

1. **Remove 4 bare except clauses**
   - Files: utils/helpers.py, old/parser.py, legacy/api.py, tests/mocks.py
   - Replace with specific exception types

2. **Add exception chaining to 8 locations**
   - Use `raise NewError() from original`
   - Preserves debugging context

3. **Implement add_note() in 5 functions**
   - Add context: request IDs, user info, timestamps

### Medium Priority

4. **Replace open() with context manager**
   - File: legacy/parser.py
   - Prevents file descriptor leaks

5. **Add ExceptionGroup for parallel operations**
   - Files: workers/batch.py, api/webhook.py
   - Collect all errors, report together

6. **Rename poorly named exceptions**
   - XError, GenericError, CustomError need better names

### Low Priority

7. **Add except* handling for ExceptionGroup**
   - When upgrading to Python 3.11+

8. **Document exception hierarchy**
   - Create doc explaining when to use which exception

---

## GitHub Issue Drafts

### Issue: Remove bare except clauses

```markdown
## Remove bare except clauses

### Problem

4 bare `except:` clauses found that catch everything including
KeyboardInterrupt and SystemExit. This can hide critical issues.

### Impact

- Errors may be silently swallowed
- Keyboard interrupt doesn't work properly
- Debugging becomes impossible

### Locations

- utils/helpers.py:34
- old/parser.py:89
- legacy/api.py:123
- tests/mocks.py:45

### Proposed Changes

Replace each bare except with specific exception types.

### Effort

~30 minutes
```

---

### Issue: Add exception chaining

```markdown
## Add exception chaining for better debugging

### Problem

8 locations raise new exceptions without chaining from the original.
This loses valuable stack trace context.

### Impact

- Debugging requires manual tracing
- Root cause obscured
- Longer investigation times

### Locations

- api/client.py:89
- services/parser.py:145
- utils/convert.py:67
- (5 more)

### Proposed Changes

Change `raise NewError()` to `raise NewError() from exc`

### Effort

~1 hour
```

---

## Confirmation

**This skill will NOT modify any code.** It only analyzes and reports findings.

**This skill will NOT create issues without your confirmation.**

**This skill will NOT write any files without your confirmation.**

---

## Scoring System

### Score Calculation

| Dimension | Weight | Max Score |
|-----------|--------|-----------|
| Exception Class Design | 25% | 25 |
| Exception Chaining | 20% | 20 |
| Exception Groups | 15% | 15 |
| Exception Notes | 15% | 15 |
| Cleanup Patterns | 15% | 15 |
| Specificity | 10% | 10 |
| **Total** | **100%** | **100** |

### Grade Scale

| Grade | Score | Interpretation |
|-------|-------|----------------|
| A+ | 95-100 | Exceptional - modern Python patterns |
| A | 90-94 | Excellent - minimal improvements |
| A- | 85-89 | Very Good - minor gaps |
| B+ | 80-84 | Good - solid foundation |
| B | 75-79 | Good - some gaps |
| B- | 70-74 | Acceptable - improvements needed |
| C+ | 65-69 | Average - significant gaps |
| C | 60-64 | Below Average - major issues |
| D | 50-59 | Poor - critical gaps |
| F | <50 | Failing - exception handling broken |

## Best Practices Summary

### Do

- Inherit custom exceptions from Exception
- Use specific exception types in except clauses
- Chain exceptions with `raise ... from exc`
- Use add_note() for context (Python 3.11+)
- Use ExceptionGroup for parallel operations
- Use context managers for resource cleanup
- Log exceptions before re-raising

### Do Not

- Use bare except clauses
- Swallow exceptions silently
- Catch Exception when more specific exists
- Lose exception context with bare raise
- Open files without context managers

## Additional Resources

- Python docs: [Exceptions](https://docs.python.org/3/library/exceptions.html)
- PEP 654: [Exception Groups](https://peps.python.org/pep-0654/)
- PEP 678: [add_note()](https://peps.python.org/pep-0678/)
- For error handling patterns, see [simplify-code-skill](../simplify-code-skill/SKILL.md)
