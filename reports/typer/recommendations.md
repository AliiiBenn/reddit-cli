# Recommendations

## Prioritized Action Items

This document lists all recommendations in priority order based on impact and effort.

---

## CRITICAL Priority

### 1. Fix Unused Options in post Command

**Issue:** --view and --info options are defined but never checked.

**Location:** reddit_cli/commands/post.py:66-86

**Fix:** Either implement the options or remove them.

```python
@app.command(name="post")
def post(
    post_id: str,
    view: bool = False,
    info: bool = False,
    duplicates: bool = False,
) -> None:
    if view or info:
        asyncio.run(_post_async(post_id))
    elif duplicates:
        asyncio.run(_duplicates_async(post_id))
    else:
        asyncio.run(_post_async(post_id))
```

---

### 2. Remove Unused Typer Instances

**Issue:** 5 command files create app = typer.Typer() that is never used.

**Location:** browse.py, comments.py, post.py, search.py, navigation.py

**Fix:** Delete the unused app = typer.Typer() lines.

---

## HIGH Priority

### 3. Extract Shared Error Handler

**Issue:** _handle_api_error() duplicated across 5 files.

**Fix:** Create reddit_cli/errors.py with shared error handler.

---

### 4. Add User-Agent Header

**Issue:** Reddit API requests lack User-Agent header.

**Location:** reddit_cli/reddit/base.py

**Fix:** Add headers parameter to httpx.AsyncClient.

---

## MEDIUM Priority

### 5. Implement Semantic Exit Codes

**Issue:** All errors exit with code 1 regardless of type.

**Fix:** Use exit code 2 for usage errors, exit code 1 for general errors.

---

### 6. Add Input Validation

**Issue:** Options like --sort, --period accept any string.

**Fix:** Use Typer validators or Enum types.

---

### 7. Replace print() with typer.echo()

**Issue:** All output uses print() instead of typer.echo().

**Fix:** Replace throughout commands.

---

### 8. Add Retry Logic with Backoff

**Issue:** No retry on transient errors (429, 500, 503).

**Fix:** Implement retry with exponential backoff.

---

## LOW Priority

### 9. Add Structured Logging
### 10. Consider Subcommand Grouping
### 11. Add Terminal Escape Code Sanitization

---

## Quick Wins (Under 30 Minutes Each)

1. Remove unused app = typer.Typer() lines (5 files)
2. Add User-Agent header to httpx client
3. Extract error handler to shared module
4. Add output assertions to existing tests
5. Fix the post command unused options

---

*Report generated for project: better-reddit-cli v0.4.4*
