# Typer CLI Skill — Usage Example

This example demonstrates a typical interaction with the Typer CLI skill, showing the expected input scenario and the resulting guidance/output.

## Scenario: User Wants to Build a Project Management CLI

**User Request:**
> "I want to create a CLI for managing projects. It should have commands to create projects, list them, and delete them. I also need to support subcommands for adding tasks to projects."

---

## Skill Invocation Analysis

**Relevant Skill:** `typer-cli`

**Topics Triggered:**
- App creation (`typer.Typer()`)
- Commands (`@app.command()`)
- Subcommands (`add_typer()`)
- Arguments and options
- Exit codes

---

## Example: Project Management CLI Structure

### Input Files (Before)

The user has the following project structure:

```
my_project/
├── cli/
│   ├── __init__.py
│   └── main.py
└── pyproject.toml
```

### Existing `cli/main.py`:

```python
import typer

app = typer.Typer()

@app.command()
def create(name: str):
    """Create a new project."""
    print(f"Creating project: {name}")

if __name__ == "__main__":
    app()
```

### User's Request in Detail:
1. Add a `list` command to show all projects
2. Add a `delete` command with confirmation prompt
3. Create a `tasks` subcommand group for managing tasks within projects
4. Add a `--verbose` flag that works across all commands

---

## Typer CLI Skill Guidance

### 1. Recommended Structure

The skill recommends separating concerns using a multi-file structure:

```
cli/
├── __init__.py
├── main.py          # Main app with global options
├── projects.py      # Project commands
└── tasks.py         # Task subcommands
```

### 2. Refactored Code

**`cli/projects.py`** — Project commands module:

```python
import typer

app = typer.Typer()

@app.command()
def create(
    name: str,
    description: str = "",
):
    """Create a new project."""
    typer.echo(f"Creating project: {name}")
    if description:
        typer.echo(f"Description: {description}")

@app.command()
def list():
    """List all projects."""
    projects = [
        {"name": "alpha", "tasks": 5},
        {"name": "beta", "tasks": 3},
    ]
    for project in projects:
        typer.echo(f"  - {project['name']} ({project['tasks']} tasks)")

@app.command()
def delete(
    name: str,
    force: bool = typer.Option(False, prompt=True, help="Skip confirmation"),
):
    """Delete a project."""
    if not force:
        typer.echo("Deletion cancelled")
        raise typer.Abort()
    typer.echo(f"Deleted project: {name}")
```

**`cli/tasks.py`** — Task subcommands:

```python
import typer

app = typer.Typer()

@app.command()
def add(
    project: str,
    task: str,
    priority: str = typer.Option("medium", "--priority", "-p"),
):
    """Add a task to a project."""
    typer.echo(f"Adding task '{task}' to project '{project}' (priority: {priority})")

@app.command()
def list_cmd(project: str):
    """List tasks in a project."""
    typer.echo(f"Tasks in {project}:")
    typer.echo("  - Design API (high)")
    typer.echo("  - Write tests (medium)")

@app.command()
def complete(project: str, task: str):
    """Mark a task as complete."""
    typer.echo(f"Marked '{task}' as complete in {project}")
```

**`cli/main.py`** — Main app with subcommand composition:

```python
import typer
import projects
import tasks

app = typer.Typer()
state = {"verbose": False}

@app.callback()
def main(verbose: bool = False):
    """Manage projects and tasks."""
    state["verbose"] = verbose

app.add_typer(projects.app, name="project")
app.add_typer(tasks.app, name="task")

if __name__ == "__main__":
    app()
```

### 3. Command Tree

```
cli.py
├── project
│   ├── create
│   ├── list
│   └── delete
└── task
    ├── add
    ├── list
    └── complete
```

### 4. Usage Examples

```bash
# Create a project
$ python cli.py project create myapp --description "My awesome app"
Creating project: myapp
Description: My awesome app

# List all projects
$ python cli.py project list
  - alpha (5 tasks)
  - beta (3 tasks)

# Delete with prompt
$ python cli.py project delete myapp
Are you sure? [y/n]: n
Deletion cancelled

# Delete with force flag
$ python cli.py project delete myapp --force
Deleted project: myapp

# Add task with priority
$ python cli.py task add myapp "Write docs" --priority high
Adding task 'Write docs' to project 'myapp' (priority: high)

# Verbose mode
$ python cli.py --verbose project create myapp
DEBUG: Loading projects database
Creating project: myapp
DEBUG: Project created successfully
```

### 5. Help Output

```bash
$ python cli.py --help
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

  Manage projects and tasks.

Options:
  --verbose / --no-verbose
  --help                    Show this message and exit.

Commands:
  project
  task

$ python cli.py project --help
Usage: cli.py project [OPTIONS] COMMAND [ARGS]...

Options:
  --help                    Show this message and exit.

Commands:
  create
  delete
  list

$ python cli.py project create --help
Usage: cli.py project create [OPTIONS] NAME

  Create a new project.

Arguments:
  NAME    [required]

Options:
  --description TEXT
  --help                Show this message and exit.
```

---

## Key Patterns Demonstrated

### Pattern 1: Subcommand Composition
```python
app.add_typer(projects.app, name="project")
app.add_typer(tasks.app, name="task")
```

### Pattern 2: Confirmation Prompt
```python
force: bool = typer.Option(False, prompt=True, help="Skip confirmation"),
```

### Pattern 3: App-level State with Callback
```python
@app.callback()
def main(verbose: bool = False):
    """Manage projects and tasks."""
    state["verbose"] = verbose
```

### Pattern 4: Abort on Cancellation
```python
if not force:
    typer.echo("Deletion cancelled")
    raise typer.Abort()
```

---

## Testing This CLI

### Example Test File

```python
# tests/test_cli.py
from typer.testing import CliRunner
from cli.main import app

runner = CliRunner()

def test_project_create():
    result = runner.invoke(app, ["project", "create", "testproj"])
    assert result.exit_code == 0
    assert "Creating project: testproj" in result.output

def test_project_list():
    result = runner.invoke(app, ["project", "list"])
    assert result.exit_code == 0
    assert "-" in result.output

def test_project_delete_cancelled():
    result = runner.invoke(app, ["project", "delete", "testproj"], input="n\n")
    assert result.exit_code == 1
    assert "cancelled" in result.output.lower()

def test_project_delete_force():
    result = runner.invoke(app, ["project", "delete", "testproj", "--force"])
    assert result.exit_code == 0
    assert "Deleted" in result.output

def test_task_add():
    result = runner.invoke(app, ["task", "add", "proj1", "mytask", "--priority", "high"])
    assert result.exit_code == 0
    assert "mytask" in result.output
    assert "high" in result.output
```

---

## Related Skills for This Implementation

- [typer-cli-testing](../typer-cli-testing/SKILL.md) — For writing the tests above
- [typer-error-handling](../typer-error-handling/SKILL.md) — For better error messages
- [typer-cli-deployment](../typer-cli-deployment/SKILL.md) — For packaging as installable CLI
