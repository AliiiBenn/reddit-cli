name: reddit-cli
description: A command-line tool for browsing Reddit without an API key. Use when asking about Reddit CLI commands, browsing subreddits, searching posts, viewing comments, or getting subreddit info. No authentication required.
disable-model-invocation: false
allowed-tools: Read,Grep,Glob,Bash
---

# Reddit CLI Skill

Browse Reddit from your terminal - no API key needed.

## Quick Examples

```bash
# Browse a subreddit
reddit browse python --sort hot --limit 10

# Search globally
reddit search programming --sort top --period month

# View a post
reddit post t3_abc123

# View comments
reddit comments t3_abc123 --sort top --depth 3

# Get subreddit info
reddit subreddit python --rules
```

## Commands Overview

| Command | Description |
|---------|-------------|
| `reddit frontpage` | Browse Reddit's frontpage |
| `reddit home` | Alias for frontpage |
| `reddit best` | Top posts of all time |
| `reddit browse <subreddit>` | Browse posts from a subreddit |
| `reddit search <query>` | Search posts across Reddit |
| `reddit post <post_id>` | View a single post |
| `reddit comments <post_id>` | View comments for a post |
| `reddit comment <post_id> <comment_id>` | View a specific comment |
| `reddit subreddit <name>` | Get subreddit info |
| `reddit subreddits` | List popular subreddits |

## Key Features

- **No API key required** - uses Reddit's public JSON API
- **Async requests** - fast, non-blocking
- **Retry logic** - automatic retry on rate limits
- **Input validation** - clear error messages

## Additional Resources

For detailed command usage:
- [navigation.md](features/navigation.md) - frontpage, home, best
- [browse.md](features/browse.md) - browse command
- [search.md](features/search.md) - global search
- [post.md](features/post.md) - view posts
- [comments.md](features/comments.md) - view comments
- [subreddit.md](features/subreddit.md) - subreddit info and listing
- [error-handling.md](features/error-handling.md) - troubleshooting
