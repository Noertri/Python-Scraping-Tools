import logging


DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL
NOTSET = logging.NOTSET


def create_stream_logger(name, fmt, level=None):
    logger = logging.getLogger(name)
    logger.setLevel(DEBUG)
    stream_handler = logging.StreamHandler()
    if level:
        stream_handler.setLevel(level)
    logger.addHandler(stream_handler)
    fmtr = logging.Formatter(fmt)
    stream_handler.setFormatter(fmtr)
    return logger