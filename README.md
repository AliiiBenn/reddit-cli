<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="public/banner.jpg">
    <source media="(prefers-color-scheme: light)" srcset="public/banner.jpg">
    <img src="public/banner.jpg" alt="Reddit CLI Logo" width="100%">
  </picture>
</p>

<h1 align="center">Reddit CLI</h1>

<p align="center">
  A command-line tool for browsing Reddit without requiring an API key.
</p>

<p align="center">
  <a href="https://github.com/AliiiBenn/reddit-cli">
    <img src="https://img.shields.io/github/license/AliiiBenn/reddit-cli" alt="License">
  </a>
</p>

> Browse Reddit from the terminal. No authentication required.

## Features

- Browse subreddits (hot, new, top, rising, controversial, gilded)
- View posts and comments
- Navigate with pagination cursors
- Explore subreddit info, rules, and moderators
- Async HTTP client using httpx

## Requirements

- Python 3.14+

## Installation

```bash
# Using uv
uv add reddit

# Or using pip
pip install reddit
```

## Usage

```bash
# Browse frontpage
reddit

# Browse a subreddit
reddit browse python --sort hot --limit 10

# View a post
reddit view t3_abc123

# View comments
reddit comments t3_abc123 --sort top --depth 3

# Get subreddit info
reddit subreddit python --rules

# List popular subreddits
reddit subreddits --sort subscribers
```

## Navigation Commands

| Command | Description |
|---------|-------------|
| `reddit` | Frontpage (hot posts) |
| `reddit frontpage` | Browse r/reddit hot posts |
| `reddit home` | Alias for frontpage |
| `reddit best` | Top posts of all time |

## Browse Options

```
--sort hot|new|top|rising|controversial|gilded
--limit <n>     Number of posts (max 100)
--period day|week|month|year|all
--after <id>    Pagination cursor
--before <id>   Pagination cursor
```

## Development

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Run CLI
uv run reddit <command>
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see the [LICENSE](LICENSE) file for details.
