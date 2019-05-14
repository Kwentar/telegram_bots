import threading
from queue import PriorityQueue
from datetime import datetime, timedelta
import time

from notifier.speech_bubble import generate_image
from notifier.utils import read_info, ParsingResult, get_logger


class Chat:
    images_info = read_info(file_name='notifier/resources/images_info.csv')

    def __init__(self, updater, chat_id):
        self.q = PriorityQueue()
        self.chat_id = chat_id
        self.minutes_delta = -60
        self.logger = get_logger(f'Chat {chat_id}')
        self.thread = threading.Thread(target=Chat.chat_thread,
                                       kwargs={'updater': updater,
                                               'user_queue': self.q,
                                               'chat_id': self.chat_id,
                                               'logger': self.logger})
        self.thread.start()

    def add_event(self, parsing_result: ParsingResult):
        event = (parsing_result.datetime + timedelta(minutes=self.minutes_delta), parsing_result.message)
        self.logger.info(f'added event {event}')
        self.q.put(event)

    @staticmethod
    def chat_thread(updater, user_queue: PriorityQueue, chat_id, logger):
        while True:
            if user_queue.queue:
                msg = user_queue.queue[0]
                if msg[0] < datetime.now():
                    msg = user_queue.get()

                    img_name = generate_image(Chat.images_info,
                                              'yellow_bird.jpg',
                                              msg[1].capitalize(),
                                              font_path='notifier/resources/OpenSans-Semibold.ttf')
                    logger.info(f'remind about {msg[1]}')
                    updater.bot.send_photo(chat_id, open(img_name, 'rb'),
                                           caption=f'{msg[1]}')
            time.sleep(1)
