# isolated_filesystem()

**Date:** 2026-03-31

## Overview

Use `isolated_filesystem()` to test file operations without polluting the real filesystem. Files created during the test are automatically cleaned up.

## Usage

```python
def test_export_creates_file():
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["export", "--format", "csv"])
        assert result.exit_code == 0
        assert Path("export.csv").exists()
        # File is automatically cleaned up after the test
```

## Key Benefits

- No file system pollution
- Automatic cleanup (even if test fails)
- Deterministic file paths for assertions

## Examples

### Testing File Export

```python
def test_export_creates_file():
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["export", "--format", "csv"])
        assert result.exit_code == 0
        assert Path("export.csv").exists()
```

### Testing File Import

```python
def test_import_reads_file():
    with runner.isolated_filesystem():
        # Create a test file first
        Path("data.json").write_text('{"name": "test"}')
        result = runner.invoke(app, ["import", "data.json"])
        assert result.exit_code == 0
        assert "Imported: test" in result.output
```

### Testing File Not Found

```python
def test_file_not_found():
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["import", "nonexistent.json"])
        assert result.exit_code != 0
        assert "not found" in result.output.lower()
```

## Configuration

By default, `CliRunner(isolated_filesystem=True)` is set. To disable:

```python
runner = CliRunner(isolated_filesystem=False)
```

## See Also

- [file-operations.md](file-operations.md) - Testing file operations
