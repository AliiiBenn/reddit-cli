<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="public/banner.jpg">
    <source media="(prefers-color-scheme: light)" srcset="public/banner.jpg">
    <img src="public/banner.jpg" alt="Reddit CLI Logo" width="100%">
  </picture>
</p>

<h1 align="center">Reddit CLI</h1>

<p align="center">
  Browse Reddit from your terminal. No API key, no authentication, no hassle.
</p>

<p align="center">
  <a href="https://github.com/AliiiBenn/reddit-cli">
    <img src="https://img.shields.io/github/license/AliiiBenn/reddit-cli" alt="License">
  </a>
  <a href="https://github.com/AliiiBenn/reddit-cli/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/AliiiBenn/reddit-cli/test" alt="Tests">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/python-3.14+-blue" alt="Python">
  </a>
</p>

Explore subreddits, dive into discussions, and discover trending content - all from a sleek command-line interface.

## Why Reddit CLI?

- **Zero setup** - No API key needed, just install and go
- **Blazing fast** - Async HTTP powered by httpx
- **Explore deeply** - Pagination, sorting, and threaded comments
- **Clean output** - Readable formatting right in your terminal

## Features

- Browse subreddits with 6 sorting modes (hot, new, top, rising, controversial, gilded)
- View posts with full metadata
- Threaded comment display with depth control
- Pagination support for infinite scrolling
- Subreddit info, rules, and moderator discovery
- 100% type-annotated Python

## Quick Start

```bash
# Install
uv add reddit

# Browse the frontpage
reddit

# Explore a subreddit
reddit browse python --limit 10

# View a post and its comments
reddit view t3_abc123
reddit comments t3_abc123 --depth 3

# Discover subreddits
reddit subreddits --sort subscribers
reddit subreddit python --rules
```

## Command Overview

| Command | Description |
|---------|-------------|
| `reddit` | Frontpage (hot posts) |
| `reddit browse <sub>` | Browse a subreddit |
| `reddit view <id>` | View a post |
| `reddit comments <id>` | View post comments |
| `reddit subreddit <name>` | Subreddit info |
| `reddit subreddits` | List popular subreddits |

## Browse Options

```
--sort hot|new|top|rising|controversial|gilded
--limit <n>     Number of posts (max 100)
--period day|week|month|year|all
--after <id>    Next page
--before <id>    Previous page
```

## Development

```bash
# Clone and install
git clone https://github.com/AliiiBenn/reddit-cli.git
cd reddit-cli
uv sync

# Run tests
uv run pytest

# Lint and type-check
uv run ruff check .
uv run mypy reddit_cli

# Try it out
uv run reddit browse python
```

## Contributing

Contributions are welcome! Feel free to open issues or submit PRs.

## License

MIT - See [LICENSE](LICENSE) for details.
