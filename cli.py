import argparse
import sys

import telegram_cb as tcb


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('entity', type=str, help='example: @Dogecoin_click_bot')
    run_client(parser.parse_args())


def run_client(args):
    entity = args.entity
    tcb.main('session', tcb.API_ID, tcb.API_HASH, entity)


if __name__ == "__main__":
    sys.exit(main())
