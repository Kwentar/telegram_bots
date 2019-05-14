from datetime import datetime
import logging
from enum import Enum
from typing import NamedTuple
import pandas as pd

logging_level = logging.DEBUG


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging_level)
    sh = logging.StreamHandler()
    sh.setLevel(logging_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    return logger


class Modes(Enum):
    NOTIFY = 0
    CANCEL = 10


class ParsingResult(NamedTuple):
    mode: Modes
    datetime: datetime
    message: str


def read_info(file_name='images_info.csv'):
    return pd.read_csv(file_name, index_col='image')
