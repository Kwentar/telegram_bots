from notifier.chat_id import Chat
from notifier.utils import get_logger


class ChatIdManager(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.threads = []
        self.dict = dict()
        self.logger = get_logger('ChatIdManager')

    def __getitem__(self, item):
        return self.dict[item]

    def add_item(self, bot, chat_id, minutes_delta=60):
        self.logger.info(f'added new chat_id {chat_id}')
        self.dict[chat_id] = Chat(bot, chat_id, minutes_delta)

    def __contains__(self, item):
        return item in self.dict

    def get_stat_total(self):
        total_users = len(self.dict)
        total_reminders = 0
        for k in self.dict:
            total_reminders += self.dict[k].get_queue_size()
        stat_string = f'We have {total_users} users with ' \
            f'{total_reminders} reminders'
        self.logger.info(f'get stat, stat is {stat_string}')
        return stat_string


if __name__ == '__main__':
    d = ChatIdManager()
    d.add_item(None, 'tmp')
    d['tmp'] = 10
    d['ttt'] = 101
    print('tmp' in d)
    print('ttt' in d)
    print(d['tmp'], d['rrr'])
