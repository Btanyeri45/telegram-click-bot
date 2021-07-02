import time

from requests import ConnectionError
from telethon import TelegramClient, sync

from .exceptions import DejavuError, LinkError, LoopError, NoOfferError
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

    def visit_site(self, entity: str, max_attempt: int, max_loop: int = 10):
        current_loop = 0
        attempt = 0
        rest = 10
        while attempt <= max_attempt:
            if current_loop == max_loop:
                restart_program()

            try:
                do_visit_site(self.messg._get_messages(entity))
            except ConnectionError:
                max_attempt += 1
            except (AttributeError, DejavuError):
                self.messg._send_message(entity, '/visit')
            except LinkError:
                max_attempt += 1
                time.sleep(rest)
                new_url(clear=True)
            except NoOfferError:
                break
            except LoopError:
                current_loop += 1
            except (Exception, KeyboardInterrupt):
                raise
            attempt += 1

    def join_chat(self):
        pass

    def message_bot(self):
        pass
