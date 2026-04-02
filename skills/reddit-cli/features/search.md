# Search Command

Search for posts across all of Reddit.

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
