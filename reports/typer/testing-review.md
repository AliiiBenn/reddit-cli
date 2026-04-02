# Testing Review

## Overview

This review analyzes test coverage, test quality, testing patterns, and identifies gaps in the test suite.

---

## Test Suite Structure

```
tests/
├── conftest.py              # Shared fixtures
├── test_cli_browse.py       # Browse command tests
├── test_cli_comments.py     # Comments command tests
├── test_cli_errors.py       # Error handling tests
├── test_cli_navigation.py   # Frontpage/home/best tests
├── test_cli_ping.py         # Ping and help tests
├── test_cli_post.py         # Post command tests
├── test_cli_search.py       # Search command tests
├── test_cli_subreddit.py    # Subreddit commands tests
└── test_models.py           # Pydantic model unit tests
```

---

## Test Coverage Analysis

### Files with Tests

| File | Tests | Coverage Focus |
|------|-------|----------------|
| test_cli_browse.py | 21 tests | Browse, sticky, random, search, pagination |
| test_cli_comments.py | 14 tests | Comments, single comment, replies |
| test_cli_errors.py | 17 tests | HTTP errors (404, 500, 429, 403) |
| test_cli_navigation.py | 13 tests | Frontpage, home, best, pagination |
| test_cli_ping.py | 6 tests | Ping, help commands |
| test_cli_post.py | 10 tests | Post view, info, duplicates |
| test_cli_search.py | 11 tests | Global search |
| test_cli_subreddit.py | 22 tests | Subreddit info, list, search, new, gold, default |
| test_models.py | 10 tests | Pydantic model validation |

**Total:** ~124 tests

---

## Test Quality Assessment

### Strengths

1. **Good Use of Fixtures** - `conftest.py` provides reusable fixtures
2. **respx Mocking** - Proper HTTP mocking with respx
3. **Parametrized Tests** - Good use of `@pytest.mark.parametrize`
4. **Isolation** - Tests don't depend on each other

### Weaknesses

1. **Shallow Assertions** - Most tests only check exit_code == 0
2. **No Verification of API Calls** - Don't verify correct parameters passed
3. **No Negative Testing** - Limited tests for invalid inputs

---

## Common Test Pattern

```python
def test_browse_exit_code(self, runner, mock_reddit_base, sample_browse_response):
    mock_reddit_base.get("/r/python/hot.json").mock(
        return_value=httpx.Response(200, json=sample_browse_response)
    )
    result = runner.invoke(app, ["browse", "python"])
    assert result.exit_code == 0
```

**Issues with this pattern:**
1. Only verifies the command doesn't crash
2. Doesn't verify correct API endpoint was called
3. Doesn't verify correct query parameters were passed
4. Output assertions are rare

---

## Missing Test Coverage

### 1. No Tests for Option Validation

```python
# What happens with invalid sort value?
result = runner.invoke(app, ["browse", "python", "--sort", "invalid_sort"])
# Currently: passes to API, API returns 400
```

No tests verify user gets helpful error message.

### 2. No Tests for Limit Bounds

```python
# What happens with limit > 100?
result = runner.invoke(app, ["browse", "python", "--limit", "500"])
```

### 3. No Tests for Mutually Exclusive Options

```python
# What happens with --sticky AND --random?
result = runner.invoke(app, ["browse", "python", "--sticky", "--random"])
```

Currently both are accepted (but one takes precedence).

### 4. No Tests for Rate Limit Handling (429)

`test_cli_errors.py` has a test for 429, but only checks exit code. No tests verify:
- Error message content
- Retry behavior (if implemented)
- Backoff timing

### 5. No Tests for Network Timeouts

Tests use respx which don't simulate slow responses.

### 6. No Tests for Malformed JSON Response

What happens if Reddit returns malformed JSON?

### 7. No Tests for Empty Subreddit Name

```python
result = runner.invoke(app, ["browse", ""])
```

