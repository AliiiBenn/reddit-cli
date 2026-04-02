# DateTime

Typer supports `datetime` arguments with custom format parsing.

## Basic DateTime

```python
from typing import Annotated
import typer
from datetime import datetime

app = typer.Typer()

@app.command()
def schedule(
    date: Annotated[datetime, typer.Option("--date")],
):
    """Schedule with date."""
    typer.echo(f"Scheduled for {date}")
    typer.echo(f"Year: {date.year}, Month: {date.month}, Day: {date.day}")

# python main.py schedule --date 2024-12-25
# python main.py schedule --date "2024-12-25 14:30"
```

## Custom Date Formats

Specify multiple accepted formats:

```python
from typing import Annotated
import typer
from datetime import datetime

app = typer.Typer()

@app.command()
def schedule(
    date: Annotated[
        datetime,
        typer.Option(formats=["%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"])
    ],
):
    """Schedule with custom date formats."""
    typer.echo(f"Scheduled for {date}")

# python main.py schedule --date 25/12/2024
# python main.py schedule --date 25-12-2024
# python main.py schedule --date 2024-12-25
# All work with the specified formats
```

## Common DateTime Formats

| Format | Example | Description |
|--------|---------|-------------|
| `%Y-%m-%d` | 2024-12-25 | ISO date |
| `%d/%m/%Y` | 25/12/2024 | European date |
| `%m/%d/%Y` | 12/25/2024 | US date |
| `%Y-%m-%d %H:%M:%S` | 2024-12-25 14:30:00 | Date with time |
| `%Y-%m-%dT%H:%M:%S` | 2024-12-25T14:30:00 | ISO 8601 |
| `%d %B %Y` | 25 December 2024 | Long date format |

## DateTime with Time

```python
from typing import Annotated
import typer
from datetime import datetime

app = typer.Typer()

@app.command()
def schedule(
    when: Annotated[
        datetime,
        typer.Option(formats=["%Y-%m-%d %H:%M", "%Y-%m-%d"])
    ],
):
    """Schedule with date and optional time."""
    typer.echo(f"Scheduled for: {when}")
    if when.hour or when.minute:
        typer.echo(f"Time: {when.hour:02d}:{when.minute:02d}")
    else:
        typer.echo("Time: All day")
```

## DateTime Validation

```python
from typing import Annotated
import typer
from datetime import datetime, timedelta

app = typer.Typer()

@app.command()
def reserve(
    checkin: Annotated[datetime, typer.Option("--checkin")],
    checkout: Annotated[datetime, typer.Option("--checkout")],
):
    """Reserve hotel rooms with date validation."""
    if checkout <= checkin:
        typer.echo("Error: Checkout must be after checkin", err=True)
        raise typer.Exit(code=1)

    nights = (checkout - checkin).days
    typer.echo(f"Check-in: {checkin.strftime('%Y-%m-%d')}")
    typer.echo(f"Check-out: {checkout.strftime('%Y-%m-%d')}")
    typer.echo(f"Nights: {nights}")
```

## DateTime Relative

```python
from typing import Annotated
import typer
from datetime import datetime, timedelta

app = typer.Typer()

@app.command()
def schedule(
    start: Annotated[datetime, typer.Option("--start")],
    duration: Annotated[int, typer.Option("--days", help="Duration in days")] = 1,
):
    """Schedule with duration."""
    end = start + timedelta(days=duration)
    typer.echo(f"Start: {start.strftime('%Y-%m-%d')}")
    typer.echo(f"End: {end.strftime('%Y-%m-%d')}")
```

## ISO Format Parsing

```python
from typing import Annotated
import typer
from datetime import datetime

app = typer.Typer()

@app.command()
def sync(
    timestamp: Annotated[datetime, typer.Option("--timestamp")],
):
    """Sync with ISO timestamp."""
    typer.echo(f"Parsed timestamp: {timestamp.isoformat()}")
    typer.echo(f"Unix time: {timestamp.timestamp()}")
```

## DateTime with Default

```python
from typing import Annotated
import typer
from datetime import datetime, timedelta

app = typer.Typer()

def tomorrow():
    return datetime.now() + timedelta(days=1)

@app.command()
def schedule(
    date: Annotated[
        datetime,
        typer.Option("--date", default_factory=tomorrow)
    ],
):
    """Schedule with default to tomorrow."""
    typer.echo(f"Scheduled for: {date.strftime('%Y-%m-%d')}")
```

## Key Points

- `typer.DateTime` automatically parses date/time strings
- Use `formats` parameter to specify accepted format strings
- Multiple formats can be specified for flexible input
- Parsed datetime objects have full datetime functionality
- Use `default_factory` for dynamic default dates
- Format strings follow Python's `strptime` conventions
- `%H:%M` for 24-hour time, `%I:%M %p` for 12-hour time
