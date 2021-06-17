import json
import os
import subprocess
import sys
import time
from typing import Any, Union

import requests
from requests import ConnectionError
from requests.models import requote_uri

from .exceptions import DejavuError, LinkError
from .settings import BASE_DIR

OPENURL_UTIL_PATH = f'{BASE_DIR}/src/utils/openurl.py'

# HTML template attrib
CHALLENGE_FORM = 'challenge-form'
STAY_COUNTDOWN = 'timeleft'

# Checks
USER_VISIT_MSG = '/visit'


def visit_site(chat_summary: dict, chat_type: object) -> None:
    """Perform HTTP requests accordingly.

    Args:
        chat_summary (dict): Summary/details of the bot's message.
        chat_type (object): Object instantiated from the caller.

    Raises:
        LinkError: Method can't perform operations on the URL.
        AttributeError: Problem with dictionary keys.

    Returns:
        None
    """
    url = chat_type.check_buttonurl(chat_summary)['url']
    if not _new_url(url=url):
        raise LinkError
    response_object = {}
    with requests.Session() as session:
        try:
            resp = session.get(url, timeout=5)
            resptext = resp.text.lower()
        except ConnectionError:
            raise
        if USER_VISIT_MSG in resptext:
            raise DejavuError
        if STAY_COUNTDOWN in resptext:
            post_options = chat_type.post_options(resp.text, url)
            post_headers = _format_header(chat_type.custom_headers,
                                          post_options)
            session.post(post_options['redirect'],
                         data=post_options['payload'],
                         headers=post_headers,
                         allow_redirects=True,
                         timeout=5)
        if CHALLENGE_FORM in resptext:
            subprocess.Popen([sys.executable, OPENURL_UTIL_PATH, url])
            time.sleep(60)
            _new_url(url=url, write=True)


def _format_header(header: dict, options: dict) -> dict:
    """Format request header

    Args:
        header (dict): The necessary header dictionary.
        options (dict): See post_options from the presets module.

    Returns:
        dict: A header ready for an HTTP request.
    """
    rewd = '/reward'
    code = f'/visit/{options.get("payload").get("code")}'
    header['origin'] = options['redirect'].replace(rewd, '')
    header['referer'] = options['redirect'].replace(rewd, code)
    return header


def _new_url(url=None,
             write=False,
             clear=False,
             fname='currenturl.txt',
             fdir='src') -> bool:
    """Check if the next target URL is currently being accessed.

    A lazy solution to long wait times during site visits. This will 
    perform IO operations on a text file and match the passed URL with 
    the URL currently saved in said file.

    Args:
        url (str): Next target URL.
        write (bool): Whether to write the url to the file.
        clear (bool): Whether to clear the content of the file.
        fname (str): File where the previous/active URL is stored.
        fdir (str): Directory where within BASE_DIR.

    Returns:
        bool: True for no match, False otherwise. 
    """
    fpath = os.path.join(
        BASE_DIR,
        fdir,
        fname,
    )
    is_new = True
    with open(fpath, 'a+') as currurl:
        currurl.seek(0)
        if currurl.read() == url:
            is_new = False
        if write:
            currurl.truncate(0)
            currurl.write(url)
        if clear:
            currurl.truncate(0)
    return is_new
