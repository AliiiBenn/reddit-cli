# File Operations Testing

**Date:** 2026-03-31

## Testing File Operations

Always use `isolated_filesystem()` for testing file operations:

```python
from pathlib import Path

def test_export_creates_file():
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["export", "--format", "csv"])
        assert result.exit_code == 0
        assert Path("export.csv").exists()
```

## Creating Test Files

```python
def test_import_reads_file():
    with runner.isolated_filesystem():
        # Create a test file first
        Path("data.json").write_text('{"name": "test"}')
        result = runner.invoke(app, ["import", "data.json"])
        assert result.exit_code == 0
        assert "Imported: test" in result.output
```

## Testing File Not Found

```python
def test_file_not_found():
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["import", "nonexistent.json"])
        assert result.exit_code != 0
        assert "not found" in result.output.lower()
```

## Testing with Config Files

```python
def test_config_loading():
    with runner.isolated_filesystem():
        # Create a config file
        Path("config.yaml").write_text("key: value\n")
        result = runner.invoke(app, ["load-config", "--file", "config.yaml"])
        assert result.exit_code == 0
        assert "Config loaded" in result.output
```

## See Also

- [isolated-filesystem.md](isolated-filesystem.md) - isolated_filesystem() usage
