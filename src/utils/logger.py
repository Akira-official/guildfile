"""
src/utils/logger.py
Configures structured console and rotating file logging for HelixCore.
"""

import os
import sys
import logging
from logging.handlers import RotatingFileHandler

# Ensure UTF-8 output encoding across Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def setup_logger(name: str = "HelixCore", log_file: str = "helixcore.log") -> logging.Logger:
    """Configures and returns a thread-safe rotating file and console logger."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Rotating File Handler (Max 5MB, keep 3 backups)
    try:
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Could not initialize file logger: {e}")

    return logger

