import logging
import sys

from conf import settings


LOGGERS_NAMES_IN_USE: set[str] = set()


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if name in LOGGERS_NAMES_IN_USE:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s (%(filename)s:%(lineno)d %(threadName)s)\n\t"
        '%(levelname)s - %(name)s: "%(message)s"'
    )
    if settings.DEBUG:
        logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    LOGGERS_NAMES_IN_USE.add(name)

    return logger
