import random
import threading
from queue import PriorityQueue
import datetime
import time

from notifier.speech_bubble import generate_image
from notifier.utils import read_info, ParsingResult, get_logger


class Chat:
    images_info = read_info(file_name='notifier/resources/images_info.csv')
    images = images_info.index.values

    def __init__(self, bot, chat_id, minutes_delta=-60):
        self.q = PriorityQueue()
        self.bot = bot
        self.chat_id = chat_id
        self.minutes_delta = minutes_delta
        self.logger = get_logger(f'Chat {chat_id}')
        self.thread = threading.Thread(target=Chat.chat_thread,
                                       kwargs={'bot': bot,
                                               'user_queue': self.q,
                                               'chat_id': self.chat_id,
                                               'logger': self.logger})
        self.thread.start()

    def add_event(self, parsing_result: ParsingResult):
        self.logger.info(f'thread is alive: {self.thread.is_alive()}')
        event = (parsing_result.datetime,
                 parsing_result.message)
        self.logger.info(f'added event {event}')
        self.q.put(event)

    @staticmethod
    def upper_first_letter(s):
        return s[0].upper() + s[1:]

    @staticmethod
    def chat_thread(bot, user_queue: PriorityQueue, chat_id, logger):
        font_path = 'notifier/resources/OpenSans-Semibold.ttf'
        while True:
            if user_queue.queue:
                msg = user_queue.queue[0]
                if msg[0] < datetime.datetime.now():
                    msg = user_queue.get()
                    try:
                        img_name = generate_image(Chat.images_info,
                                                  random.choice(Chat.images),
                                                  Chat.upper_first_letter(msg[1]),
                                                  font_path=font_path)
                        logger.info(f'remind about {msg[1]}')
                        bot.send_photo(chat_id,
                                       open(img_name, 'rb'),
                                       caption=f'{msg[1]}')
                    except Exception as ex:
                        logger.error(f'ERROR: {ex}')
                        user_queue.put(msg)
            time.sleep(1)
