# https://docs.python.org/3/library/logging.html#logrecord-attributes

from genericpath import isdir
import logging
import os

if not (isdir("logs")):
    os.mkdir("logs")

formatter = logging.Formatter("%(name)s | %(asctime)s | %(levelname)s | %(message)s")


def create_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(f"logs/{log_file}", mode="a")
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


"""
# first file logger
logger = setup_logger('first_logger', 'logs/first_logfile.log')
logger2 = setup_logger("second_logger", "logs/second.log")
"""

"""
logging.basicConfig(filename='logs/logs.log',
                    encoding='utf-8',
                    level=logging.DEBUG,
                    filemode = "w",
                    format = "%(message)s\n%(asctime)s - %(pathname)s - %(funcName)s - %(lineno)d"
                    )
"""

"""
logger.debug('This message should go to the log file')
logger2.info('So should this')
logger.warning('And this, too')
logger.error('And non-ASCII stuff, too, like Øresund and Malmö')
logger.critical("error")
"""
