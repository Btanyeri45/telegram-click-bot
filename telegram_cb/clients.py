import time

from requests import ConnectionError as ConErr
from requests import ReadTimeout
from telethon import TelegramClient, sync  # noqa: F401

from .exceptions import DejavuError, LinkError, NoOfferError
from .helpers import countdown_timer, new_url, restart_client
from .loggers import console_logger, console_show_stat, start_logger
from .messages import get_message_details
from .tasks import do_visit_site


class Bot:
    def __init__(
        self, client: TelegramClient, entity: str, reloop: bool = False
    ) -> None:
        self.client = client
        self.entity = entity
        self.reloop = reloop

    @console_logger
    def visit_site(self):
        # Specify limits
        # Number of visit attempts for site visits.
        max_attempt = 100

        # So far the longest required site stay is 60 seconds.
        # An integer of 15 * 5 should be enough to accomodate that
        # requirement.
        max_link_err = 15

        # The number of times the client will attempt to visit a link.
        # An int of 15 sounds reasonable.
        max_link_cls = 15

        # Counters
        cls_att = 0
        link_err = 0
        visit_att = 0

        while visit_att <= max_attempt:

            # Remove current URL when the number of allowed LinkError
            # reaches maximum.
            if link_err == max_link_err:
                link_err = 0
                cls_att += 1
                new_url(clear=True)

            if cls_att == max_link_cls:
                restart_client()

            try:
                do_visit_site(get_message_details(self.client, self.entity))
            except ConErr:
                max_attempt += 1
            except (AttributeError, DejavuError):
                self.client.send_message(self.entity, "/visit")
            except LinkError:
                link_err += 1
                time.sleep(5)
            except (KeyboardInterrupt, NoOfferError):
                new_url(clear=True)
                break

            visit_att += 1

    def join_chat(self):
        pass

    def message_bot(self):
        pass

    def main_loop(self) -> None:
        start_logger()
        self.client.start()
        self.client.send_message(self.entity, "/visit")

        with self.client:
            self.visit_site()
            # self.join_chat()
            # self.message_bot()

        if self.reloop:
            # Allow click bot to refresh more offers, then run client
            # again
            console_show_stat("Runs are scheduled.")
            console_show_stat("Allowing target bot to refresh more offers...")
            countdown_timer(3600)
            raise ReadTimeout
