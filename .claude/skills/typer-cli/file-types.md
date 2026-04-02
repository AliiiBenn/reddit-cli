# File Types

Typer provides specialized file type handlers for text and binary files.

## FileTextRead - Read Text Files

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def read(
    file: Annotated[typer.FileText, typer.Argument()],
):
    """Read a text file."""
    content = file.read()
    typer.echo(f"Content:\n{content}")

# python main.py read file.txt
```

## FileTextWrite - Write Text Files

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def save(
    output: Annotated[typer.FileTextWrite, typer.Option("--output", "-o")],
    content: str,
):
    """Save content to file."""
    output.write(content)
    typer.echo(f"Saved to {output.name}")

# python main.py save --output result.txt "Hello World"
# Writes "Hello World" to result.txt
```

## FileBinaryRead - Read Binary Files

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def analyze(
    input_file: Annotated[typer.FileBinaryRead, typer.Argument()],
):
    """Analyze binary file."""
    data = input_file.read()
    typer.echo(f"Read {len(data)} bytes from {input_file.name}")
    typer.echo(f"First bytes: {data[:20]!r}")
```

## FileBinaryWrite - Write Binary Files

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def create_png(
    output: Annotated[typer.FileBinaryWrite, typer.Option("--output", "-o")],
):
    """Create a minimal PNG file."""
    # Minimal PNG signature
    png_data = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
    output.write(png_data)
    typer.echo(f"PNG written to {output.name}")
```

## Combining FileTextWrite with allow_dash

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def process(
    input_file: Annotated[typer.FileText, typer.Argument()],
    output: Annotated[typer.FileTextWrite, typer.Option("--output", "-o", allow_dash=True)],
):
    """Process text file and write to output."""
    content = input_file.read()

    # Simple transformation - uppercase
    transformed = content.upper()

    if str(output) == "-":
        typer.echo(transformed)
    else:
        output.write(transformed)
        typer.echo(f"Written to {output.name}")

# python main.py process input.txt --output -      # Output to stdout
# python main.py process input.txt --output out.txt # Output to file
```

## Lazy File Reading

For large files, read line by line:

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def wc(
    file: Annotated[typer.FileText, typer.Argument()],
):
    """Count lines, words, and characters."""
    lines = 0
    words = 0
    chars = 0

    for line in file:  # Lazy reading line by line
        lines += 1
        words += len(line.split())
        chars += len(line)

    typer.echo(f"Lines: {lines}")
    typer.echo(f"Words: {words}")
    typer.echo(f"Chars: {chars}")
```

## Processing Binary Data

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def checksum(
    file: Annotated[typer.FileBinaryRead, typer.Argument()],
):
    """Calculate checksum of a binary file."""
    import hashlib

    hasher = hashlib.sha256()
    for chunk in iter(lambda: file.read(8192), b""):
        hasher.update(chunk)

    typer.echo(f"File: {file.name}")
    typer.echo(f"SHA256: {hasher.hexdigest()}")
```

## File Object Attributes

File objects have standard attributes:

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def info(
    file: Annotated[typer.FileText, typer.Argument()],
):
    """Show file information."""
    typer.echo(f"Name: {file.name}")
    typer.echo(f"Mode: {file.mode}")
    typer.echo(f"Encoding: {file.encoding}")

# Note: name, mode, and encoding are available
```

## Stdin/Stdout as Files

```python
import typer

app = typer.Typer()

@app.command()
def cat():
    """Read from stdin and write to stdout."""
    content = typer.get_text_stream("stdin").read()
    typer.echo(content, nl=False)

@app.command()
def pipeline():
    """Process stdin line by line."""
    stdin = typer.get_text_stream("stdin")
    for line in stdin:
        processed = line.upper()
        typer.echo(processed, nl=False)
```

## Multiple File Inputs

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def merge(
    files: Annotated[list[typer.FileText], typer.Argument()],
):
    """Merge multiple files."""
    for file in files:
        typer.echo(f"--- {file.name} ---")
        typer.echo(file.read())
        typer.echo("")

# python main.py merge file1.txt file2.txt file3.txt
```

## File Type Summary

| Type | Purpose | Use Case |
|------|---------|----------|
| `typer.FileText` | Read text | Reading text files |
| `typer.FileTextWrite` | Write text | Writing text files |
| `typer.FileBinary` | Read binary | Reading binary files |
| `typer.FileBinaryWrite` | Write binary | Writing binary files |

## Key Points

- `typer.FileText` opens files in text mode for reading
- `typer.FileTextWrite` opens files in text mode for writing
- `typer.FileBinaryRead` opens files in binary mode for reading
- `typer.FileBinaryWrite` opens files in binary mode for writing
- Use `allow_dash=True` with options to accept `-` for stdin/stdout
- File objects have `.name`, `.mode`, and `.encoding` attributes
- Lazy reading with `for line in file` is efficient for large files
- `typer.get_text_stream("stdin")` reads from stdin directly
