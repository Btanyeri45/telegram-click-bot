import time

from requests import ConnectionError
from telethon import TelegramClient, sync

from .exceptions import DejavuError, LinkError, NoOfferError
from .helpers import new_url, restart_program
from .messages import ClickBotMsg
from .tasks import do_visit_site
from .utils.attribute import AttrDict


class Bot:

    def __init__(self, *args, **kwargs) -> None:
        self.setting = AttrDict(**kwargs)
        self.client = TelegramClient(
            self.setting.session_name,
            self.setting.api_id,
            self.setting.api_hash,
        )
        self.messg = ClickBotMsg(self.client)

    def connect(self) -> None:
        self.client.start()

    def main_loop(self, entity: str, max_attempt: int = 100) -> None:
        self.entity = entity
        self.messg._send_message(entity, '/visit')

        with self.client:
            self.visit_site(entity, max_attempt)
            # self.join_chat()
            # self.message_bot()

    def visit_site(self, entity: str, max_attempt: int):
        # Specify limits
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
                restart_program()

            try:
                do_visit_site(self.messg._get_messages(entity))
            except ConnectionError:
                max_attempt += 1
            except (AttributeError, DejavuError):
                self.messg._send_message(entity, '/visit')
            except LinkError:
                link_err += 1
                time.sleep(5)
            except (KeyboardInterrupt, NoOfferError):
                new_url(clear=True)
                break
            except Exception:
                raise

            visit_att += 1

    def join_chat(self):
        pass

    def message_bot(self):
        pass
