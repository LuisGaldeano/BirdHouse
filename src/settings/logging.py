import logging


def logger():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    start_logger = logging.getLogger(__name__)
    return start_logger


logger = logger()