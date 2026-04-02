# Error Handling Review

## Current Error Handling Approach

### Pattern Used Across Commands

Each command file implements the same pattern:

```python
# commands/browse.py (lines 11-21)
def _handle_api_error(e: Exception) -> None:
    """Print a user-friendly error message for API errors and exit with code 1."""
    if isinstance(e, httpx.TimeoutException):
        print("Error: Connection timed out...", file=sys.stderr)
    elif isinstance(e, httpx.ConnectError):
        print("Error: Could not connect to Reddit...", file=sys.stderr)
    elif isinstance(e, httpx.HTTPStatusError):
        print(f"Error: Reddit API returned status {e.response.status_code}...", file=sys.stderr)
    else:
        print(f"Error: {e}", file=sys.stderr)
    raise typer.Exit(1)
```

**Duplicated in:**
- `commands/browse.py`
- `commands/comments.py`
- `commands/post.py`
- `commands/search.py`
- `commands/navigation.py`
- `commands/subreddit.py` (same pattern)

---

## Issues Identified

### 1. Code Duplication (HIGH)

The same 12-line function is copy-pasted 5 times. Any change to error handling requires updating all 5 files.

### 2. All Errors Exit with Code 1 (MEDIUM)

Typer/Click exit code conventions:

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success |
| 1 | General error / Abort |
| 2 | Usage error (invalid arguments) |
| 130 | Interrupted (Ctrl+C) |

**Current behavior:** All errors exit with code 1, regardless of severity.

**Example issues:**
- Invalid `--sort` value should exit with code 2 (usage error)
- Network timeout should exit with code 1 (general error)
- Reddit API 429 (rate limit) should exit with code 1 but with specific message

### 3. Bare `except Exception` Catches TyperExit (MEDIUM)

```python
# commands/browse.py:66-69
try:
    asyncio.run(_comments_async(post_id, sort, depth))
except Exception as e:
    _handle_api_error(e)
```

**Problem:** This catches `typer.Exit` and re-raises it with code 1, losing the original exit code if it was set differently.

### 4. HTTPStatusError Handling is Generic (LOW)

```python
elif isinstance(e, httpx.HTTPStatusError):
    print(f"Error: Reddit API returned status {e.response.status_code}. Please try again later.")
```

All HTTP errors show the same message. Could differentiate:
- 400 Bad Request (invalid input)
- 401/403 Forbidden (auth issues - not applicable here)
- 404 Not Found (subreddit/post doesn't exist)
- 429 Too Many Requests (rate limited)
- 500/502/503 Server Error (Reddit's problem)

### 5. No Retry Logic (MEDIUM)

Reddit's API is known for rate limiting. The current implementation makes no attempt to retry failed requests with backoff.

### 6. Timeout Configuration (LOW)

```python
# reddit/base.py
TIMEOUT = 10.0  # seconds
```

The timeout is hardcoded and not configurable via CLI options.

---

## Exception Handling in RedditClient

```python
# reddit/base.py:24-30
async def get(self, path: str, params: dict | None = None) -> dict:
    """Make a GET request to the Reddit API."""
    if not self._client:
        raise RuntimeError("Client not initialized. Use async context manager.")
    response = await self._client.get(path, params=params)
    response.raise_for_status()
    return response.json()
```

**Issues:**
1. `raise_for_status()` raises `httpx.HTTPStatusError` for non-2xx responses
2. No handling for `httpx.TimeoutException` or `httpx.ConnectError` at the client level
3. JSON parsing errors will raise `json.JSONDecodeError` with no user-friendly message

---

## Pydantic Validation Errors

**Unhandled:** If Reddit API returns unexpected data structure, Pydantic validation will fail with `ValidationError`. This is caught by the generic exception handler but the message won't be user-friendly.

---

## Typer.Abort vs Typer.Exit

The codebase uses `typer.Exit(1)` exclusively. `typer.Abort()` is not used.

| Method | Behavior |
|--------|----------|
| `typer.Exit(1)` | Exits with code 1, prints nothing by default |
| `typer.Abort()` | Exits with code 1, prints "Aborted!" |

Current usage is correct - no unnecessary Abort messages.

---

## Error Output Destinations

```python
print("Error: ...", file=sys.stderr)
```

All error messages go to stderr. This is correct behavior.

---

## Summary

| Aspect | Finding | Severity |
|--------|---------|----------|
| Error handler duplication | 5 copies of same function | HIGH |
| Exit code semantics | All errors = exit 1 | MEDIUM |
| Exception catching | Bare except may mask issues | MEDIUM |
| HTTP error differentiation | Generic message for all 4xx/5xx | LOW |
| Retry/backoff | No retry logic | MEDIUM |
| Timeout config | Hardcoded, not configurable | LOW |

---

## Recommendations

1. **Extract shared error handler** to `reddit_cli/errors.py`:
   ```python
   def handle_api_error(e: Exception) -> None:
       # Centralized error handling
   ```

2. **Implement semantic exit codes**:
   - Exit 1: General errors (network, API errors)
   - Exit 2: Usage errors (invalid arguments)
   - Exit 130: User interrupted (Ctrl+C)

3. **Add retry logic** with exponential backoff for transient errors

4. **Differentiate HTTP status codes** in error messages

5. **Handle Pydantic ValidationError** separately with user-friendly message

---

*Report generated for project: better-reddit-cli v0.4.4*
