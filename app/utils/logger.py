import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from .config import cfg

LOG_DIR = cfg.logging.log_dir
LOG_FILE = cfg.logging.log_file
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


def get_logger(file_path: str):
    """
    Creates or retrieves a configured logger with both console and file handlers.

    This function implements a singleton-like pattern for named loggers to prevent
    duplicate handlers. It logs to stdout and a rotating file named 'app.log'.

    Args:
        file_path (str): The path of the file requesting the logger (usually __file__).
            The logger name is derived from the filename stem.

    Returns:
        logging.Logger: A configured logger instance with RotatingFileHandler 
            and StreamHandler attached.

    Example:
        >>> logger = get_logger(__file__)
        >>> logger.info("System initialized")
    """


    file_name = Path(file_path).stem  # extract file name without extension
    logger = logging.getLogger(file_name)

    if not logger.handlers:
        # crete log filepath
        log_file = os.path.join(LOG_DIR, f"{LOG_FILE}.log")

        # - console handler setup -
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.stream.reconfigure(encoding="utf-8", errors="replace")
        console_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
            )
        )

        # - file handler setup -
        os.makedirs(LOG_DIR, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=3
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
            )
        )

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        logger.setLevel(LOG_LEVEL)

    return logger