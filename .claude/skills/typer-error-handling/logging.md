# Logging Integration with stderr

Use stderr for logging to separate it from normal output.

## Basic Logging to stderr

```python
import logging
import sys

# Handler for stderr
stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.WARNING)
stderr_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))

logger = logging.getLogger(__name__)
logger.addHandler(stderr_handler)
logger.setLevel(logging.WARNING)
```

## Complete Logging Example

```python
import logging
import sys

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)

@app.command()
def risky_operation(config_path: str):
    try:
        config = load_config(config_path)
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        raise typer.Exit(f"Error: Config '{config_path}' not found", code=2, err=True)
    except PermissionError:
        logger.error(f"Permission denied: {config_path}")
        raise typer.Exit(f"Error: Cannot read '{config_path}'", code=1, err=True)
```

## Structured Logging

```python
import logging
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj)

# Production logging with JSON
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(JsonFormatter())
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
```

## Logging Best Practices

1. **Log to stderr, not stdout** - Errors should be separated from normal output
2. **Use appropriate log levels** - ERROR for failures, WARNING for degraded behavior, INFO for progress
3. **Don't expose sensitive data in logs** - Scrub credentials, tokens, etc.
4. **Include context in log messages** - File paths, IDs, relevant parameters

```python
# Good - includes context
logger.error(f"Failed to process file: {path}, error: {e}")

# Bad - no context
logger.error("Failed to process file")
```

## Combining Logging with typer.Exit

```python
@app.command()
def process_files(files: list[str]):
    for path in files:
        try:
            process(path)
            logger.info(f"Processed: {path}")
        except PermissionError as e:
            logger.error(f"Permission denied: {path}")
            typer.echo(f"Error: Cannot read '{path}'", err=True)
            raise typer.Exit(code=2)
        except Exception as e:
            logger.exception(f"Unexpected error processing: {path}")
            typer.echo(f"Error processing '{path}': {e}", err=True)
            raise typer.Exit(code=1)
```

## Environment-Aware Logging

```python
import os

def setup_logging(verbose: bool = False):
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)]
    )

@app.command()
def main(verbose: bool = False):
    setup_logging(verbose)
    # ...
```

See also:
- [secho-style.md](secho-style.md) - For typer.secho() styling
- [context-managers.md](context-managers.md) - For resource cleanup
