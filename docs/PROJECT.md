# Reddit CLI Explorer

A command-line tool for browsing Reddit subreddits without requiring an API key.

## Overview

This project uses Reddit's public JSON API to explore subreddits, view posts, and read comments directly from the terminal.

## Architecture

```
reddit-explorer/
├── main.py              # Typer entry point
├── reddit/
│   ├── __init__.py
│   ├── client.py        # Reddit JSON API client
│   ├── models.py        # Pydantic models
│   └── formatters.py    # CLI output formatting
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

## Features

- Browse subreddits (hot, new, top, rising, controversial)
- View posts with comments
- Search across Reddit
- Save posts locally
- Interactive navigation

## API

The project uses Reddit's public JSON endpoints:

```
https://www.reddit.com/r/{subreddit}/{sort}.json
```

No authentication required for read operations.

## Usage

```
redditexplorer --help
redditexplorer browse <subreddit>
redditexplorer view <post_id>
redditexplorer search <query>
```

## License

MIT
