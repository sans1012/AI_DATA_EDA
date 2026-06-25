"""
=========================================================
Logger Utility

Provides a centralized logger for the application.

Author : Sanskriti Jain
=========================================================
"""

import logging
from pathlib import Path

from config import LOG_DIR


LOG_FILE = LOG_DIR / "application.log"


def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger instance.

    Parameters
    ----------
    name : str
        Usually __name__

    Returns
    -------
    logging.Logger
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File Handler
    file_handler = logging.FileHandler(
        LOG_FILE,
        mode="a",
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger