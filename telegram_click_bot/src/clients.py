import time

from requests import ConnectionError
from telethon import TelegramClient, sync

from .exceptions import DejavuError, LinkError, NoOfferError
from .messages import ClickBotMsg
from .presets import ClickBot
from .sessions import visit_site
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

    def main_loop(self, entity, clickbot=True, max_attempt=100) -> None:
        self._visit_task(entity)

        if clickbot:
            chat_type = ClickBot()

        with self.client:
            attmp = 0
            rest = 10
            while attmp <= max_attempt:
                try:
                    visit_site(self.messg._get_messages(entity), chat_type)
                except ConnectionError:
                    max_attempt += 1
                except (AttributeError, DejavuError):
                    self._visit_task(entity)
                except LinkError:
                    max_attempt += 1
                    time.sleep(rest)
                except NoOfferError:
                    break
                except (Exception, KeyboardInterrupt):
                    raise
                attmp += 1

    def _visit_task(self, entity) -> None:
        self.messg._send_message(entity, '/visit')
