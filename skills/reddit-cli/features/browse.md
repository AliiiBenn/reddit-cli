# Browse Command

Browse posts from any subreddit.

## Command

```bash
reddit browse <subreddit>
reddit browse <subreddit> [options]
```

## Options

| Option | Description |
|--------|-------------|
| `--sort` | Sort by: hot, new, top, rising, controversial, gilded (default: hot) |
| `--limit` | Number of posts: 1-100 (default: 25) |
| `--period` | Time range: day, week, month, year, all |
| `--after` | Get posts after this ID (for pagination) |
| `--before` | Get posts before this ID (for pagination) |
| `--search` | Search within the subreddit instead of listing |
| `--format` | Output format: display, csv, sql, json, xlsx |
| `--output` | Write to file instead of stdout |

## Examples

```bash
# Browse hot posts from python subreddit
reddit browse python

# Top 10 posts this week
reddit browse programming --sort top --period week --limit 10

# Search within subreddit
reddit browse javascript --search "react hooks"

# Search with sorting
reddit browse python --search "async" --sort new --limit 20
```

## Pagination

Use `--after` or `--before` with IDs from previous output to navigate pages:

```bash
# First page
reddit browse python --limit 10

# Next page (use the last ID from previous output)
reddit browse python --limit 10 --after t3_abc123
```
