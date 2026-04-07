"""Structured logging setup for Reddit CLI."""
import logging
import sys

# Logger instance for use across the codebase
logger = logging.getLogger("reddit_cli")

# Log levels
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR


def setup_logging(level: int = INFO) -> None:
    """Configure logging for the application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR). Default is INFO.
    """
    # Configure root logger
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stderr)
        ]
    )
    
    # Ensure our logger uses the configured level
    logger.setLevel(level)


def get_logger() -> logging.Logger:
    """Get the reddit_cli logger instance.
    
    Returns:
        The configured logger instance.
    """
    return logger
