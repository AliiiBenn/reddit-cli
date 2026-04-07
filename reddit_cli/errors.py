"""Shared error handling utilities for Reddit CLI."""
import httpx
import typer

from reddit_cli.logging import get_logger

# Exit code constants for semantic exit codes
EXIT_GENERAL_ERROR = 1
EXIT_USAGE_ERROR = 2
EXIT_INTERRUPTED = 130


def handle_api_error(e: Exception) -> None:
    """Print a user-friendly error message for API errors and exit.

    Args:
        e: The exception to handle

    Exit codes:
        1: General error (network issues, API errors)
        2: Usage error (invalid arguments)
    """
    logger = get_logger()

    # Re-raise typer.Exit exceptions without modification
    if isinstance(e, typer.Exit):
        raise e
    if isinstance(e, httpx.TimeoutException):
        logger.error("Connection timed out: %s", str(e))
        typer.echo("Error: Connection timed out. Please check your internet connection and try again.", err=True)
        raise typer.Exit(code=EXIT_GENERAL_ERROR)
    elif isinstance(e, httpx.ConnectError):
        logger.error("Could not connect to Reddit: %s", str(e))
        typer.echo("Error: Could not connect to Reddit. Please check your internet connection.", err=True)
        raise typer.Exit(code=EXIT_GENERAL_ERROR)
    elif isinstance(e, httpx.HTTPStatusError):
        status_code = e.response.status_code
        logger.error("Reddit API error: status %s for URL %s", status_code, e.request.url)
        if status_code == 400:
            typer.echo(f"Error: Bad request (status {status_code}). Please check your input and try again.", err=True)
        elif status_code == 401 or status_code == 403:
            typer.echo(f"Error: Authentication required (status {status_code}). This feature may require login.", err=True)
        elif status_code == 404:
            typer.echo(f"Error: Resource not found (status {status_code}). Please check the ID and try again.", err=True)
        elif status_code == 429:
            logger.warning("Rate limited by Reddit")
            typer.echo(f"Error: Rate limited by Reddit (status {status_code}). Please wait a moment and try again.", err=True)
        elif status_code >= 500:
            typer.echo(f"Error: Reddit server error (status {status_code}). Please try again later.", err=True)
        else:
            typer.echo(f"Error: Reddit API returned status {status_code}. Please try again later.", err=True)
        raise typer.Exit(code=EXIT_GENERAL_ERROR)
    else:
        logger.error("Unexpected error: %s", str(e))
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=EXIT_GENERAL_ERROR)


def handle_validation_error(param_name: str, valid_values: list[str], received: str) -> None:
    """Handle validation errors for invalid parameter values.

    Args:
        param_name: Name of the parameter that failed validation
        valid_values: List of valid values
        received: The invalid value that was received

    Exit code: 2 (usage error)
    """
    logger = get_logger()
    valid_str = ", ".join(valid_values)
    logger.warning("Validation failed for --%s: received '%s', expected one of: %s", param_name, received, valid_str)
    typer.echo(f"Error: Invalid value '{received}' for --{param_name}. Valid values are: {valid_str}", err=True)
    raise typer.Exit(code=EXIT_USAGE_ERROR)


def handle_interrupt() -> None:
    """Handle user interruption (Ctrl+C).

    Exit code: 130 (interrupted)
    """
    logger = get_logger()
    logger.info("User interrupted execution")
    typer.echo("Interrupted by user.", err=True)
    raise typer.Exit(code=EXIT_INTERRUPTED)
