# Architecture Review

## Project Structure

```
reddit_cli/
├── __init__.py          # Main app entry, Typer app definition
├── commands/             # CLI command implementations
│   ├── browse.py        # browse, sticky, random, search
│   ├── comments.py      # comments, comment (single)
│   ├── navigation.py    # frontpage, home, best
│   ├── post.py          # post view, info, duplicates
│   ├── search.py        # global search
│   └── subreddit.py     # subreddit, subreddits
└── reddit/              # API client layer
    ├── __init__.py      # Re-exports
    ├── base.py          # RedditClient (HTTP)
    ├── models.py        # Pydantic models
    ├── posts.py         # PostsClient
    ├── comments.py      # CommentsClient
    └── subreddits.py   # SubredditsClient
```

---

## Layer Analysis

### Layer 1: CLI Commands (`commands/`)

**Purpose:** Parse user input, orchestrate API calls, format output

**Observations:**
- Each command file creates its own `typer.Typer()` instance (anti-pattern)
- Commands are registered directly on the main app via decorators
- No shared state between commands
- Each file has its own `_handle_api_error()` function

**Issues:**
1. **Duplicate Typer instances** - Each command module creates `app = typer.Typer()` but they are never used
   - `browse.py`: `app = typer.Typer()` (unused)
   - `comments.py`: `app = typer.Typer()` (unused)
   - `post.py`: `app = typer.Typer()` (unused)
   - `search.py`: `app = typer.Typer()` (unused)
   - `navigation.py`: `app = typer.Typer()` (unused)
   - `subreddit.py`: `subreddit_app = typer.Typer()`, `subreddits_app = typer.Typer()` (unused)

2. **Code duplication** - `_handle_api_error()` is copy-pasted 5 times

### Layer 2: API Clients (`reddit/`)

**Purpose:** Encapsulate Reddit JSON API calls

**Clients:**
- `RedditClient` - Base HTTP client using httpx.AsyncClient
- `PostsClient` - Post-related endpoints
- `CommentsClient` - Comment endpoints with recursive parsing
- `SubredditsClient` - Subreddit endpoints

**Observations:**
- Clean separation from CLI layer
- Proper use of async/await
- Context manager pattern for client lifecycle

**Issues:**
1. No retry logic or backoff
2. No User-Agent header (Reddit may block requests without it)
3. Limited error handling beyond status code checks

---

## Command Registration Analysis

### Current Approach (Anti-pattern)

```python
# In __init__.py
app = typer.Typer()
app.command()(browse)      # Flat registration
app.command()(post)
app.command()(subreddit)
app.command()(subreddits)
app.command()(comments)
# ...
```

### Issues with Flat Registration

1. **No command grouping** - `post view`, `post duplicates` should be subcommands of `post`
2. **No shared callbacks** - Cannot share state between related commands
3. **Help text organization** - All commands appear at same level

### Recommended Approach (Subcommand Groups)

```python
# Using add_typer() for command groups
post_app = Typer()
app.add_typer(post_app, name="post")

@post_app.command(name="view")
def post_view(post_id: str): ...

@post_app.command(name="duplicates")
def post_duplicates(post_id: str): ...
```

**Note:** The current structure with flat commands actually matches the documented usage pattern in the README:
- `reddit browse python` (not `reddit browse python hot`)
- `reddit post t3_abc123` (not `reddit post view t3_abc123`)

So the flat structure may be intentional for usability.

---

## Async Flow Analysis

```
CLI Command (sync)
    │
    ▼
asyncio.run(_async_impl(...))
    │
    ▼
async with RedditClient() as client:
    │
    ▼
PostsClient(client).list_posts(...)
    │
    ▼
client.get(path, params)
```

**Pattern:** 
- CLI commands are sync wrappers around async implementations
- Each async function creates its own RedditClient instance
- HTTP client is properly closed via context manager

**Issue:** Creating a new HTTP client for each command may not efficiently handle connection pooling.

---

## Dependency Graph

```
__init__.py (app)
    │
    ├── commands/browse.py ──────► reddit/posts.py ──────► reddit/base.py
    ├── commands/comments.py ───► reddit/comments.py ──► reddit/base.py
    ├── commands/post.py ───────► reddit/posts.py ─────► reddit/base.py
    ├── commands/search.py ─────► reddit/posts.py ─────► reddit/base.py
    ├── commands/navigation.py ─► reddit/posts.py ─────► reddit/base.py
    ├── commands/subreddit.py ──► reddit/subreddits.py ─► reddit/base.py
    │
    └── reddit/models.py (shared Pydantic models)
```

---

## Summary

| Aspect | Finding | Severity |
|--------|---------|----------|
| Structure | Clean separation of concerns | N/A |
| Modularity | Commands well-separated by domain | N/A |
| Code Sharing | Duplicated error handling | HIGH |
| Extensibility | Flat commands limit grouping | MEDIUM |
| Async Design | Proper async/await usage | N/A |
| Resource Mgmt | Context managers for HTTP client | N/A |

---

## Recommendations

1. **Extract shared error handler** - Create `reddit_cli/utils.py` with shared `_handle_api_error()`
2. **Remove unused Typer instances** - Delete `app = typer.Typer()` from command files
3. **Consider subcommand grouping** - For `post view/info/duplicates` if UX benefits outweigh complexity
4. **Add connection pooling** - Reuse single httpx client across commands (if performance critical)
5. **Add User-Agent header** - Reddit API requires this

*Report generated for project: better-reddit-cli v0.4.4*
