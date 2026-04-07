# Post Command

View a single post by its ID.

## When to Use

Use `reddit post <post_id>` when you:
- Have a specific post link or ID you want to read
- Found a post through search or a shared link
- Want to see full post details before reading comments
- Need post metadata (score, author, subreddit, URL)

**Common sources of post IDs:**
- Shared Reddit links (the last part of the URL)
- Search results
- Comments that reference other posts

## Command

```bash
reddit post <post_id>
reddit post t3_abc123
```

## Examples

```bash
# View a post (t3_ prefix is optional)
reddit post abc123def
reddit post t3_abc123def
```

## Output

Shows:
- Title
- Score
- Number of comments
- Author
- Subreddit
- URL
- Permalink
- Post body text (if self-post)

## Post ID Format

Reddit post IDs are prefixed with `t3_`. The CLI accepts both:
- `t3_abc123def` (full ID)
- `abc123def` (short ID)

## Options

| Option | Description |
|--------|-------------|
| `--format` | Output format: display, csv, sql, json, xlsx |
| `--output` | Write to file instead of stdout |

## Related Commands

| Command | Description |
|---------|-------------|
| `reddit comments <post_id>` | View comments for a post |
| `reddit browse <subreddit>` | List posts from a subreddit |
