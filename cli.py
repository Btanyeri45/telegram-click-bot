import argparse
import sys

import telegram_cb as tcb


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("entity", type=str, help="example: @Dogecoin_click_bot")
    parser.add_argument(
        "session", type=str, help="name for the session", nargs="?", default="session"
    )
    parser.add_argument(
        "schedule",
        type=bool,
        help="schedule runs rather than auto-detecting offers",
        nargs="?",
        default=False,
    )
    args = parser.parse_args()
    run_client(args.session, args.entity, args.schedule)


def run_client(session: str, entity: str, schedule: bool):
    tcb.main(session, tcb.API_ID, tcb.API_HASH, entity, schedule)


if __name__ == "__main__":
    sys.exit(main())
