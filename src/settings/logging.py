import logging
from logging.config import fileConfig
from pathlib import Path

LOG_CONFIG_PATH = Path("/src/logs/logging_config.ini")

if LOG_CONFIG_PATH.exists():
    fileConfig(LOG_CONFIG_PATH, disable_existing_loggers=False)
else:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    )

def get_logger(name: str):
    return logging.getLogger(name)