# Common Mistakes Checklist

**Date:** 2026-03-31

## Must Have (E2E Minimum)

- [ ] Every command has at least one test
- [ ] Every test checks `exit_code`
- [ ] Every test verifies output
- [ ] Error cases return non-zero exit codes

## Should Have (Good Coverage)

- [ ] All argument combinations tested
- [ ] All options/flags tested
- [ ] Interactive prompts have `input=` with complete sequences
- [ ] Edge cases covered (empty input, invalid values)

## Nice to Have (Excellent)

- [ ] Subcommands tested independently
- [ ] stderr checked separately from stdout
- [ ] Environment variables tested
- [ ] Specific exit code values verified
- [ ] Help text verified with `--help`

## Testing File Structure

```
tests/
├── test_main.py        # Tests for main app commands
├── test_users.py       # Tests for user-related commands
└── test_output.py     # Tests for output formatting

# Test file naming
test_*.py               # pytest auto-discovery
*_test.py               # Alternative naming
```

## Test Function Naming

```
test_<command>_<scenario>
test_create_user_success
test_create_user_missing_name
test_create_user_invalid_email
```

## See Also

- [anti-patterns.md](anti-patterns.md) - Anti-patterns to avoid
- [basic-testing.md](basic-testing.md) - Basic testing patterns
