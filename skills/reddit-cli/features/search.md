# Search Command

Search for posts across all of Reddit.

## When to Use

Use `reddit search` when you:
- Don't know which subreddit to look at
- Want to find posts about a specific topic or keyword
- Are looking for something across all of Reddit
- Want to discover communities related to a topic

**Don't use search when:**
- You already know the subreddit → use `reddit browse <subreddit> --search` instead
- You want to browse a community's recent posts → use `reddit browse <subreddit>` instead

## Command

```bash
reddit search <query>
reddit search <query> [options]
```

## Examples

```bash
# Basic search
reddit search programming

# Top posts this month
reddit search "python tips" --sort top --period month

# Most commented
reddit search javascript --sort comments --limit 50

# Recent posts
reddit search rust --sort new
```

## Options

| Option | Description |
|--------|-------------|
| `--sort` | Sort by: relevance, hot, top, new, comments (default: relevance) |
| `--limit` | Number of results: 1-100 (default: 25) |
| `--period` | Time range: hour, day, week, month, year, all |
| `--format` | Output format: display, csv, sql, json, xlsx |
| `--output` | Write to file instead of stdout |

## Search vs Browse

| Aspect | `reddit search` | `reddit browse <subreddit> --search` |
|--------|-----------------|-------------------------------------|
| Scope | All of Reddit | One specific subreddit |
| Default sort | relevance | relevance |

## Sort Options

| Sort | Description |
|------|-------------|
| `relevance` | Best match (default) |
| `hot` | Hottest posts |
| `top` | Top scored |
| `new` | Most recent |
| `comments` | Most commented |
