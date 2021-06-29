from typing import Any

from telethon import TelegramClient

from .exceptions import LinkError, NoOfferError


class ClickBotMsg:
    def __init__(self, client: TelegramClient) -> None:
        self.client = client

    def _start(self) -> None:
        self.client.start()

    def _send_message(self, entity: str, message: str) -> None:
        self.client.send_message(entity, message)

    def _get_messages(self, entity: str) -> dict[str, Any]:
        message = self.client.get_messages(entity)
        message = message[0]
        self._messages_n_action(message)
        summary = {
            'id': message.id,
            'user_id': message.peer_id.user_id,
            'rows': message.reply_markup.rows,
        }
        return summary

    def _messages_n_action(self, message: Any) -> None:
        user_common = {
            'visit': '/visit',
        }
        bot_common = {
            'reply_a': 'there are no new ads available',
        }

        text = message.message
        text_lower = text.lower()

        if bot_common['reply_a'] in text_lower:
            print('\nNo new ads\n')
            raise NoOfferError

        if user_common['visit'] in text_lower:
            raise LinkError