### 8. No Tests for Special Characters in Search

```python
result = runner.invoke(app, ["search", "python <script>"])
```

### 9. No Tests for Concurrent Invocations

Single-user CLI, but could be tested.

---

## Fixtures Analysis

### conftest.py Fixtures

| Fixture | Purpose | Quality |
|---------|---------|---------|
| runner | CliRunner instance | Good |
| mock_reddit_base | respx mock setup | Good |
| sample_post_json | Single post data | Good |
| sample_posts_response | Listing response | Good |
| sample_comment_json | Single comment data | Good |
| sample_subreddit_json | Subreddit data | Good |
| sample_navigation_response | Frontpage response | Good |
| sample_search_response | Search results | Good |
| empty_posts_response | Empty listing | Good |
| error_response_404/500/403/429 | HTTP error responses | Good |

**Issues:**
1. Error response fixtures return raw httpx.Response, not JSON-decoded error bodies
2. No fixture for network connect errors (respx has different mocking for this)

---

## Test Patterns That Need Improvement

### 1. No assert on result.output

Many tests don't verify the actual output:

```python
# Only checks exit code
assert result.exit_code == 0

# Should also verify output contains expected content
assert "Python Tip of the Day" in result.output
```

### 2. No assert on API call parameters

Tests mock the endpoint but don't verify what parameters were sent:

```python
# This test passes even if --limit 10 is ignored
mock_reddit_base.get("/r/python/hot.json").mock(
    return_value=httpx.Response(200, json=sample_browse_response)
)
result = runner.invoke(app, ["browse", "python", "--limit", "10"])
assert result.exit_code == 0  # passes regardless of limit
```

### 3. Exception Testing with catch_exceptions

```python
# Default: catch_exceptions=True
result = runner.invoke(app, ["browse", "nonexistent"])
assert result.exit_code != 0
```

But tests never verify `result.exception` is None or inspect it for debugging.

---

## Integration vs Unit Testing

**Current State:** All tests are unit tests with mocks.

**Missing:** Integration tests that hit real Reddit API.

**Recommendation:** Add a `tests/integration/` folder with optional integration tests that require network access and potentially rate-limit.

---

## Test Execution

### Current CI/CD

GitHub Actions workflow (test.yml):
- Runs on: push to main, pull requests
- Steps: checkout, install uv, install Python 3.14, sync deps, run pytest

**Missing:**
- Coverage reporting to codecov or similar
- Parallel test execution
- Test timing/flaky detection

---

## Test Coverage Report

Based on code analysis, estimated coverage:

| Module | Coverage |
|--------|----------|
| reddit_cli/__init__.py | HIGH (most commands tested) |
| reddit_cli/commands/browse.py | HIGH |
| reddit_cli/commands/comments.py | HIGH |
| reddit_cli/commands/post.py | MEDIUM (missing --view, --info tests) |
| reddit_cli/commands/search.py | HIGH |
| reddit_cli/commands/navigation.py | HIGH |
| reddit_cli/commands/subreddit.py | HIGH |
| reddit_cli/reddit/base.py | LOW (only through integration) |
| reddit_cli/reddit/posts.py | MEDIUM |
| reddit_cli/reddit/comments.py | MEDIUM |
| reddit_cli/reddit/subreddits.py | MEDIUM |
| reddit_cli/reddit/models.py | HIGH (dedicated tests) |

**Estimated Overall:** 85-90%

---

## Recommendations

1. **HIGH PRIORITY:** Add output content assertions to all tests
2. **MEDIUM PRIORITY:** Add API parameter verification tests
3. **MEDIUM PRIORITY:** Add tests for invalid option values
4. **MEDIUM PRIORITY:** Add tests for edge cases (empty results, special chars)
5. **LOW PRIORITY:** Consider adding integration tests
6. **LOW PRIORITY:** Add coverage reporting to CI

---

*Report generated for project: better-reddit-cli v0.4.4*
