import time

from requests import ConnectionError
from telethon import TelegramClient, sync

from .exceptions import DejavuError, LinkError, NoOfferError
from .messages import ClickBotMsg
from .presets import ClickBotEntity
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

    def main_loop(self,
                  entity: str,
                  bot_type: str = 'click_bot',
                  max_attempt: int = 100) -> None:
        self.entity = entity
        self.messg._send_message(entity, '/visit')

        if bot_type.lower() == 'click_bot':
            self.click_bot_task(entity, ClickBotEntity(), max_attempt)

    def click_bot_task(self, entity: str, chat_type: ClickBotEntity,
                       max_attempt: int):
        with self.client:
            attmp = 0
            rest = 10
            while attmp <= max_attempt:
                try:
                    visit_site(self.messg._get_messages(entity), chat_type)
                except ConnectionError:
                    max_attempt += 1
                except (AttributeError, DejavuError):
                    self.messg._send_message(entity, '/visit')
                except LinkError:
                    max_attempt += 1
                    time.sleep(rest)
                except NoOfferError:
                    break
                except (Exception, KeyboardInterrupt):
                    raise
                attmp += 1
