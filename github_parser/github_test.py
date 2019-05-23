from github_parser.github_email_parser import get_email_from_account
from github_parser.github_email_parser import get_email_from_page


def test_page_email():
    assert get_email_from_page('kwentar') is None
    assert get_email_from_page('dbader') == 'mail@dbader.org'


def test_url():
    assert get_email_from_account('mi5aka') == \
        'commit_author: mi5aka | From: zakharova_a <mi5akatwi@gmail.com>'
    assert get_email_from_account('kwentar') == \
        'commit_author: kwentar | From: Aleksei <alekseev.yeskela@gmail.com>'


def test_get_email_from_account():
    assert get_email_from_account('mi5aka') == \
        'commit_author: mi5aka | From: zakharova_a <mi5akatwi@gmail.com>'
    assert get_email_from_account('kwentar') == \
        'commit_author: kwentar | From: Aleksei <alekseev.yeskela@gmail.com>'
    assert get_email_from_account('nimfadore') == \
        'commit_author: nimfadore | From: nimfadore <nimfadore96@gmail.com>'
    assert get_email_from_account('madjoks') == \
        'commit_author: madjoks | From: madjoks <madjoks@yandex.ru>'
    assert get_email_from_account('Jamakase') == \
        'commit_author: jamakase | From: Artem Astapenko <jamakase54@gmail.com>'
    assert get_email_from_account('panovivan') == \
        'Probably commit_author: панов иван | <i.panov@bars-open.ru>'
