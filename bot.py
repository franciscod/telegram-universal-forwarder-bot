import os
import asyncio
from aiotg import TgBot

import sublogic

bot = TgBot(os.environ["TG_BOT_TOKEN"])
CHAT_ID_KEEPALIVE = '9147949'  # @franciscod telegram id for development purposes


@bot.default
def default(chat, msg):
    return chat.reply("Hello! Check out my commands with /help")


@bot.command(r"/help")
@bot.command(r"/start")
def help(chat, match):
    return chat.reply("""
Hello! This bot lets you subscribe to RSS/Atom feeds.
Here's the commands:
- /feedsub - subscribes to a feed
- /list  - lists current subscriptions
- /feedunsub - unsubscribes from a feed
- /export - sends you a /sub command that contains all current subscriptions
- /wipe - the bot forgets all the data about you
- /source - info about source code
- /help - view this help text (also triggered with /start)
This bot is being worked on, so it may break sometimes. Contact @franciscod if you want to!
""")


@bot.command(r"/source")
def source(chat, match):
    return chat.reply("""
This bot is Free Software under the LGPLv3.
It is powered by the awesome feedparser library: https://github.com/kurtmckee/feedparser
You can get the code from here:
https://github.com/franciscod/telegram-universal-feed-bot
""")


@bot.command(r"/feedsub(.*)")
def sub(chat, match):
    urls = match.group(1).split()

    if not urls:
        return chat.reply("Use /feedsub <url> [<url>...]")

    for url in urls:
        asyncio.ensure_future(chat.reply("Subscribing to {}...".format(url)))
        sublogic.subscribe(telegram_chat_id=chat.id, feed_url=url)

        asyncio.ensure_future(chat.reply("Done! Subscribed to FEED TITLE".format(url)))  # TODO


@bot.command(r"/list")
def list(chat, match):
    # TODO get the chat subscriptions and show them verbosely
    pass


@bot.command(r"/export")
def export(chat, match):
    # TODO get the chat subscriptions and show them in a whole line of /feedsub
    pass


@bot.command(r"/feedunsub")
def unsub_show(chat, match):
    # TODO get the chat subscriptions and show them as clickable commands
    # with /feedunsub_1, /feedunsub_2. /feedunsub_3 and so on
    # TODO potentially this would use a custom keyboard
    pass


@bot.command(r"/feedunsub_(.*)")
def unsub_do(chat, match):
    url = match.group(1)
    sublogic.unsubscribe(telegram_chat_id=chat.id, feed_url=url)


@bot.command(r"/wipe")
def wipe_ask(chat, match):
    # TODO ask for confirmation
    # TODO mark a flag that expires in 1min
    pass


@bot.command(r"/wipe Yes, I am totally sure.")
def wipe_do(chat, match):
    # TODO check if the flag hasn't expired and wipe
    pass

async def say(wat, chat_id):
    await bot.send_message(chat_id=chat_id, text=wat)


async def keepalive():
    await say('started!', chat_id=CHAT_ID_KEEPALIVE)
    while True:
        await asyncio.sleep(30*60)
        await say('still alive!', chat_id=CHAT_ID_KEEPALIVE)

if __name__ == '__main__':
    sublogic.init()
    asyncio.ensure_future(keepalive())
    bot.run()
