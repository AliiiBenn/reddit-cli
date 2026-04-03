"""Shared utilities for Reddit CLI commands."""
from pathlib import Path

import typer

from reddit_cli.errors import handle_validation_error


# =============================================================================
# Valid Values Constants
# =============================================================================

VALID_FORMAT_VALUES = ["display", "sql", "csv", "xlsx"]

VALID_SORT_VALUES = ["hot", "new", "top", "rising", "controversial", "gilded"]
VALID_PERIOD_VALUES = ["day", "week", "month", "year", "all"]

VALID_SEARCH_SORT_VALUES = ["relevance", "hot", "top", "new", "comments"]
VALID_SEARCH_PERIOD_VALUES = ["hour", "day", "week", "month", "year", "all"]

VALID_SUBREDDIT_SORT_VALUES = ["gilded", "subscribers", "active"]


# =============================================================================
# Validation Functions
# =============================================================================

def _validate_sort_period(
    sort: str,
    period: str | None,
    limit: int,
    valid_sort_values: list[str],
    valid_period_values: list[str],
) -> None:
    """Validate sort, period, and limit parameters.

    Args:
        sort: Sort type
        period: Time period (or None)
        limit: Number of results
        valid_sort_values: List of valid sort values
        valid_period_values: List of valid period values

    Raises:
        typer.Exit: If validation fails with exit code 2
    """
    if sort not in valid_sort_values:
        handle_validation_error("sort", valid_sort_values, sort)

    if period is not None and period not in valid_period_values:
        handle_validation_error("period", valid_period_values, period)

    if limit < 1 or limit > 100:
        typer.echo("Error: --limit must be between 1 and 100", err=True)
        raise typer.Exit(code=2)


def _validate_format(format_type: str, valid_values: list[str] | None = None) -> None:
    """Validate format type.

    Args:
        format_type: Format type to validate
        valid_values: Optional list of valid values (defaults to VALID_FORMAT_VALUES)

    Raises:
        typer.Exit: If validation fails with exit code 2
    """
    if valid_values is None:
        valid_values = VALID_FORMAT_VALUES
    if format_type not in valid_values:
        handle_validation_error("format", valid_values, format_type)


# =============================================================================
# Path Validation
# =============================================================================

def validate_output_path(path: Path) -> Path:
    """Validate output path to prevent path traversal attacks.

    Args:
        path: The path to validate

    Returns:
        The resolved absolute path

    Raises:
        typer.Exit: If path is invalid with exit code 2
    """
    # Resolve to absolute path
    resolved = path.resolve()

    # Check for path traversal attempts
    path_str = str(resolved)
    if ".." in path_str:
        typer.echo("Error: Path traversal not allowed", err=True)
        raise typer.Exit(code=2)

    # Check if path starts with dash (could be interpreted as option)
    if path_str.startswith("-"):
        typer.echo("Error: Path cannot start with '-'", err=True)
        raise typer.Exit(code=2)

    return resolved
