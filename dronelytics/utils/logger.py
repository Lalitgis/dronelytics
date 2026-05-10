"""Logger setup for dronelytics."""

import logging
from pathlib import Path


def setup_logger(name):
    """Set up logger with clean output (no decorative symbols)."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
