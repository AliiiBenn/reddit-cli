# Navigation Commands

Browse Reddit's frontpage and top posts.

## When to Use

Use `reddit frontpage` or `reddit home` when you:
- Want to see what's trending on Reddit right now
- Start your Reddit session without a specific topic in mind
- Want to discover popular content across all of Reddit

Use `reddit best` when you:
- Want to see the all-time best posts on Reddit
- Are looking for highly-regarded content worth reading
- Want a curated "best of" Reddit experience

**Tip:** These are great starting points if you're new to Reddit or just browsing casually.

## Commands

### `reddit frontpage`

Browse the Reddit frontpage.

```bash
reddit frontpage
reddit frontpage --sort hot
reddit frontpage --sort top --period month --limit 50
```

### `reddit home`

Same as `frontpage`.

### `reddit best`

Browse top posts of all time.

```bash
reddit best
reddit best --period year --limit 100
```

## Options

| Option | Description |
|--------|-------------|
| `--sort` | Sort by: hot, new, top, rising, controversial, gilded (default: hot) |
| `--limit` | Number of posts: 1-100 (default: 25) |
| `--period` | Time range: day, week, month, year, all |
| `--after` | Get posts after this ID |
| `--before` | Get posts before this ID |
| `--format` | Output format: display, csv, sql, json, xlsx |
| `--output` | Write to file instead of stdout |

## Examples

```bash
# Hot posts
reddit frontpage

# Top posts this month
reddit frontpage --sort top --period month

# Top 50 rising posts
reddit frontpage --sort rising --limit 50

# All-time best
reddit best --period all
```
