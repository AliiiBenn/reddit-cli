# Path Handling

Typer provides specialized path handling with validation and conversion options.

## Path Type with `typer.Path`

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def read_file(
    path: Annotated[typer.Path, typer.Argument()],
):
    """Read a file."""
    with open(path) as f:
        typer.echo(f.read())
```

## Path Exists Validation

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def process(
    config: Annotated[typer.Path(exists=True), typer.Option("--config")],
):
    """Process a config file that must exist."""
    typer.echo(f"Processing {config}")

# python main.py --config missing.txt
# Error: Invalid value for '--config': File 'missing.txt' does not exist.
```

## resolve_path - Resolve Symlinks

Automatically resolve symbolic links in paths:

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def read_config(
    config: Annotated[typer.Path(exists=True, resolve_path=True)],
):
    """Read config file (symlinks resolved)."""
    typer.echo(f"Config path: {config.resolve()}")

# If /etc/myapp is a symlink to /home/user/.myapp,
# resolve_path=True returns the actual resolved path
```

## allow_dash - Accept stdin/stdout

Allow `-` to represent stdin/stdout:

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def process(
    input_file: Annotated[typer.Path(allow_dash=True)],
):
    """Process a file or stdin."""
    if str(input_file) == "-":
        content = typer.get_text_stream("stdin")
        typer.echo(f"Reading from stdin: {len(content)} bytes")
    else:
        typer.echo(f"Processing {input_file}")

@app.command()
def output(
    output_file: Annotated[typer.FileTextWrite, typer.Option("--output", "-o", allow_dash=True)],
):
    """Write to file or stdout."""
    if str(output_file) == "-":
        typer.echo("Writing to stdout")
    else:
        output_file.write("Content")
        typer.echo(f"Written to {output_file.name}")

# python main.py process -           # Read from stdin
# python main.py process input.txt   # Read from file
```

## path_type - Control Path Type

Specify whether paths are returned as strings or Path objects:

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def list_files(
    path: Annotated[typer.Path(path_type=str)] = ".",
):
    """List files as strings."""
    import os
    for item in os.listdir(path):
        typer.echo(item)

@app.command()
def find_files(
    path: Annotated[typer.Path(path_type=None)] = ".",
):
    """Get raw path (string or Path based on input)."""
    import os
    for item in os.listdir(path):
        typer.echo(f"Found: {item}")

# path_type=str - Always returns string
# path_type=None - Returns whatever user provided
# Default - Returns PosixPath on Unix, WindowsPath on Windows
```

## Path with File Type Check

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def compile(
    source: Annotated[typer.Path(exists=True), typer.Argument(help="Source .py file")],
    output: Annotated[typer.Path(), typer.Option("--output", "-o", help="Output .pyc file")],
):
    """Compile a Python file."""
    if not str(source).endswith(".py"):
        typer.echo("Warning: Source file does not have .py extension", err=True)
    typer.echo(f"Compiling {source} to {output}")
```

## Path with Permissions Check

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def execute(
    script: Annotated[typer.Path(exists=True), typer.Argument(help="Script to execute")],
):
    """Execute a script file."""
    import os
    import stat

    st = os.stat(script)
    is_executable = bool(st.st_mode & stat.S_IXUSR)

    if not is_executable:
        typer.echo(f"Making {script} executable...")
        os.chmod(script, st.st_mode | stat.S_IXUSR)

    typer.echo(f"Executing {script}")
```

## Combining Path Options

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def read_config(
    config: Annotated[
        typer.Path,
        typer.Option(
            "--config",
            exists=True,
            resolve_path=True,
            path_type=str,
        ),
    ] = "config.yaml",
):
    """Read config with full path options."""
    import os
    resolved = os.path.abspath(config)
    typer.echo(f"Config: {resolved}")
    typer.echo(f"Exists: {os.path.exists(config)}")
    typer.echo(f"Type: {type(config)}")
```

## Working with Path Objects

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def analyze(
    directory: Annotated[typer.Path(exists=True), typer.Argument()],
):
    """Analyze a directory."""
    import os

    # Path objects have all the standard methods
    typer.echo(f"Name: {directory.name}")
    typer.echo(f"Parent: {directory.parent}")
    typer.echo(f"Is file: {directory.is_file()}")
    typer.echo(f"Is dir: {directory.is_dir()}")

    # List contents
    for item in directory.iterdir():
        typer.echo(f"  {item.name}")
```

## Path Completion

Path arguments automatically get file/directory completion:

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def open_file(
    file: Annotated[typer.Path, typer.Argument()],
):
    """Open a file."""
    typer.echo(f"Opening {file}")

# Tab completion automatically provides file paths
```

## Key Points

- `typer.Path` provides path handling with validation
- `exists=True` validates that the path exists
- `resolve_path=True` resolves symbolic links
- `allow_dash=True` accepts `-` for stdin/stdout
- `path_type=str` returns string, `path_type=None` returns original type
- Default returns `pathlib.Path` (PosixPath or WindowsPath based on OS)
- Path objects have `.resolve()`, `.exists()`, `.is_file()`, `.is_dir()`, etc.
- Path completion is automatic with `typer.Path`
