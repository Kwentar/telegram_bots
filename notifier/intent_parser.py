from datetime import datetime, timedelta
from notifier.utils import *

logger = get_logger('intent parser')

NOTIFY = 0


class IntentException(Exception):
    def __init__(self, message):
        super().__init__(message)


def parse_date(date_: str):
    now = datetime.now().date()
    if not date_:
        return now
    date_ = date_.lower()
    day_delta = 0
    if date_ == 'сегодня':
        day_delta = 0
    elif date_ == 'завтра':
        day_delta = 1
    elif date_ == 'послезавтра':
        day_delta = 2
    else:
        day, month = map(int, date_.split('.'))
        now = datetime(now.year, month, day)

    goal_date = now + timedelta(days=day_delta)
    logger.debug(goal_date)
    return goal_date


def parse_time(time_: str):
    now = datetime.now()

    if not time_:
        hour, minutes = 14, 0
    elif ':' in time_:
        hour, minutes = map(int, time_.split(':'))
    else:
        try:
            hour, minutes = int(time_), 0
        except Exception as ex:
            logger.error(f'wrong time {time_} with exception {ex}')
            raise IntentException(f'wrong time {ex}')
    return datetime(now.year, now.month, now.day, hour=hour, minute=minutes)


def parse_intent(text: str) -> ParsingResult:

    logger.debug(text)
    words = text.split()
    if words[0].lower() == 'напомни':
        date_time = text[text.find(' '):text.rfind(':')]
        message = text[text.rfind(':')+1:].strip()
        try:
            date_, time_ = map(str.strip, date_time.split(' в '))
        except ValueError:
            date_ = date_time
            time_ = ''
        date_ = parse_date(date_.strip())
        time_ = parse_time(time_.strip())
        result_date_time = datetime(date_.year,
                                    date_.month,
                                    date_.day,
                                    time_.hour,
                                    time_.minute,
                                    time_.second)
        logger.debug((date_time, date_, time_))
        logger.debug(date_)
        logger.debug(date_)
        result = ParsingResult(mode=Modes.NOTIFY, datetime=result_date_time, message=message)
        return result
    else:
        raise IntentException(f'wrong command {words[0]}')


if __name__ == '__main__':
    print(parse_intent('напомни завтра: сделать дела'))
    print(parse_intent('напомни 12.05 в 14:30: сделать дела'))
    print(parse_intent('напомни в 14:30: сделать дела'))