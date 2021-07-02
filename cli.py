import argparse
import sys

from telegram_cb import settings
from telegram_cb.clients import Bot

api_id = settings.API_ID
api_hash = settings.API_HASH

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('entity',
                        type=str,
                        help='example: @Dogecoin_click_bot')
    args = parser.parse_args()
    entity = args.entity
    bot = Bot(**{
        'session_name': 'session',
        'api_id': api_id,
        'api_hash': api_hash,
    })
    bot.connect()
    bot.main_loop(entity)


if __name__ == "__main__":
    sys.exit(main())
