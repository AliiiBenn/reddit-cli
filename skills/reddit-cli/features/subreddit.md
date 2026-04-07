# Subreddit Commands

Get subreddit information and browse subreddit lists.

## When to Use

Use `reddit subreddit <name>` when you:
- Want to learn about a specific community
- Need to see subreddit rules before posting
- Want to check subscriber count or activity level

Use `reddit subreddits` (no argument) when you:
- Want to discover new communities
- Are looking for popular subreddits to join
- Want to find subreddits related to a topic
- Need to browse Reddit Gold or default subreddits

**Tip:** If you know the topic but not the subreddit name, try `reddit subreddits --search <keyword>`.

## Commands

### Get subreddit info

```bash
reddit subreddit <name>
reddit subreddit python
reddit subreddit r/programming --rules
```

### List subreddits

```bash
reddit subreddits
reddit subreddits --sort subscribers --limit 50
reddit subreddits --search python
reddit subreddits --new
reddit subreddits --gold
reddit subreddits --default
```

## Subreddit Info

Shows:
- Display name
- Title
- Subscriber count
- Active users
- Description

### With `--rules`

Displays the subreddit's rules instead of info.

## List Options

| Option | Description |
|--------|-------------|
| `--sort` | Sort by: subscribers, active (default: subscribers) |
| `--limit` | Number of results: 1-100 (default: 25) |
| `--search` | Search subreddits by keyword |
| `--new` | List newly created subreddits |
| `--gold` | List Reddit Gold subreddits |
| `--default` | List default subreddits |
| `--format` | Output format: display, csv, sql, json, xlsx |
| `--output` | Write to file instead of stdout |

## Examples

```bash
# Get subreddit info
reddit subreddit python

# Show rules
reddit subreddit javascript --rules

# Most popular subreddits
reddit subreddits --sort subscribers --limit 50

# Most active subreddits
reddit subreddits --sort active

# Search for subreddits
reddit subreddits --search python --limit 10

# Recently created subreddits
reddit subreddits --new

# Default subreddits
reddit subreddits --default
```
