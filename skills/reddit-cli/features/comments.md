# Comments Commands

View comments for a post or view a specific comment.

## When to Use

Use `reddit comments <post_id>` when you:
- Want to read the discussion on a specific post
- Need to see community reactions and opinions
- Want to find the best comments (sort by top/confidence)

Use `reddit comment <post_id> <comment_id>` when you:
- Want to reference a specific comment
- Need to see a comment's replies
- Are building a discussion thread analysis

**Note:** Comments are fetched with a default sort of "confidence" (best first).

## Commands

### View all comments

```bash
reddit comments <post_id>
reddit comments <post_id> --sort top --depth 3
```

### View a single comment

```bash
reddit comment <post_id> <comment_id>
reddit comment <post_id> <comment_id> --replies
```

## Options

### Comments Options

| Option | Description |
|--------|-------------|
| `--sort` | Sort by: confidence, top, new, old, controversial, qa (default: confidence) |
| `--depth` | Maximum nesting depth (1 = top-level only) |
| `--format` | Output format: display, csv, sql, json, xlsx |
| `--output` | Write to file instead of stdout |

### Single Comment Options

| Option | Description |
|--------|-------------|
| `--replies` | Include nested replies |
| `--format` | Output format: display, csv, sql, json, xlsx |
| `--output` | Write to file instead of stdout |

## Sort Options

| Sort | Description |
|------|-------------|
| `confidence` | Best comments first (default) |
| `top` | Top scored |
| `new` | Most recent |
| `old` | Oldest first |
| `controversial` | Most controversial |
| `qa` | Q&A format |

## Examples

```bash
# View all comments (best first)
reddit comments t3_abc123

# Top comments only, no nesting
reddit comments abc123 --sort top --depth 1

# Newest comments
reddit comments t3_abc123 --sort new

# View a specific comment with replies
reddit comment t3_abc123 t1_def456 --replies
```

## Comment ID Format

Comment IDs are prefixed with `t1_`. The CLI accepts both:
- `t1_abc123` (full ID)
- `abc123` (short ID)

## Related Commands

| Command | Description |
|---------|-------------|
| `reddit post <post_id>` | View the post itself |
