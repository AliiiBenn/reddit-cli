# Reddit CLI - Remaining Issues Investigation Report

**Date:** 2026-04-02
**Project:** reddit_cli

---

## Issue 1: Error handling duplication in browse.py

**Status:** RESOLVED

**Finding:**
The issue described that `_handle_api_error()` was redefined in browse.py instead of being imported from errors.py. After reviewing `browse.py:1-5`, the code now correctly imports the error handling functions:

```python
from reddit_cli.errors import handle_api_error, handle_validation_error
```

No duplication exists. The fix has been properly applied.

---

## Issue 2: Inconsistency between navigation.py and browse.py

**Status:** BY DESIGN (no issue)

**Finding:**
The current structure is intentional:

| File | Contains | Purpose |
|------|----------|---------|
| `navigation.py` | `frontpage()`, `home()`, `best()` | Navigation commands for Reddit's built-in feeds |
| `browse.py` | `browse()` | General subreddit browsing with filtering options |

This separation makes sense architecturally:
- `navigation.py` handles Reddit's pre-defined feeds (frontpage, home, best) that don't require a subreddit argument
- `browse.py` handles user-specified subreddit browsing with full filter options (sort, period, sticky, random, search)

In `__init__.py`, all commands are registered as separate top-level commands regardless of which file they come from.

---

## Issue 3: Potential dead code in base.py:77-79

**Status:** DEFECT FOUND

**Location:** `reddit_cli/reddit/base.py:47-79`

**Analysis:**
The retry logic has a structural issue. `last_exception` is initialized to `None` at line 47 but is never assigned inside the retry loop. The exception handlers at lines 72-75 re-raise exceptions immediately:

```python
except (httpx.TimeoutException, httpx.ConnectError):
    raise
except httpx.HTTPStatusError:
    raise
```

Since all caught exceptions are re-raised immediately, `last_exception` remains `None` throughout loop execution.

**Problem:** If any unexpected exception type occurs that is not `TimeoutException`, `ConnectError`, or `HTTPStatusError`, it would propagate up without being stored. The fallback `RuntimeError("Max retries exceeded")` at line 79 would then incorrectly mask the original error.

**Additional Issue - Incorrect Error Handling Flow:**
For retryable status codes (429, 5xx), when `attempt == MAX_RETRIES - 1` and the condition fails, the code calls `response.raise_for_status()` but does not store the exception in `last_exception`. If this raises, it bypasses the `last_exception` check entirely.

**Fix Recommendation:**
```python
except (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPStatusError) as e:
    last_exception = e
    raise
```

Or better yet, restructure to properly capture and re-raise the final exception.

---

## Issue 4: Encoding issue with sys.stdout.encoding

**Status:** POTENTIAL ISSUE (acceptable workaround)

**Locations:**
- `commands/comments.py:26-27`
- `commands/comments.py:93-94`
- `commands/post.py:24`
- `commands/subreddit.py:61-63`

**Analysis:**
The code uses:
```python
body = comment.body.encode(sys.stdout.encoding, errors="replace").decode(sys.stdout.encoding)
```

**Potential Issues:**

