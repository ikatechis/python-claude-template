"""
Logging configuration module.
Dual output: console (WARNING+ or DEBUG+) and file (DEBUG+ always).
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path


def setup_logging(log_prefix: str = "app") -> None:
    """Initialize logging system.

    Args:
        log_prefix: Prefix for log filename (e.g., "app", "game")

    - Creates timestamped log in logs/ directory
    - Console: WARNING+ by default, DEBUG+ if DEBUG=1
    - File: Always DEBUG+ for full history
    """
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    log_file = log_dir / f"{log_prefix}_{timestamp}.log"

    debug_mode = os.getenv("DEBUG", "0") == "1"

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.DEBUG if debug_mode else logging.WARNING)
    console.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))
    root_logger.addHandler(console)

    # File handler
    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )
    root_logger.addHandler(file_handler)

    logger = get_logger("logger")
    logger.info(f"Logging initialized - log file: {log_file}")
    logger.info(f"Debug mode: {'ON' if debug_mode else 'OFF'}")


def get_logger(name: str) -> logging.Logger:
    """Get logger instance for a module.

    Args:
        name: Module name (typically __name__)
    """
    return logging.getLogger(name)
