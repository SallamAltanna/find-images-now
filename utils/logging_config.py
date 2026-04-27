"""
Logging Configuration
=====================
Provides a centralised logging setup for the FINd API.
Log level is configured via the LOG_LEVEL environment variable
(default: INFO). Supported levels: DEBUG, INFO, WARNING, ERROR, CRITICAL.

Usage:
    from utils.logging_config import get_logger
    logger = get_logger(__name__)
"""

import logging
import os
from dotenv import load_dotenv

load_dotenv()

def get_logger(name):
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # Silence the specifically noisy libraries
    logging.getLogger("python_multipart").setLevel(logging.WARNING)
    return logging.getLogger(name)