1. **stdout.encoding can be None:** In some unusual environments (certain CI systems, redirected stdout in Python's stdin encoding mode), `sys.stdout.encoding` could be `None`, causing `AttributeError`.

2. **ASCII-only encoding corruption:** If stdout.encoding is ASCII (rare), characters outside ASCII range will be replaced with `?` or `\ufffd`, silently corrupting non-ASCII content.

**Current Mitigation:**
The `errors="replace"` parameter prevents crashes but causes silent character substitution.

**Risk Assessment:** Low to Medium
- Most modern terminals use UTF-8
- The fallback handles most edge cases
- Reddit content typically displays correctly

**Better Fix:**
```python
encoding = sys.stdout.encoding or "utf-8"
body = comment.body.encode(encoding, errors="replace").decode(encoding)
```

---

## Issue 5: --sort validation on frontpage

**Status:** DEFECT FOUND

**Finding:**
The issue claimed `reddit frontpage --sort invalid` passes through without local validation.

**Current Behavior:**
Looking at `navigation.py:80-84`:
```python
try:
    _validate_sort_period(sort, period, limit)
    asyncio.run(_browse_frontpage_async(sort, limit, period, after, before))
except Exception as e:
    handle_api_error(e)
```

The `_validate_sort_period()` function IS called, which validates `sort` against `VALID_SORT_VALUES`. If invalid, it calls `handle_validation_error()` which exits with code 2.

**However:** The `_validate_sort_period` function is defined in **browse.py** (lines 13-32), not in navigation.py.

Looking at `navigation.py:1-5`:
```python
from reddit_cli.errors import handle_api_error, handle_validation_error
from reddit_cli.reddit import RedditClient, PostsClient
```

The `_validate_sort_period` function is NOT imported into navigation.py. But it is used directly in `frontpage()`, `home()`, and `best()` at lines 81, 104, and 125.

This means navigation.py calls `_validate_sort_period()` but does NOT import it. This would cause a `NameError` at runtime if someone runs `reddit frontpage --sort invalid`.

---

## Issue 6: --sticky and --random (403 Auth required)

**Status:** DOCUMENTED LIMITATION (API change)

**Finding:**
Both `get_sticky()` and `get_random()` in `reddit_cli/reddit/posts.py` use public API endpoints that Reddit now requires OAuth for:

**sticky** (`posts.py:63-70`):
```python
async def get_sticky(self, subreddit: str) -> Post:
    data = await self._client.get(f"/r/{subreddit}/sticky.json")
    return Post(**data["data"]["children"][0]["data"])
```

**random** (`posts.py:72-82`):
```python
async def get_random(self, subreddit: str) -> Post:
    data = await self._client.get(f"/r/{subreddit}/random.json")
    posts = data.get("data", {}).get("children", [])
    if posts:
        return Post(**posts[0]["data"])
    raise ValueError(f"No random post found in r/{subreddit}")
```

**Root Cause:** Reddit's API changes have restricted these endpoints to OAuth-authenticated requests only. The CLI uses a simple User-Agent header which does not authenticate.

**Error Handling:**
- `_sticky_async()` in `browse.py:65-74` has no try/except for the 403 error
- `_random_async()` in `browse.py:77-89` catches `ValueError` but not HTTP errors

**Current Behavior:** When called, these will raise `HTTPStatusError(403)` which is caught by the outer `handle_api_error()` in `browse.py:164-165`.

**Recommendation:**
1. Catch 403 specifically in `_sticky_async()` and `_random_async()`
2. Provide user-friendly message: "This feature requires Reddit authentication"
3. Consider implementing OAuth flow for full functionality

---

## Issue 7: --duplicates 404 on valid posts

**Status:** DEFECT FOUND

**Location:** `reddit_cli/reddit/posts.py:84-119`

**Finding:**
The `get_duplicates()` method has multiple issues with Reddit API response parsing:

**Issue 1 - Incorrect Key Access:**
```python
children = data.get("", data.get("data", {}))  # Line 107
```
Uses empty string `""` as a key fallback, which is incorrect. Reddit API uses specific response structures.

**Issue 2 - Complex Response Format:**
Reddit's `/api/duplicates/{id}.json` endpoint returns a JSON list:
```json
[
  {"kind": "Listing", "data": {"children": [...original post...]}},
  {"kind": "Listing", "data": {"children": [...duplicates...]}}
]
```

**Issue 3 - Incorrect Data Extraction:**
The code at lines 99-103:
```python
if isinstance(data, list) and len(data) >= 2:
    original = [Post(**p["data"]) for p in data[0].get("data", {}).get("children", [])]
    duplicates = [Post(**p["data"]) for p in data[1].get("data", {}).get("children", [])]
```

This tries to get `p["data"]` from each child, but children are dicts with structure `{"kind": "...", "data": {...}}`. The code SHOULD be `p["data"]["data"]` (first "data" is the child wrapper, second "data" is the actual post data).

**Issue 4 - Fallback Logic May Hide Errors:**
Lines 106-118 contain multiple fallback attempts that could mask legitimate 404 errors or other API issues.

**Root Cause:** The Reddit duplicate/crosspost API has changed its response format, and the current code doesn't correctly parse it.

**Fix Recommendation:**
```python
async def get_duplicates(self, post_id: str) -> tuple[Post, list[Post]]:
    if post_id.startswith("t3_"):
        post_id = post_id[3:]

    data = await self._client.get(f"/api/duplicates/t3_{post_id}.json")

    if not isinstance(data, list) or len(data) < 2:
        return Post(id="", title="", author="", subreddit="", score=0, num_comments=0, permalink="", url="", created_utc=0.0), []

    original_data = data[0].get("data", {}).get("children", [])
    duplicates_data = data[1].get("data", {}).get("children", [])

    if not original_data:
        return Post(id="", title="", author="", subreddit="", score=0, num_comments=0, permalink="", url="", created_utc=0.0), []

    original = Post(**original_data[0]["data"])
    duplicates = [Post(**p["data"]) for p in duplicates_data]

    return original, duplicates
```

---

## Summary Table

| Issue | Status | Severity | Fix Required |
|-------|--------|----------|--------------|
| 1. Error duplication | RESOLVED | - | None |
| 2. navigation/browse inconsistency | BY DESIGN | - | None |
| 3. Dead code in base.py | DEFECT | HIGH | Yes - exception not captured |
| 4. Encoding issue | ACCEPTABLE | LOW | Optional - UTF-8 fallback |
| 5. --sort validation | DEFECT | MEDIUM | Yes - missing import |
| 6. --sticky/--random 403 | DOC LIMITATION | LOW | User-friendly error message |
| 7. --duplicates 404 | DEFECT | HIGH | Yes - API parsing bugs |

---

## Priority Fixes

1. **Issue 7 (HIGH):** Fix `get_duplicates()` API parsing - currently broken
2. **Issue 3 (HIGH):** Fix exception capture in retry logic in `base.py`
3. **Issue 5 (MEDIUM):** Fix missing import of `_validate_sort_period` in navigation.py
4. **Issue 6 (LOW):** Add graceful 403 handling for sticky/random commands