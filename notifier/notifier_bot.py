from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from config import *
from notifier.chat_id_manager import ChatIdManager
from notifier.utils import *
from notifier.intent_parser import parse_intent


logger = get_logger('notifier_bot')

chat_manager = ChatIdManager()


def check_text(bot, message):

    # if message['message']['from_user']['username'] != 'Kwent':
    #     updater.bot.send_message(message.effective_chat.id,
    #                              f'You are not the God, get out')
    message_text = message['message']['text']
    try:
        logger.info(f"Message {message_text} from "
                    f"{message['message']['from_user']['username']} "
                    f"{message['message']['from_user']['first_name']}")
    except:
        pass

    if message.effective_chat.id < 0 and not message_text.startswith('@animal_reminder_bot'):
        return
    if message_text.startswith('@animal_reminder_bot'):
        message_text = message_text[message_text.index(' ')+1:]
    result = parse_intent(message_text)

    command = result.mode
    if command == Modes.NOTIFY:
        if result.datetime < datetime.now():
            updater.bot.send_message(message.effective_chat.id,
                                     f'{result.datetime} прошло. \nЯ не могу исправить твоих ошибок прошлого, пока.')
        else:
            if message.effective_chat.id not in chat_manager:
                chat_manager.add_item(updater, message.effective_chat.id)
            chat_manager[message.effective_chat.id].add_event(result)
            updater.bot.send_message(message.effective_chat.id,
                                     f'Я напомню {result.datetime} о {result.message}')
    else:
        updater.bot.send_message(message.effective_chat.id, help_string)
    logger.info(f'parsed result: {result}')


def start(bot, message):
    updater.bot.send_message(message.effective_chat.id, help_string)


def error(update, context):
    """Log Errors caused by Updates."""
    print('Update "%s" caused error "%s"', update, context.error)


if __name__ == '__main__':
    user_token = notifier_token

    # updater = Updater(token=user_token, request_kwargs={'proxy_url': address})
    updater = Updater(token=user_token)
    dispatcher = updater.dispatcher

    text_handler = MessageHandler(Filters.text, check_text)
    dispatcher.add_handler(text_handler)
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    dispatcher.add_error_handler(error)
    updater.start_polling()
    print('Notifier Bot has started')
    updater.idle()
