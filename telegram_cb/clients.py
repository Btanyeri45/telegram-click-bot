import time

from requests import ConnectionError
from telethon import TelegramClient, sync

from .exceptions import DejavuError, LinkError, NoOfferError
from .helpers import new_url, restart_client
from .loggers import console_logger, start_logger
from .messages import get_message_details
from .tasks import do_visit_site


class Bot:

    def __init__(self, client: TelegramClient, entity: str) -> None:
        self.client = client
        self.entity = entity

    def main_loop(self) -> None:
        start_logger()
        self.client.start()
        self.client.send_message(self.entity, '/visit')

        with self.client:
            self.visit_site()
            # self.join_chat()
            # self.message_bot()

    @console_logger
    def visit_site(self):
        # Specify limits
        max_attempt = 100
        max_link_cls = 10
        max_link_err = 10

        # Counters
        cls_att = 0
        link_err = 0
        visit_att = 0

        while visit_att <= max_attempt:

            # Remove current URL when the number of allowed LinkError
            # reaches maximum
            if link_err == max_link_err:
                link_err = 0
                cls_att += 1
                new_url(clear=True)

            if cls_att == max_link_cls:
                restart_client()

            try:
                do_visit_site(get_message_details(self.client, self.entity))
            except ConnectionError:
                max_attempt += 1
            except (AttributeError, DejavuError):
                self.client.send_message(self.entity, '/visit')
            except LinkError:
                link_err += 1
                time.sleep(5)
            except (Exception, KeyboardInterrupt, NoOfferError):
                new_url(clear=True)
                raise

            visit_att += 1

    def join_chat(self):
        pass

    def message_bot(self):
        pass
