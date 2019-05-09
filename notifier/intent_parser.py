from datetime import datetime, timedelta
import logging


logger = logging.getLogger('intent parser')
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)

logger.addHandler(sh)


class IntentException(Exception):
    def __init__(self, message):
        super().__init__(message)


def parse_date(date_: str):
    date_ = date_.lower()
    now = datetime.now().date()
    day_delta = 0
    if date_ == 'завтра':
        day_delta = 1
    elif date_ == 'послезавтра':
        day_delta = 2
    else:
        day, month = map(int, date_.split('.'))
        now = datetime(now.year, month, day)

    goal_date = now + timedelta(days=day_delta)
    logger.debug(goal_date)
    return goal_date


def parse_intent(text: str):

    logger.debug(text)
    words = text.split()
    if words[0].lower() == 'напомни':
        date_time = text[text.find(' '):text.rfind(':')].strip()
        date_, time_ = map(str.strip, date_time.split(' в '))

        logger.debug((date_time, date_, time_))
        logger.debug(parse_date(date_))
    else:
        raise IntentException(f'wrong command {words[0]}')


if __name__ == '__main__':
    parse_intent('напомни завтра в 14:30: сделать дела')
    parse_intent('напомни 12.05 в 14:30: сделать дела')