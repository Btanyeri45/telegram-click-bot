# telegram-click-bot
Automate telegram click bots for easy beer money.
- @Dogecoin_click_bot
- @Litecoin_click_bot
- @BCH_clickbot
- @Zcash_click_bot
- @Bitcoinclick_bot

# Features
- [x] Automatically detect new offers and perform tasks
- [x] Visit sites
- [ ] Join chats
- [ ] Message bots

# TODO
- [ ] Users stacking
- [ ] User stack parallel processing
- [ ] Output status for each process/user

# Installation
Clone the repository:
```
git clone https://github.com/huenique/telegram-click-bot.git
```

# Setup
1. Configure your environment variables or create a copy of `.env.example` inside the package root directory without `.example` at the end.

    Inside the `.env` file, set your Telegram `API_ID` and `API_HASH`. Get your own API_ID and API_HASH from [https://my.telegram.org](https://my.telegram.org)

2. Install the dependencies: `pip install -r requirements.txt`

# Usage
From the package root, run:
```
python cli.py -h
```

Example:

```
python cli.py "@Litecoin_click_bot"
```

You will be asked for your phone number on first run. This is what it will look like:
```
Please enter your phone (or bot token): +639123456789
Please enter the code you received: 12345
```

Once you get it running, go to your Telegram app!

# Update

Caution: For users only

To update the package and to get the new features and improvements, run:

```
git reset --hard
git pull
```

# Tips

* Let the script run and leave your device;
* or, run it on a different device.
* If you run into errors related to coroutines or telethon, run `make reset-session`. If your OS doesn't have `make`, simply delete the session files from the package root.

# Contributing
- Fork the [repository](https://github.com/huenique/telegram-click-bot)
- Post and discuss an [issue](https://github.com/huenique/telegram-click-bot/issues).
- Create a [pull request](https://github.com/huenique/telegram-click-bot/pulls)
