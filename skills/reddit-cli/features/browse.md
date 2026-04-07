# Browse Command

Browse posts from any subreddit.

## When to Use

Use `reddit browse` when you:
- Want to explore posts in a specific subreddit (e.g., r/python, r/programming)
- Know which subreddit you want to read
- Need to browse posts sorted by hot/new/top within a community
- Want to filter by time period (week, month, year)

**Don't use browse when:**
- You don't know which subreddit to look at → use `reddit search` instead
- You want to find a specific post → use `reddit search <query>` instead

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
