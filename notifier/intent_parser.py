import datetime
from notifier.utils import *

logger = get_logger('intent parser')

NOTIFY = 0


class IntentException(Exception):
    def __init__(self, message):
        super().__init__(message)


def parse_date_time(date_: str, time_: str):
    """
    Parse date part

    :param date_: date in format dd.mm and a few special words: {сегодня, завтра, послезавтра}
    :return:
    """
    now = datetime.datetime.now()
    if not date_:
        hours, minutes = parse_time(time_)
        goal_date = datetime.datetime(now.year,
                                      now.month,
                                      now.day,
                                      hours,
                                      minutes)
        return goal_date
    date_ = date_.lower()
    time_delta = 0
    type_ = 'days'

    if date_ == 'сегодня':
        time_delta = 0
    elif date_ == 'завтра':
        time_delta = 1
    elif date_ == 'послезавтра':
        time_delta = 2
    elif 'через' in date_:
        _, time_delta, time_type = date_.split()
        time_type = time_type.lower()
        time_delta = int(time_delta)
        if 'мин' in time_type:
            type_ = 'minutes'
        elif 'час' in time_type:
            type_ = 'hours'
    else:
        day, month = map(int, date_.split('.'))
        now = datetime.datetime(now.year, month, day)

    goal_date = now + datetime.timedelta(**{type_: time_delta})
    if type_ not in ['hours', 'minutes']:
        hours, minutes = parse_time(time_)
        goal_date = datetime.datetime(goal_date.year,
                                      goal_date.month,
                                      goal_date.day,
                                      hours,
                                      minutes)
    logger.debug(f'parsed date {goal_date}')
    return goal_date


def parse_time(time_: str):
    """
    Parse time part

    :param time_: time in format hh:mm
    :return: hours and minutes
    """

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
    logger.debug(f'parsed time {hour}:{minutes}')

    return hour, minutes


def get_intent(text: str):
    words = text.split()
    command = Modes.NONE
    if words[0].lower() == 'напомни':
        command = Modes.REMIND

    text = text[text.find(' '):]
    return command, text


def parse_remind(text: str) -> ParsingResult:
    """
    Parse remind command

    :param text: source string from chat except command part
    :return: ParsingResult - command (mode), date and
    time (datetime) and message for remind (message)
    """
    logger.debug(text)
    date_time = text[:text.rfind(':')]
    message = text[text.rfind(':')+1:].strip()
    try:
        date_, time_ = map(str.strip, date_time.split(' в '))
    except ValueError:
        date_ = date_time
        time_ = ''
    result_date_time = parse_date_time(date_.strip(), time_.strip())

    result = ParsingResult(datetime=result_date_time,
                           message=message)
    logger.debug(f'parsing result {result}')

    return result


if __name__ == '__main__':

    print(get_intent('напомни завтра: сделать дела'))
    print(get_intent('напомни 12.05 в 14:30: сделать дела'))
    print(get_intent('напомни в 14:30: сделать дела'))

    print(parse_remind(get_intent('напомни завтра: сделать дела1')[1]))
    print(parse_remind(get_intent('напомни 12.05 в 14:30: сделать дела2')[1]))
    print(parse_remind(get_intent('напомни в 14:30: сделать дела3')[1]))
