# config/logger.py
import logging
import os

def setup_logger(name: str, log_file: str = "logs/app.log", level=logging.INFO):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    # Avoid duplicate logs
    if not logger.hasHandlers():
        logger.addHandler(handler)

    return logger
