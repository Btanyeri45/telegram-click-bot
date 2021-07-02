import subprocess
import sys
import time

import requests
from requests import ConnectionError

from .exceptions import DejavuError, LinkError
from .helpers import check_buttonurl, format_header, new_url, post_options
from .presets import ClickBotPrereq
from .settings import BASE_DIR

OPENURL_UTIL_PATH = f'{BASE_DIR}/utils/openurl.py'

# HTML template attrib
CHALLENGE_FORM = 'challenge-form'
STAY_COUNTDOWN = 'timeleft'

# Checks
USER_VISIT_MSG = '/visit'


def do_visit_site(chat_summary: dict) -> None:
    """Perform HTTP requests accordingly.

    Args:
        chat_summary (dict): Summary/details of the bot's message.

    Raises:
        LinkError: Can't perform operations on the URL.
        DejavuError: Loop encounters a client sent message.
    """
    rest = 20
    url = check_buttonurl(chat_summary)['url']
    if not new_url(url=url):
        raise LinkError

    with requests.Session() as session:
        try:
            resp = session.get(url, timeout=5)
            resptext = resp.text.lower()
        except ConnectionError:
            raise
        if USER_VISIT_MSG in resptext:
            raise DejavuError
        elif STAY_COUNTDOWN in resptext:
            ch = ClickBotPrereq().custom_headers
            op = post_options(resp.text, url)
            he = format_header(ch, op)
            session.post(op['redirect'],
                         data=op['payload'],
                         headers=he,
                         allow_redirects=True,
                         timeout=5)
        elif CHALLENGE_FORM in resptext:
            subprocess.Popen([sys.executable, OPENURL_UTIL_PATH, url])
            time.sleep(rest)
        new_url(url=url, write=True)


def do_join_chat():
    pass


def do_message_bot():
    pass
