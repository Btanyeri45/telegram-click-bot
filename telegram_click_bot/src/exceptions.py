import sys
from typing import Optional


class NoOfferError(Exception):
    """Exception raised when no offers are available or recieved from 
    the current entitity.
    """

    def __init__(self,
                 entitiy: Optional[str] = None,
                 message: Optional[str] = 'No offers {0}') -> None:
        self.message = message.format(
            f':{entitiy}') if entitiy else message.format('')
        self.traceback = sys.exc_info()


class LinkError(Warning):
    """Exception raised when the target URL is invalid or unavailable.
    """

    def __init__(self,
                 url: Optional[str] = None,
                 message: Optional[str] = 'Same link {0}') -> None:
        self.message = message.format(f':{url}') if url else message.format('')
        self.traceback = sys.exc_info()


class DejavuError(Exception):
    """Exception raised when the client encounters the message it sent. 
    """

    def __init__(self, message: Optional[str] = 'I have done this before.'):
        self.message = message
        self.traceback = sys.exc_info()
