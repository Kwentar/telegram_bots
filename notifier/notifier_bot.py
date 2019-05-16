import datetime
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
import sys
import os
sys.path.append(os.getcwd())
from config import *
from notifier.chat_id_manager import ChatIdManager
from notifier.utils import *
from notifier.intent_parser import get_intent, parse_remind

logger = get_logger('notifier_bot')

chat_manager = ChatIdManager()
bot_name = '@animal_reminder_bot'


def check_text(bot, message):
    message_text = message['message']['text']

    if message.effective_chat.id < 0 and not message_text.startswith(bot_name):
        return

    try:
        logger.info(f"Message {message_text} from "
                    f"{message['message']['from_user']['username']} "
                    f"{message['message']['from_user']['first_name']}")
    except:
        pass
    if message_text.startswith(bot_name):
        message_text = message_text[len(bot_name)+1:].strip()
    command, text = get_intent(message_text)

    if command == Modes.REMIND:
        process_remind(bot, message.effective_chat.id, text)
    else:
        bot.send_message(message.effective_chat.id, help_string)


def get_time_delta(chat_id):
    if chat_id in chat_manager:
        return chat_manager[chat_id].minutes_delta
    else:
        return 60


def process_remind(bot, chat_id, text):
    if chat_id not in chat_manager:
        chat_manager.add_item(bot, chat_id)
    result = parse_remind(text)

    if result.datetime < chat_manager[chat_id].get_now():
        logger.debug(f'previous {chat_manager[chat_id].get_now()}')
        bot.send_message(chat_id,
                         f'{result.datetime} прошло.\n'
                         f'Я не могу исправить твоих ошибок прошлого, пока.')
    else:
        chat_manager[chat_id].add_event(result)
        bot.send_message(chat_id, f'Я напомню {result.datetime} о '
                                  f'{result.message}')
    logger.info(f'parsed result for remind command: {result}')


def start(bot, message):
    bot.send_message(message.effective_chat.id, help_string)


def remind(bot, message):
    message_text = message['message']['text']
    _, text = get_intent(message_text)
    logger.info(f"parsed result: {message_text}")
    process_remind(bot, message.effective_chat.id, text)


def get_time(bot, message):
    chat_id = message.effective_chat.id
    if chat_id not in chat_manager:
        chat_manager.add_item(bot, chat_id)
    bot.send_message(message.effective_chat.id,
                     str(chat_manager[chat_id].get_now()))


def set_time(bot, message):
    message_text = message['message']['text']
    chat_id = message.effective_chat.id
    try:
        value = int(message_text.split()[1])
        if chat_id not in chat_manager:
            chat_manager.add_item(bot, chat_id, value)
        else:
            chat_manager[chat_id].minutes_delta = value
        logger.info(f'set up new time delta for chat {chat_id} = {value}')
        bot.send_message(message.effective_chat.id,
                         f'Время бота для вас: {chat_manager[chat_id].get_now()}')
    except:
        bot.send_message(message.effective_chat.id,
                         'Неправильный аргумент, '
                         'синтаксис /set_time <количество минут>, например, '
                         '/set_time 60 установит время GMT+3 (Москва)')


def error(update, context):
    """Log Errors caused by Updates."""
    print('Update "%s" caused error "%s"', update, context.error)


if __name__ == '__main__':
    # user_token = notifier_token
    # updater = Updater(token=user_token)

    user_token = room_vs_plan_token
    updater = Updater(token=user_token, request_kwargs={'proxy_url': address})
    dispatcher = updater.dispatcher

    text_handler = MessageHandler(Filters.text, check_text)
    dispatcher.add_handler(text_handler)
    start_handler = CommandHandler('start', start)
    remind_handler = CommandHandler('remind', remind)
    get_time_handler = CommandHandler('get_time', get_time)
    set_time_handler = CommandHandler('set_time', set_time)
    # get_time_handler = CommandHandler('get_time', remind)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(remind_handler)
    dispatcher.add_handler(get_time_handler)
    dispatcher.add_handler(set_time_handler)
    dispatcher.add_error_handler(error)
    updater.start_polling()
    print('Notifier Bot has started')
    updater.idle()
