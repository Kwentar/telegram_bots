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


if __name__ == '__main__':
    d = ChatIdManager()
    d.add_item(None, 'tmp')
    d['tmp'] = 10
    print('tmp' in d)
    print('ttt' in d)
    print(d['tmp'], d['rrr'])
