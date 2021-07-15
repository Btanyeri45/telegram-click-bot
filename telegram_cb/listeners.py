import asyncio
import os
import platform
import subprocess

from requests.exceptions import ReadTimeout
from telethon import TelegramClient
from telethon.events import NewMessage

from .clients import Bot
from .helpers import restart_client, timer
from .settings import BASE_DIR


def check_session_file(session_name: str) -> str:
    """Replace user input for session with already existing session file.
    """
    session_dir = str(BASE_DIR).strip('telegram_cb')
    for file in os.listdir(session_dir):
        if file.endswith('.session'):
            return file.split('.', 1)[0]
    return session_name


@timer
def main(session: str, api_id: str, api_hash: str, entity: str) -> None:
    try:
        session = check_session_file(session)
        client = TelegramClient(session, api_id, api_hash)
        run_loop(client, entity)
    except ReadTimeout as rt:
        print(f'{rt}\nRestarting client. Hit Ctrl+C to stop.')
        restart_client()
    except KeyboardInterrupt:
        if platform.system() == 'Windows':
            subprocess.run('cls')
        else:
            subprocess.run('clear')

    # TODO: show earning summary


def run_loop(client: TelegramClient, entity: str):
    bot_client = Bot(client, entity)
    bot_client.main_loop()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(site_visits(client))


async def site_visits(client: TelegramClient) -> None:
    pattern = '^There.*/visit!.'

    @client.on(NewMessage(pattern=pattern))
    async def new_sites_listener(event):
        restart_client()

    async with client:
        await client.run_until_disconnected()


if __name__ == '__main__':
    pass
