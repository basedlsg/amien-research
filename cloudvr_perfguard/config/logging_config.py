"""
Logging configuration for CloudVR-PerfGuard
Provides structured logging with proper levels and formatting
"""

import logging
import os
import sys
from typing import Optional


def setup_logging(
    level: Optional[str] = None,
    log_file: Optional[str] = None,
    json_format: bool = False
) -> logging.Logger:
    """
    Configure application-wide logging

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL). Defaults to env var LOG_LEVEL or INFO
        log_file: Optional file path to write logs. If None, logs to stdout
        json_format: If True, use JSON formatting (useful for log aggregation)

    Returns:
        Configured logger instance
    """
    # Determine log level
    log_level = level or os.getenv("LOG_LEVEL", "INFO")
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # Create root logger
    logger = logging.getLogger("cloudvr_perfguard")
    logger.setLevel(numeric_level)

    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create formatter
    if json_format:
        # JSON formatting for production log aggregation
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
            '"module": "%(name)s", "message": "%(message)s"}'
        )
    else:
        # Human-readable formatting for development
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Add file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module

    Args:
        name: Module name (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(f"cloudvr_perfguard.{name}")


# Create default logger instance
default_logger = setup_logging()
