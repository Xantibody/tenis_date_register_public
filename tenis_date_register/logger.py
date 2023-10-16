import logging
import datetime
from logging import Formatter, StreamHandler, getLogger, DEBUG
#from logging import FileHandler

class MyLogger:
    @staticmethod
    def setup(name, level=logging.DEBUG):
        logger = getLogger(name)
        logger.setLevel(DEBUG)
        if not logger.hasHandlers():
            formatter = Formatter(
                fmt="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            handler = StreamHandler()
            #handler = FileHandler(filename='test.log',encoding='utf-8')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger