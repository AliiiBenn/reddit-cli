# Code Quality Review

## Overview

This review covers code quality issues including code smells, anti-patterns, maintainability concerns, and deviation from Python best practices.

---

## Code Duplication (HIGH Severity)

### 1. Duplicate Error Handler

The function _handle_api_error() is identical across 5 command files (12 lines each).

Total duplicated lines: ~60 lines

### 2. Duplicate Output Formatting

Every command file has similar print statements for formatting posts:

    print(f"[{post.score}] {post.title}")
    print(f"  ID: {post.id}")
    print(f"  r/{post.subreddit} by {post.author}")
    print(f"  {post.num_comments} comments")

No shared formatting utility exists.

### 3. Duplicate RedditClient Instantiation

    async with RedditClient() as client:
        posts_client = PostsClient(client)

This pattern is repeated in every command with different clients.

---

## Unused Code (MEDIUM Severity)

### 1. Unused Typer Instances

All command files except subreddit.py create:

    app = typer.Typer()  # Never used

### 2. Unused Options in post Command

Location: commands/post.py lines 66-86

    view: bool = False,   # Defined but never checked
    info: bool = False,   # Defined but never checked

Only duplicates is actually checked.

---

## Type Annotation Issues (LOW Severity)

### 1. Self-referencing Type in Pydantic Model

    replies: list["Comment"] = []

Requires quotes due to forward reference. Modern Python (3.14) supports list[Comment] directly.

---

## String Formatting (LOW Severity)

### 1. f-string with encode/decode

Location: Multiple files

    body = comment.body.encode(sys.stdout.encoding, errors="replace").decode(sys.stdout.encoding)

Purpose: Handle non-BMP characters. Could be extracted to utility function.

### 2. String Truncation

    print(f"     {rule.get('description', 'N/A')[:100]}...")

Magic number 100 used directly. Should be a constant.

---

## API Client Issues

### 1. No User-Agent Header

Location: reddit/base.py

Reddit API recommends setting a User-Agent header. The httpx client does not set one.

Impact: Reddit may block or rate-limit requests more aggressively.

### 2. No Connection Pooling

Each command creates a new httpx.AsyncClient:

    async with RedditClient() as client:  # New client each time

For a CLI tool making one request per invocation, this is fine.

### 3. No Request Timeout Configuration

    TIMEOUT = 10.0  # Hardcoded

Could be made configurable.

---

## Pydantic Model Issues

### 1. Mutable Default in replies

    replies: list["Comment"] = []

While Pydantic handles this correctly, it is an anti-pattern. Better to use:

    replies: list["Comment"] = Field(default_factory=list)

### 2. No Field Validation

No Pydantic validators ensure data integrity (e.g., id should start with expected prefix).

---

## Maintainability Concerns

### 1. Magic Strings

    path = f"/r/{subreddit}/{sort}.json"
    "/by_id/t3_{post_id}.json"

Could be extracted to constants or enum.

### 2. No Structured Logging

All output goes to stdout via print(). No logging module used.

### 3. Inconsistent Documentation

Some functions have docstrings, others have inline comments.

---

## Summary Table

| Category | Issue | Severity | Location |
|----------|-------|----------|----------|
| Duplication | Error handler copied 5x | HIGH | commands/*.py |
| Unused Code | Typer instances not used | MEDIUM | browse.py, etc. |
| Unused Code | --view, --info options ignored | HIGH | post.py |
| API Client | No User-Agent header | MEDIUM | reddit/base.py |
| Pydantic | Mutable default in model | LOW | models.py |
| Maintainability | Magic strings | LOW | posts.py |
| Maintainability | No structured logging | LOW | All files |

---

*Report generated for project: better-reddit-cli v0.4.4*
