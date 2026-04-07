# Project: better-reddit-cli

A command-line tool for browsing Reddit without requiring an API key.

## Release Process

### Prerequisites
- PyPI token must be available in GitHub Secrets (`PYPI_API_TOKEN`)
- Version in `pyproject.toml` must match the tag version

### Steps to Release

1. **Update version in pyproject.toml**:
   ```bash
   # Edit pyproject.toml and update version = "X.Y.Z"
   # Both occurrences (lines 3 and 36)
   ```

2. **Create a new branch for the version bump**:
   ```bash
   git checkout -b release/X.Y.Z
   git add pyproject.toml
   git commit -m "chore: bump version to X.Y.Z"
   git push -u origin release/X.Y.Z
   ```

3. **Create a Pull Request and merge** (branch protection requires PR)

4. **Create a GitHub Release**:
   ```bash
   gh release create vX.Y.Z --title "Release X.Y.Z" --notes "Release notes"
   ```

5. **Create and push the tag AFTER the version bump is on main**:
   ```bash
   git checkout main
   git pull
   git tag -a vX.Y.Z -m "Release X.Y.Z"
   git push origin vX.Y.Z
   ```

   This triggers the `release.yml` workflow which validates that the tag version matches `pyproject.toml`.

### Important Notes

- **The release workflow (`release.yml`) validates that tag version = pyproject.toml version**
- Tag must be pushed AFTER the version commit is merged to main
- If versions don't match, the workflow fails with: `Tag version 'vX.Y.Z' does not match pyproject.toml version 'A.B.C'`

### CI/CD

| Workflow | Trigger | Description |
|----------|---------|-------------|
| `test.yml` | push/PR | Runs pytest on Python 3.12, 3.13, 3.14 |
| `ruff.yml` | push/PR | Linting with ruff |
| `mypy.yml` | push/PR | Type checking with mypy |
| `release.yml` | tag push | Builds and publishes to PyPI |

### Local Development

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest tests/ -x -q

# Run linter
uv run ruff check .

# Run type checker
uv run mypy reddit_cli

# Build package
uv build

# Publish to PyPI (requires token)
uv publish --token $PYPI_API_TOKEN
```

### Project Structure

```
reddit_cli/
  __init__.py      # Main Typer app
  commands/        # CLI command modules
  reddit/          # Reddit API clients
  errors.py        # Error handling
  export.py        # SQL/CSV export
  xlsx_export.py   # XLSX export
  ui.py            # Rich UI helpers
  cache.py         # File-based caching
  logging.py       # Structured logging
```
