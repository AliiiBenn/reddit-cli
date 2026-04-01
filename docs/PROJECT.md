# Reddit CLI

A command-line tool for browsing and analyzing Reddit data without requiring an API key.

## Overview

This project uses Reddit's public JSON API to explore subreddits, analyze posts and comments, and extract business insights directly from the terminal.

## Architecture

```
reddit_cli/
├── __init__.py          # Main Typer app entry point
├── commands/
│   ├── navigation.py    # Navigation commands (frontpage, home, best)
│   ├── subreddit.py    # Subreddit commands (subreddits, subreddit info)
│   ├── browse.py       # Browse commands (browse with sort/period/limit)
│   ├── post.py         # Post commands (view, post)
│   ├── comments.py     # Comments commands (comments with sort/depth)
│   └── comment.py      # Single comment commands
├── reddit/
│   ├── __init__.py     # Reddit client aggregate
│   ├── base.py         # Async HTTP client (httpx.AsyncClient)
│   ├── subreddits.py   # Subreddit endpoints
│   ├── posts.py        # Post endpoints
│   ├── comments.py     # Comment endpoints
│   └── models.py       # Pydantic models
├── formatters.py        # CLI output formatting
├── cache/
│   └── cache.py         # Local JSON cache
├── pyproject.toml
└── README.md
```

## Dependencies

- **typer** - CLI framework
- **httpx** - Async HTTP client
- **pydantic** - Data validation
- **rich** - Rich terminal output

---

## API Endpoints Used

```
# Submissions
GET /r/{subreddit}/hot.json
GET /r/{subreddit}/new.json
GET /r/{subreddit}/top.json
GET /r/{subreddit}/rising.json
GET /r/{subreddit}/controversial.json
GET /r/{subreddit}/gilded.json
GET /r/{subreddit}/{post_id}.json
GET /r/{subreddit}/comments/{post_id}.json

# Subreddits
GET /subreddits.json
GET /r/{subreddit}/about.json
GET /r/{subreddit}/about/rules.json
GET /r/{subreddit}/about/moderators.json
GET /r/{subreddit}/about/related.json
```

---

## License

MIT
