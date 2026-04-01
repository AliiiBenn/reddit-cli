# CLI Commands

## Navigation

```
reddit                      # Frontpage (hot posts)
reddit frontpage            # Alias for frontpage
reddit home                 # Alias for frontpage
reddit best                 # Best posts overall
```

## Subreddit Discovery

```
reddit subreddits                     # List popular subreddits
reddit subreddits --sort subscribers  # Sort by subscribers
reddit subreddits --sort active       # Sort by active users
reddit subreddit <name>               # Get subreddit info
reddit subreddit <name> --details     # Full subreddit details
reddit subreddit <name> --rules       # Get subreddit rules
reddit subreddit <name> --moderators  # List moderators
reddit subreddit <name> --related     # Related subreddits
```

## Posts Browsing

```
reddit browse <subreddit>                    # List posts (default: hot)
reddit browse <subreddit> --sort hot          # Hot posts
reddit browse <subreddit> --sort new          # New posts
reddit browse <subreddit> --sort top          # Top posts (all time)
reddit browse <subreddit> --sort top --period day      # Top of the day
reddit browse <subreddit> --sort top --period week     # Top of the week
reddit browse <subreddit> --sort top --period month    # Top of the month
reddit browse <subreddit> --sort top --period year     # Top of the year
reddit browse <subreddit> --sort rising      # Rising posts
reddit browse <subreddit> --sort controversial       # Controversial
reddit browse <subreddit> --sort gilded      # Gilded posts
reddit browse <subreddit> --limit <n>        # Limit results (default: 25)
reddit browse <subreddit> --after <id>       # Pagination cursor
reddit browse <subreddit> --before <id>      # Pagination cursor
```

## Post Details

```
reddit view <post_id>              # View post with comments
reddit view <url>                  # View post from URL
reddit post <post_id>              # Alias for view
reddit post <post_id> --full       # Full post metadata
reddit post <post_id> --stats      # Post statistics only
reddit post <post_id> --meta       # Post metadata only
```

## Comments

```
reddit comments <post_id>          # View comments only
reddit comments <post_id> --thread # Threaded view
reddit comments <post_id> --flat   # Flat view
reddit comments <post_id> --depth <n>     # Max depth (default: unlimited)
reddit comments <post_id> --sort confidence  # Best comments
reddit comments <post_id> --sort top        # Top comments
reddit comments <post_id> --sort new        # New comments
reddit comments <post_id> --sort old        # Old comments
reddit comments <post_id> --sort controversial      # Controversial
reddit comments <post_id> --sort qa         # Q&A mode
```

## Comment Details

```
reddit comment <comment_id>                 # Single comment details
reddit comment <comment_id> --replies      # Include replies
reddit comment <comment_id> --author       # Comment author info
```
