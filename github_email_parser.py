import time
import requests
from bs4 import BeautifulSoup
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
import logging
import re
from config import *


def get_email_from_account(account_name):
    url = 'https://github.com/' + account_name + '?tab=repositories'
    resp = requests.get(url)
    if resp.ok:
        soup = BeautifulSoup(resp.text, features="html.parser")
        time.sleep(0.1)
        try:
            repos = soup.find(id='user-repositories-list').find_all('a')
            if not repos:
                return 'No repos'
            for repo in repos[:5]:
                if 'class' not in repo:
                    repo_url = 'https://github.com/' + account_name + '/' + repo.text.strip() + '/commits/master'
                    resp = requests.get(repo_url)
                    soup = BeautifulSoup(resp.text, features="html.parser")
                    commits_list = soup.find(class_='commits-listing')
                    if commits_list is None:
                        continue
                    commits_list = commits_list.find_all(class_='commit')

                    for commit in commits_list:

                        commit_url = commit.find(class_='message')['href']
                        author = commit.find(class_='commit-author').text.strip().lower()

                        if author == account_name.lower():

                            commit_url = 'https://github.com/' + commit_url + '.patch'
                            time.sleep(0.1)

                            resp = requests.get(commit_url)
                            # emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", resp.text)

                            if len(resp.text.split('\n')) > 1:

                                email = resp.text.split('\n')[1]
                                if '@' not in email:
                                    email = resp.text.split('\n')[2].strip()
                                if email and '@' in email:
                                    return 'commit_author: {} | {}'.format(author, email)
                            else:
                                break
        except:
            return 'Terrible error'
    else:
        return 'wrong user name'
    return 'Cannot find anything =('


# Enable logging
logging.basicConfig(format='%(asctime)s  %(message)s',
                    level=logging.WARNING)

logger = logging.getLogger(__name__)

# print(get_email_from_account('LiudmilaE'))
# # print(get_email_from_account('nimfadore'))
# # print(get_email_from_account('sdfds'))
# exit()


def check_text(bot, message):
    print('-'*40)
    email = get_email_from_account(message['message']['text'])

    # print(message['message']['from']['username'], message['message']['from']['first_name'])
    try:
        logger.warning(message['message']['from_user']['username'] + ' ' + message['message']['from_user']['first_name'])
    except:
        pass
    print(message['message']['text'], email)
    print('-'*40)

    # update.message.reply_text(get_email_from_account(update.message.text))
    updater.bot.send_message(message.effective_chat.id, email)


def start(bot, message):
    updater.bot.send_message(message.effective_chat.id, 'Send me nickname, please')


def error(update, context):
    """Log Errors caused by Updates."""
    print('Update "%s" caused error "%s"', update, context.error)


if __name__ == '__main__':
    user_token = github_user_token

    # updater = Updater(token=token, request_kwargs={'proxy_url': address})
    updater = Updater(token=user_token)
    dispatcher = updater.dispatcher

    text_handler = MessageHandler(Filters.text, check_text)
    dispatcher.add_handler(text_handler)
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    dispatcher.add_error_handler(error)
    updater.start_polling()
    print('Bot has started')
    updater.idle()
