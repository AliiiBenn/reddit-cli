# Error Handling

What to expect when something goes wrong.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Something went wrong (network, API error) |
| 2 | Invalid command or option |
| 130 | Interrupted (Ctrl+C) |

## Common Errors

### Connection Issues

```
Error: Connection timed out. Please check your internet connection and try again.
```

### API Errors

| Error | Meaning |
|-------|---------|
| `400 Bad request` | Check your command options |
| `401/403 Authentication required` | Feature requires login (not supported) |
| `404 Not found` | Post or subreddit doesn't exist |
| `429 Rate limited` | Wait a moment and try again |
| `500/503 Server error` | Reddit is having issues, try later |

## Validation Errors

```
Error: Invalid value 'invalid' for --sort. Valid values are: hot, new, top
```

This means you used an invalid option value. Check the valid options for the command.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection timed out | Check internet connection |
| 429 Rate limited | Wait 30 seconds and retry |
| 404 Not found | Verify the post/subreddit ID or name |
| 403 Auth required | Feature not available without OAuth |
| All commands fail | Check internet connection, try again later |
