
import logging

from uvicorn.logging import DefaultFormatter


def setup_logger(name: str, log_level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    handler = logging.StreamHandler()
    handler.setLevel(log_level)
    handler.formatter = DefaultFormatter(fmt='%(levelprefix)s %(filename)s %(message)s')
    logger.addHandler(handler)
    return logger
