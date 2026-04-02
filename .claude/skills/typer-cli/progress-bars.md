# Progress Bars

Typer provides progress bar functionality for long-running operations.

## Progress Bar with `typer.track()`

Use `typer.track()` to display progress for iterable operations:

```python
import typer

app = typer.Typer()

def fetch_items():
    """Generator that yields items."""
    for i in range(100):
        yield f"item_{i}"

@app.command()
def process():
    """Process items with progress bar."""
    for item in typer.track(fetch_items(), description="Processing..."):
        # Simulate work
        pass
    typer.echo("Done!")

# Shows: Processing... |███████░░░░░░░░░| 35%
```

## Progress Bar for Lists

```python
import typer

app = typer.Typer()

@app.command()
def install():
    """Install packages with progress."""
    packages = ["numpy", "pandas", "matplotlib", "scikit-learn", "tensorflow"]

    for package in typer.track(packages, description="Installing"):
        # Simulate installation
        import time
        time.sleep(0.5)
    typer.echo("All packages installed!")
```

## Manual Progress Bar

```python
import typer

app = typer.Typer()

@app.command()
def download():
    """Download with manual progress."""
    total = 100

    with typer.progressbar(range(total), label="Downloading") as bar:
        for i in bar:
            # Simulate download chunk
            import time
            time.sleep(0.05)

    typer.echo("Download complete!")
```

## Progress Bar with Custom Length

```python
import typer

app = typer.Typer()

@app.command()
def process_files():
    """Process files with known total."""
    files = ["a.txt", "b.txt", "c.txt", "d.txt"]

    with typer.progressbar(files, label="Processing files", length=len(files)) as bar:
        for file in bar:
            # Process file
            import time
            time.sleep(0.3)

    typer.echo(f"Processed {len(files)} files")
```

## Spinner with Rich Console

Use Rich's `console.status()` for spinner animations:

```python
from rich.console import Console
import typer

app = typer.Typer()
console = Console()

@app.command()
def long_task():
    """Run a task with custom spinner."""
    import time

    with console.status("[bold green]Processing your request...", spinner="dots"):
        time.sleep(3)
    typer.echo("Task complete!")

# Spinner styles: dots, dot2, line, pulse, moon, material
```

## Multiple Spinners in Sequence

```python
from rich.console import Console
import typer

app = typer.Typer()
console = Console()

@app.command()
def setup():
    """Setup with multiple stages."""
    stages = [
        ("Initializing...", "done"),
        ("Configuring...", "done"),
        ("Finalizing...", "done"),
    ]

    for stage_name, _ in stages:
        with console.status(f"[bold blue]{stage_name}", spinner="aesthetic"):
            import time
            time.sleep(0.5)

    console.print("[bold green]Setup complete![/bold green]")
```

## Progress Bar with Rich

```python
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
import typer

app = typer.Typer()
console = Console()

@app.command()
def batch_process():
    """Batch process with rich progress."""
    tasks = ["task1", "task2", "task3", "task4", "task5"]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Processing...", total=len(tasks))

        for i, task_name in enumerate(tasks):
            import time
            time.sleep(0.5)
            progress.update(task, advance=1, description=f"Processing {task_name}")

    console.print("[bold green]All tasks complete![/bold green]")
```

## Multi-Stage Progress with Status

```python
from rich.console import Console
import typer

app = typer.Typer()
console = Console()

@app.command()
def deploy():
    """Multi-stage deployment with Rich."""
    stages = [
        ("Validating configuration...", "config validated"),
        ("Building image...", "image built"),
        ("Running tests...", "tests passed"),
        ("Deploying to production...", "deployed successfully"),
    ]

    for stage_description, success_message in stages:
        with console.status(f"[bold blue]{stage_description}") as status:
            import time
            time.sleep(1.5)
        console.print(f"[green]✓[/green] {success_message}")

    console.print("")
    console.print("[bold green]Deployment complete![/bold green]")
```

## Indeterminate Progress (Spinner)

For operations with unknown duration:

```python
from rich.console import Console
import typer

app = typer.Typer()
console = Console()

@app.command()
def fetch_data():
    """Fetch data with indeterminate progress."""
    with console.status("[bold yellow]Fetching data from API...", spinner="moon"):
        import time
        time.sleep(3)
    console.print("[green]Data fetched successfully![/green]")

@app.command()
def building():
    """Build with indeterminate progress."""
    with console.status("[bold cyan]Building project...", spinner="dots12"):
        import time
        time.sleep(4)
    console.print("[green]Build complete![/green]")
```

## Progress Bar with Download Simulation

```python
import typer

app = typer.Typer()

@app.command()
def download_file():
    """Download simulation with progress."""
    filename = "large_file.zip"
    total_size = 100

    with typer.progressbar(range(total_size), label=f"Downloading {filename}") as bar:
        for chunk in bar:
            # Simulate download chunk
            import time
            time.sleep(0.1)

    typer.echo(f"Downloaded {filename}")
```

## Key Points

- `typer.track()` wraps iterables with progress display
- `typer.progressbar()` provides manual progress control
- Use `Rich console.status()` for spinner animations
- Available spinner styles: dots, dot2, line, pulse, moon, material, aesthetic, dots12
- Progress bars work well with file operations, downloads, and batch processing
- Rich provides more customizable progress components when needed
- Progress is automatically hidden when output is not a terminal
