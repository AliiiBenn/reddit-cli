# CLI Commands Review

## Command Inventory

### Navigation Commands

#### `frontpage`
- **File:** `commands/navigation.py`
- **Arguments:** None
- **Options:** `--sort`, `--limit`, `--period`, `--after`, `--before`
- **Implementation:** Delegates to `browse_async(subreddit="reddit")`
- **Issue:** Hardcoded "reddit" subreddit - no user personalization

#### `home`
- **File:** `commands/navigation.py`
- **Arguments:** None
- **Options:** Same as `frontpage`
- **Implementation:** Alias for `frontpage`
- **Issue:** Documentation says "home" but implementation is identical to frontpage

#### `best`
- **File:** `commands/navigation.py`
- **Arguments:** None
- **Options:** `--limit`, `--period`, `--after`, `--before`
- **Implementation:** Delegates to `browse_async(subreddit="reddit", sort="top")`
- **Issue:** Uses hardcoded "reddit" instead of true "best" across all subreddits

---

### Browse Commands

#### `browse`
- **File:** `commands/browse.py`
- **Arguments:** `subreddit` (required)
- **Options:**
  - `--sticky` (boolean)
  - `--random` (boolean)
  - `--search` (string, optional)
  - `--sort` (string, default: "hot")
  - `--limit` (int, default: 25)
  - `--period` (string, optional)
  - `--after` (string, optional)
  - `--before` (string, optional)
- **Implementation:** Dispatches to `_browse_async`, `_sticky_async`, `_random_async`, `_search_async`

**Issues:**
1. `--sticky`, `--random`, `--search` are mutually exclusive but not enforced
2. No validation of `sort` values (accepts any string)
3. `limit` max is 100 but not enforced at CLI layer
4. Missing `--sort` validation (should be: hot, new, top, rising, controversial, gilded)

---

### Post Commands

#### `post`
- **File:** `commands/post.py`
- **Arguments:** `post_id` (required)
- **Options:**
  - `--view` (boolean, unused)
  - `--info` (boolean, unused)
  - `--duplicates` (boolean)
- **Issue:** `--view` and `--info` flags are defined but never checked in code

```python
# Lines 66-86 - options defined but not used
if duplicates:
    asyncio.run(_duplicates_async(post_id))
else:
    asyncio.run(_post_async(post_id))
# view and info flags are silently ignored!
```

---

### Comment Commands

#### `comments`
- **File:** `commands/comments.py`
- **Arguments:** `post_id` (required)
- **Options:**
  - `--sort` (string, default: "confidence")
  - `--depth` (int, optional)

#### `comment` (singular)
- **File:** `commands/comments.py`
- **Arguments:** `post_id` (required), `comment_id` (required)
- **Options:** `--replies` (boolean)
- **Implementation:** Fetches all comments then filters client-side

**Issue:** Uses depth=999 as sentinel for "unlimited" instead of None

---

### Subreddit Commands

#### `subreddit`
- **File:** `commands/subreddit.py`
- **Arguments:** `name` (required)
- **Options:**
  - `--rules` (boolean)
  - `--moderators` (boolean)

**Issues:**
1. Moderators endpoint returns 403 for private subreddits but this is caught with bare `except` and prints user-friendly message

#### `subreddits`
- **File:** `commands/subreddit.py`
- **Arguments:** None
- **Options:**
  - `--search` (string, optional)
  - `--new` (boolean)
  - `--gold` (boolean)
  - `--default` (boolean)
  - `--sort` (string, default: "subscribers")
  - `--limit` (int, default: 25)

**Issues:**
1. Mutually exclusive options (`--search`, `--new`, `--gold`, `--default`) not enforced
2. `--sort` not validated (should be: subscribers, active)

---

### Search Command

#### `search`
- **File:** `commands/search.py`
- **Arguments:** `query` (required)
- **Options:**
  - `--sort` (string, default: "relevance")
  - `--limit` (int, default: 25)
  - `--period` (string, optional)

---

### Utility Commands

#### `ping`
- **File:** `__init__.py`
- **Arguments:** None
- **Options:** None
- **Output:** "pong"
- **Issue:** Uses `print()` instead of `typer.echo()`

#### `help`
- **File:** `__init__.py`
- **Arguments:** None
- **Options:** None
- **Issue:** Uses custom `print(HELP_TEXT)` instead of Typer's built-in help system

---

## Option Validation Issues

### Unvalidated Options

| Option | Valid Values | Current Behavior |
|--------|--------------|------------------|
| `--sort` (browse) | hot, new, top, rising, controversial, gilded | Accepts any string |
| `--sort` (search) | relevance, hot, top, new, comments | Accepts any string |
| `--sort` (frontpage) | hot, new, top, rising, controversial, gilded | Accepts any string |
| `--period` | day, week, month, year, all | Accepts any string |
| `--limit` | 1-100 | Accepts any int (API may reject) |

### Impact

Invalid values are passed directly to Reddit API which returns 400 Bad Request, resulting in user-friendly error but no indication of which value was wrong.

---

## Missing Options from Documentation

| Documentation | Implementation | Status |
|---------------|----------------|--------|
| `reddit view <id>` | Not implemented | MISSING |
| `reddit browse --sticky` | Implemented | OK |
| `reddit browse --random` | Implemented | OK |
| `reddit subreddits --sort active` | Parameter accepted | PARTIAL (API may not support) |

---

## ID Prefix Handling

The codebase handles Reddit ID prefixes inconsistently:

```python
# posts.py - strips prefix
if post_id.startswith("t3_"):
    post_id = post_id[3:]

# comments.py - strips prefix
if post_id.startswith("t3_"):
    post_id = post_id[3:]

# subreddits.py - strips prefix (r/ only)
if name.startswith("r/"):
    name = name[2:]
```

**Issue:** No validation if prefix is wrong (e.g., `t1_` for post ID)

---

## Output Formatting

All commands use `print()` for output, not `typer.echo()`:

```python
print(f"[{post.score}] {post.title}")  # Throughout codebase
```

**Impact:**
- Does not respect `--ansi` / `--no-ansi` flags
- Does not respect `NO_COLOR` environment variable
- Output may not be properly formatted in all terminals

---

## Summary of CLI Issues

| Severity | Issue | Location |
|----------|-------|----------|
| HIGH | Unused options `--view`, `--info` | post.py:66-86 |
| HIGH | Mutually exclusive options not enforced | browse.py, subreddit.py |
| MEDIUM | No validation for sort/period/limit | Multiple |
| MEDIUM | Output uses print() instead of typer.echo() | All commands |
| LOW | ping/help use bare print() | __init__.py |
| LOW | Inconsistent ID prefix handling | clients |

---

*Report generated for project: better-reddit-cli v0.4.4*
