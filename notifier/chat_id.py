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

    def __init__(self, bot, chat_id, minutes_delta=180):
        self.user_queue = PriorityQueue()
        self.bot = bot
        self.chat_id = chat_id
        self.minutes_delta = minutes_delta
        self.logger = get_logger(f'Chat {chat_id}')
        self.thread = threading.Thread(target=Chat.chat_thread,
                                       kwargs={'chat_object': self})
        self.thread.start()

    def add_event(self, parsing_result: ParsingResult):
        self.logger.info(f'thread is alive: {self.thread.is_alive()}')
        event = (parsing_result.datetime,
                 parsing_result.message)
        self.logger.info(f'added event {event}')
        self.user_queue.put(event)

    def get_now(self):
        return datetime.datetime.now() + \
               datetime.timedelta(minutes=self.minutes_delta)

    @staticmethod
    def upper_first_letter(s):
        return s[0].upper() + s[1:]

    def get_queue_size(self):
        return self.user_queue.qsize()

    @staticmethod
    def chat_thread(chat_object):
        font_path = 'notifier/resources/OpenSans-Semibold.ttf'
        while True:
            if chat_object.user_queue.queue:
                msg = chat_object.user_queue.queue[0]
                if msg[0] < chat_object.get_now():
                    msg = chat_object.user_queue.get()
                    try:
                        img_name = generate_image(Chat.images_info,
                                                  random.choice(Chat.images),
                                                  Chat.upper_first_letter(msg[1]),
                                                  font_path=font_path)
                        chat_object.logger.info(f'remind about {msg[1]}')
                        chat_object.bot.send_photo(chat_object.chat_id,
                                                   open(img_name, 'rb'),
                                                   caption=f'{msg[1]}')
                    except Exception as ex:
                        chat_object.logger.error(f'ERROR: {ex}')
                        chat_object.user_queue.put(msg)
            time.sleep(1)
