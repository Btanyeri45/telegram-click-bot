from typing import Any
from urllib.parse import urljoin

from bs4 import BeautifulSoup


class ClickBot:
    """Inside this are helper methods for when interacting with Telegram 
    click bots.
    """

    @staticmethod
    def check_buttonurl(summary) -> dict[str, Any]:
        """Verify and get KeyboardButtonUrl in summary of results.

        The KeyboardButtonUrl object is defined by its attributes,
        text and url.

        Returns:
            dict: A dictionary about the message's basic information.
        """
        try:
            details = {
                'message_id': summary.get('id'),
                'user_id': summary.get('user_id'),
                'url': summary.get('rows')[0].buttons[0].url
            }
            return details
        except (AttributeError, Exception):
            raise

    @staticmethod
    def post_options(resptext, url) -> dict[str, Any]:
        try:
            results = BeautifulSoup(resptext,
                                    features='html.parser').find(id='headbar')
            options = {
                'payload': {
                    'code': results['data-code'],
                    'token': results['data-token'],
                },
                'redirect': urljoin(url, '../reward'),
                'timer': results['data-timer'],
            }
            return options
        except (AttributeError, Exception):
            raise

    @property
    def custom_headers(self) -> dict[str, Any]:
        headers = {
            'accept':
                '*/*',
            'cookie':
                '_ga=GA1.2.1493590550.1622941063; _gid=GA1.2.570248229.1622941063; cf_chl_2=32c29d94bd89355; cf_chl_prog=x9; cf_clearance=a86998a5d73c744edd94574d612fc571ad5e1e79-1623046591-0-150; __cf_bm=fed1e2a27e4c31dd39d653def97cbf01f2094ca4-1623047902-1800-Aca8X/KUqNeUY2XrRXKCn8Zj4f27hkQBrKtlpomnoyYPxotKqqkidPBJdzSes3JJt2wcht3PKOHjjOjupEKGpd/BLkOKaQNDpmpfzMp5/ctuuz3AFAj0TPCwz96zqPxmzQ==',
            'origin':
                None,
            'referer':
                None,
            'user-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
            'x-requested-with':
                'XMLHttpRequest',
        }
        return headers
