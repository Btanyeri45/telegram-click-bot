import os
import sys
from typing import Any
from urllib.parse import urljoin

import psutil
from bs4 import BeautifulSoup

from telegram_cb.settings import BASE_DIR


def custom_headers() -> dict[str, str]:
    headers = {
        'accept':
            '*/*',
        'cookie':
            '_ga=GA1.2.1493590550.1622941063; _gid=GA1.2.570248229.1622941063; cf_chl_2=32c29d94bd89355; cf_chl_prog=x9; cf_clearance=a86998a5d73c744edd94574d612fc571ad5e1e79-1623046591-0-150; __cf_bm=fed1e2a27e4c31dd39d653def97cbf01f2094ca4-1623047902-1800-Aca8X/KUqNeUY2XrRXKCn8Zj4f27hkQBrKtlpomnoyYPxotKqqkidPBJdzSes3JJt2wcht3PKOHjjOjupEKGpd/BLkOKaQNDpmpfzMp5/ctuuz3AFAj0TPCwz96zqPxmzQ==',
        'origin':
            '',
        'referer':
            '',
        'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        'x-requested-with':
            'XMLHttpRequest',
    }
    return headers


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
    fname: str = 'url.txt',
) -> bool:
    """Check if the next target URL is currently being accessed.

    This will perform IO operations on a text file and match the passed 
    URL with the URL currently saved in said file.

    Args:
        bdir (str): Directory where the fill will be saved and located.
        url (str): Next target URL.
        write (bool): Whether to write the url to the file.
        clear (bool): Whether to clear the content of the file.
        fname (str): File where the previous/active URL is stored.

    Returns:
        bool: True for not match, False otherwise. 
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


def restart_client():
    """Restart the loop and cleanup file objects and descriptors.
    """
    try:
        p = psutil.Process(os.getpid())
        for handler in p.open_files() + p.connections():
            os.close(handler.fd)
        python = sys.executable
        os.execl(python, python, *sys.argv)
    except psutil.AccessDenied:
        os.execv(sys.executable, ['python'] + sys.argv)
    except Exception as e:
        sys.exit(e)


if __name__ == '__main__':
    pass
