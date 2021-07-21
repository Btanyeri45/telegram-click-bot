import subprocess
import sys

import requests
from requests.models import Response

from .exceptions import DejavuError, LinkError
from .helpers import custom_headers, format_header, new_url, post_options
from .messages import check_buttonurl
from .settings import BASE_DIR


class ClinetSession:
    def __init__(self) -> None:
        self.session = requests.Session()

    def get(self, url, timeout=5) -> tuple[Response, str]:
        resp = self.session.get(url, timeout=timeout)
        return resp, resp.text.lower()

    def post(self, url, data, headers, timeout=5) -> tuple[str, int]:
        resp = self.session.post(
            url,
            data=data,
            headers=headers,
            timeout=timeout,
        )
        return resp.text, resp.status_code


def do_visit_site(chat_summary: dict) -> None:
    """Perform HTTP requests accordingly.

    Args:
        chat_summary (dict): Summary/details of the bot's message.

    Raises:
        LinkError: Can't perform operations on the URL.
        DejavuError: Loop encounters a client-sent message.
    """

    cf = "challenge-form"
    tl = "timeleft"
    clientuser_msg = "/visit"
    page_indicator = "action="

    url = check_buttonurl(chat_summary)["url"]
    if not new_url(url=url):
        raise LinkError

    session: ClinetSession = ClinetSession()
    get_res, resp_text = session.get(url)

    if clientuser_msg in resp_text and page_indicator not in resp_text:
        raise DejavuError
    if tl in resp_text:
        opt = post_options(get_res.text, url)
        hed = format_header(custom_headers(), opt)
        _ = session.post(opt["redirect"], opt["payload"], hed)
    elif cf in resp_text:
        subprocess.Popen([sys.executable, f"{BASE_DIR}/utils/openurl.py", url])

    new_url(url=url, write=True)


def do_join_chat():
    pass


def do_message_bot():
    pass
