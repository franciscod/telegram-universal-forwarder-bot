# telegram-universal-feed-bot
Hello! This is a [Telegram](https://telegram.org) bot that forwards Atom/RSS feeds to Telegram chats.

It's not available on Telegram yet, but stay tuned!

Also, this is kind of a re-iteration on [TwitterForwarderBot](https://github.com/franciscod/telegram-twitter-forwarder-bot):
 - PRO: the interface is very similar to it
 - PRO: aims to be more generic so many types of resources can be subscribed to (twitter, atom/rss; the sky is the limit!)
 - CON: isn't implemented yet


### How do I run this?

**The code is currently targeting Python 3.5**

- TL;DR:

```sh
# clone this thing
# create your virtualenv, activate it:
#     virtualenv -p python3 venv
#     . venv/bin/activate

# install the deps
pip install -r requirements.txt

# set the token environment variable
export TG_BOT_TOKEN=213919:whateverBotFatherGaveYou
# run the bot
make run
```


#### Bot token? pip-tools?

You'll need a Telegram Bot Token, you can get it via BotFather ([more info here](https://core.telegram.org/bots)).

If you want additional info just take a look at the `Makefile` and check out [pip-tools](https://github.com/nvie/pip-tools).
