import asyncio

from telethon import TelegramClient
from telethon.events import NewMessage

from .clients import Bot
from .helpers import restart_client


def main(session: str, api_id: str, api_hash: str, entity: str) -> None:
    client = TelegramClient(session, api_id, api_hash)
    run_loop(client, entity)


def run_loop(client: TelegramClient, entity: str):
    bot_client = Bot(client, entity)
    bot_client.main_loop()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(site_visits(client))


async def site_visits(client: TelegramClient) -> None:
    print('Waiting for offers.')
    pattern = '^There.*/visit!.'

    @client.on(NewMessage(pattern=pattern))
    async def new_sites_listener(event):
        restart_client()

    async with client:
        await client.run_until_disconnected()


if __name__ == '__main__':
    pass
