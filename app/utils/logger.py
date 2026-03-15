import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = "logs"
LOG_FILE = "app"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


def get_logger(file_path: str):
    file_name = Path(file_path).stem  # extract file name without extension
    logger = logging.getLogger(file_name)

    if not logger.handlers:

        log_file = os.path.join(LOG_DIR, f"{LOG_FILE}.log")

        # console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.stream.reconfigure(encoding="utf-8", errors="replace")
        console_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
            )
        )

        # file handler
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