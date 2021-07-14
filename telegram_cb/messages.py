from typing import Any, Union

from telethon import TelegramClient

from .exceptions import LinkError, NoOfferError


def check_buttonurl(summary: dict) -> dict[str, str]:
    """Verify and get KeyboardButtonUrl in summary of results.

    The KeyboardButtonUrl object is defined by its attributes,
    text and url.

    Returns:
        dict: A dictionary about the message's basic information.
    """
    details: dict[str, str] = {}
    dtl_props = ['message_id', 'user_id', 'url']
    btn_props = ['id', 'user_id', 'rows']

    for btnp, dtlp in zip(btn_props, dtl_props):
        # Uncertain if asking for forgiveness is faster or at least
        # somewhat better in this case
        try:
            details[dtlp] = str(summary[btnp][0].buttons[0].url)
        except TypeError:
            details[dtlp] = str(summary.get(btnp))

    return details


def get_message_details(client: TelegramClient,
                        entity: str) -> Union[dict[str, Any], None]:
    message = client.get_messages(entity)
    message = message[0]
    text_lower = message.message.lower()

    user_common = {
        'visit': '/visit',
    }

    bot_common = {
        'reply_a': 'there are no new ads available',
    }

    try:
        summary = {
            'id': message.id,
            'user_id': message.peer_id.user_id,
            'rows': message.reply_markup.rows,
        }
        return summary
    except AttributeError:
        if bot_common['reply_a'] in text_lower:
            raise NoOfferError

        if user_common['visit'] in text_lower:
            raise LinkError

        return None
