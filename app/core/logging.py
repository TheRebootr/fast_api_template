"""Logging configuration using Loguru."""

import sys

from loguru import logger

from app.config import config


def configure_logging() -> None:
    """Configure Loguru logging based on application configuration.

    This function sets up logging with environment-aware behavior:
    - Development: logs to stdout AND file (errors only)
    - Production: logs to stdout only

    The configuration respects the following settings from config:
    - LOG_LEVEL: Minimum log level (DEBUG, INFO, WARNING, ERROR)
    - LOG_FILE_ENABLED: Enable file-based error logging
    - LOG_FILE_PATH: Path to error log file
    - LOG_FILE_ROTATION: Log file rotation size
    - LOG_FILE_RETENTION: Log file retention period

    File logging features (when enabled):
    - Automatic rotation by size
    - Automatic retention/cleanup
    - Compression of rotated files (zip)
    - Async-safe logging (enqueue=True)
    - Full backtrace and diagnosis in development
    """
    # Remove default handler
    logger.remove()

    # Add stdout handler (all environments)
    logger.add(
        sys.stdout,
        level=config.LOG_LEVEL,
        format=(
            "<green><level>{level: >10}</level></green> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:"
            "<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )
        if not config.is_production
        else (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:"
            "<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
        colorize=True,
        enqueue=True,  # Async-safe
        backtrace=config.is_production,
        diagnose=False,
    )

    # Add file handler (development only, ERROR level)
    if config.LOG_FILE_ENABLED:
        logger.add(
            config.LOG_FILE_PATH,
            level="ERROR",  # Only errors to file
            format=(
                "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
                "{level: <8} | "
                "{name}:{function}:{line} | "
                "{message}"
            ),
            rotation=config.LOG_FILE_ROTATION,
            retention=config.LOG_FILE_RETENTION,
            compression="zip",  # Compress rotated files
            enqueue=True,  # Async-safe
            backtrace=True,  # Full trace for errors
            diagnose=True,  # Detailed info for debugging
        )

    logger.info(
        f"Logging: level={config.LOG_LEVEL}, "
        f"file_logging={config.LOG_FILE_ENABLED}"
    )
