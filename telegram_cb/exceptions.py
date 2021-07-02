import sys
from typing import Optional


class NoOfferError(Exception):
    """Exception raised when no offers are available or recieved from the
    current entitity.
    """

    def __init__(self,
                 entitiy: str = '',
                 message: str = 'No offers {0}') -> None:
        self.message = message.format(
            f':{entitiy}') if entitiy else message.format('')
        self.traceback = sys.exc_info()

    def __str__(self):
        return str(self.message)


class LinkError(Warning):
    """Exception raised when the target URL is invalid or unavailable.
    """

    def __init__(self, url: str = '', message: str = 'Same link {0}') -> None:
        self.message = message.format(f':{url}') if url else message.format('')
        self.traceback = sys.exc_info()

    def __str__(self):
        return str(self.message)


class DejavuError(Exception):
    """Exception raised when the client encounters a message it sent. 
    """

    def __init__(self, message: Optional[str] = 'I have done this before.'):
        self.message = message
        self.traceback = sys.exc_info()

    def __str__(self):
        return str(self.message)


class LoopError(Exception):
    """Raised when the main loop has reached the maximum acceptable 
    number of iterations.
    """

    def __init__(self, message: str = 'Max loop reached.') -> None:
        self.message = message
        self.traceback = sys.exc_info()

    def __str__(self):
        return str(self.message)
