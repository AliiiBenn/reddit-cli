# Post Command

View a single post by its ID.

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

## Related Commands

| Command | Description |
|---------|-------------|
| `reddit comments <post_id>` | View comments for a post |
| `reddit browse <subreddit>` | List posts from a subreddit |
