"""
This module contains the needed logic when interacting with Telegram 
click bots.
"""
import os
import sys
from typing import Any
from urllib.parse import urljoin

import psutil
from bs4 import BeautifulSoup

from telegram_cb.settings import BASE_DIR


def check_buttonurl(summary: dict) -> dict[str, str]:
    """Verify and get KeyboardButtonUrl in summary of results.

    The KeyboardButtonUrl object is defined by its attributes,
    text and url.

    Returns:
        dict: A dictionary about the message's basic information.
    """
    details: dict[str, str] = {}
    dtl_props = ['message_id', 'user_id', 'url']
    btn_props = ['id', 'user_id', 'rows']

    for btnp, dtlp in zip(btn_props, dtl_props):
        # Uncertain if asking for forgiveness is faster or at least
        # somewhat better in this case
        try:
            details[dtlp] = str(summary[btnp][0].buttons[0].url)
        except TypeError:
            details[dtlp] = str(summary.get(btnp))

    return details


def post_options(resptext: str, url: Any) -> dict[str, Any]:
    results = BeautifulSoup(resptext, features='html.parser').find(id='headbar')
    options = {
        'payload': {
            'code': results['data-code'],
            'token': results['data-token'],
        },
        'redirect': urljoin(url, '../reward'),
        'timer': results['data-timer'],
    }
    return options


def format_header(header: dict, options: dict) -> dict:
    """Format request header

    Args:
        header (dict): The necessary header dictionary.
        options (dict): See post_options from the presets module.

    Returns:
        dict: A header ready for an HTTP request.
    """
    rewd = '/reward'
    code = f'/visit/{options["payload"]["code"]}'
    header['origin'] = options['redirect'].replace(rewd, '')
    header['referer'] = options['redirect'].replace(rewd, code)
    return header


def new_url(
    bdir: str = str(BASE_DIR),
    url: str = '',
    write: bool = False,
    clear: bool = False,
    fname: str = 'currenturl.txt',
) -> bool:
    """Check if the next target URL is currently being accessed.

    A lazy and ugly solution to long wait times during site visits. This 
    will perform IO operations on a text file and match the passed URL with 
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
    fpath = os.path.join(bdir, fname)
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


def restart_program():
    """Restart the loop and cleanup file objects and descriptors.
    """
    try:
        p = psutil.Process(os.getpid())
        for handler in p.open_files() + p.connections():
            os.close(handler.fd)
    except Exception as e:
        sys.exit(e)

    python = sys.executable
    os.execl(python, python, *sys.argv)


if __name__ == '__main__':
    pass
