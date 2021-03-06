import time
import requests
from bs4 import BeautifulSoup
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from github import Github
import sys
import os
sys.path.append(os.getcwd())
from config import *


def get_commits_list_from_repo(account_name, repo_name):
    repo_url = 'https://github.com/' + account_name + '/' + \
               repo_name + '/commits/master'
    resp = requests.get(repo_url)
    soup = BeautifulSoup(resp.text, features="html.parser")
    commits_list = soup.find(class_='commits-listing')
    if commits_list is None:
        return None
    commits_list = commits_list.find_all(class_='commit')
    return commits_list


def get_author_and_email_from_commit(account_name, commit, check_author=True):
    if not commit.find(class_='message'):
        return None
    commit_url = commit.find(class_='message')['href']
    author = commit.find(class_='commit-author').text.strip().lower()

    if author == account_name.lower() or not check_author:

        commit_url = 'https://github.com/' + commit_url + '.patch'
        time.sleep(0.1)

        resp = requests.get(commit_url)

        if len(resp.text.split('\n')) > 1:

            email = resp.text.split('\n')[1]
            if '@' not in email:
                email = resp.text.split('\n')[2].strip()
            if email and \
                    '@' in email and \
                    '@users.noreply.github.com' not in email:
                return 'commit_author: {} | {}'.format(author, email)
    return None


def get_email_from_account(account_name):
    url = 'https://github.com/' + account_name + '?tab=repositories'
    resp = requests.get(url)
    if resp.ok:
        soup = BeautifulSoup(resp.text, features="html.parser")
        time.sleep(0.1)
        try:
            repos = soup.find(id='user-repositories-list').find_all('a')
            repos = [repo for repo in repos if 'class' not in repo.attrs]
            if not repos:
                return 'No repos'
            for repo in repos[:5]:
                if 'class' not in repo:
                    repo_name = repo.text.strip()
                    commits_list = get_commits_list_from_repo(account_name,
                                                              repo_name)
                    if not commits_list:
                        continue

                    for commit in commits_list:
                        author_and_email = \
                            get_author_and_email_from_commit(account_name,
                                                             commit)
                        if author_and_email:
                            return author_and_email
        except:
            return 'Terrible error'
    else:
        return 'wrong user name'
    if repos:
        repo_name = repos[0].text.strip()
        commits_list = get_commits_list_from_repo(account_name,
                                                  repo_name)
        if commits_list:
            author_and_email = \
                get_author_and_email_from_commit(account_name,
                                                 commits_list[0],
                                                 False)
            if author_and_email:
                return f'Probably {author_and_email}'

    return 'Cannot find anything =('


git_api = None


def login(force=False):
    global git_api
    if force or git_api is None:
        logger.info('logging in github')
        git_api = Github(github_user, github_token)
    return git_api


def get_email_from_page(account_name):
    try:
        g = login()
        return g.get_user(account_name).email
    except:
        try:
            g = login(force=True)
            return g.get_user(account_name).email
        except:
            return None


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
    text = message['message']['text']
    account_name = text.split('/')[-1]
    page_email = get_email_from_page(account_name)
    email = get_email_from_account(account_name)

    try:
        logger.warning(message['message']['from_user']['username'] + ' ' +
                       message['message']['from_user']['first_name'])
    except:
        pass
    logger.info(message['message']['text'], account_name, email, page_email)
    print('-'*40)
    if page_email:
        answer = f'Page email: {page_email}\n{email}'
    else:
        answer = email
    updater.bot.send_message(message.effective_chat.id, answer)


def start(bot, message):
    updater.bot.send_message(message.effective_chat.id,
                             'Send me nickname, please')


def error(update, context):
    """Log Errors caused by Updates."""
    print('Update "%s" caused error "%s"', update, context.error)


if __name__ == '__main__':

    user_token = tg_github_user_token
    updater = Updater(token=user_token)

    # user_token = tg_room_vs_plan_token
    # updater = Updater(token=user_token, request_kwargs={'proxy_url': address})
    dispatcher = updater.dispatcher

    text_handler = MessageHandler(Filters.text, check_text)
    dispatcher.add_handler(text_handler)
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    dispatcher.add_error_handler(error)
    updater.start_polling()
    print('Bot has started')
    updater.idle()
