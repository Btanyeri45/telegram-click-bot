import argparse
import sys

import telegram_cb as tcb


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('entity', type=str, help='example: @Dogecoin_click_bot')
    parser.add_argument('session', type=str, help='name for the session', nargs='?', default='session')
    run_client(parser.parse_args())


def run_client(args):
    tcb.main(args.session, tcb.API_ID, tcb.API_HASH, args.entity)


if __name__ == "__main__":
    sys.exit(main())
