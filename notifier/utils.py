import datetime
import logging
from enum import Enum
from typing import NamedTuple
import pandas as pd

logging_level = logging.DEBUG

help_string = \
    f'''Я поддерживаю следующий синтаксис:
напомни <когда, дата> в <когда, время>: <текст напоминания>
Если не будет <когда, дата>, то сегодня, если не будет <когда, время>, то в 14:00.
Пример правильных напоминаний:
напомни завтра: купить молока
напомни 25.07 в 16:45: собеседование
напомни в 15:30: позвонить маме'''


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging_level)
    sh = logging.StreamHandler()
    sh.setLevel(logging_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - '
                                  '%(levelname)s - %(message)s')
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    return logger


class Modes(Enum):
    REMIND = 0
    CANCEL = 10
    NONE = 100


class ParsingResult(NamedTuple):
    datetime: datetime.datetime
    message: str


def read_info(file_name='images_info.csv'):
    return pd.read_csv(file_name, index_col='image')
