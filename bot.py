import os
import asyncio
from aiotg import TgBot
import sublogic

bot = TgBot(os.environ["TG_BOT_TOKEN"])


# http://www.peterbe.com/plog/uniqifiers-benchmark -- by Lukáš, 13 January 2016. thank you!
def uniquify(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


@bot.default
def default(chat, msg):
    return chat.reply("Hello! Check out my commands with /help")


@bot.command(r"/feedsub(.*)")
def feedsub(chat, match):
    """subscribes to a feed"""
    urls = match.group(1).split()

    if not urls:
        return chat.reply("Use /feedsub <url> [<url>...]")

    for url in urls:
        asyncio.ensure_future(chat.reply("Subscribing to {}...".format(url)))
        sublogic.subscribe(telegram_chat_id=chat.id, feed_url=url)

        asyncio.ensure_future(chat.reply("Done! Subscribed to FEED TITLE".format(url)))  # TODO


@bot.command(r"/list")
def list(chat, match):
    """lists current subscriptions"""
    # TODO get the chat subscriptions and show them verbosely
    pass


@bot.command(r"/export")
def export(chat, match):
    """sends you a /sub command that contains all current subscriptions"""
    # TODO get the chat subscriptions and show them in a whole line of /feedsub
    pass


@bot.command(r"/feedunsub")
def feedunsub(chat, match):
    """unsubscribes from a feed"""
    # TODO get the chat subscriptions and show them as clickable commands
    # with /feedunsub_1, /feedunsub_2. /feedunsub_3 and so on
    # TODO potentially this would use a custom keyboard
    pass


@bot.command(r"/feedunsub_(.*)")
def unsub_do(chat, match):
    url = match.group(1)
    sublogic.unsubscribe(telegram_chat_id=chat.id, feed_url=url)


@bot.command(r"/wipe")
def wipe(chat, match):
    """the bot forgets all the data about you"""
    # TODO ask for confirmation
    # TODO mark a flag that expires in 1min
    pass


@bot.command(r"/wipe Yes, I am totally sure.")
def wipe_do(chat, match):
    # TODO check if the flag hasn't expired and wipe
    pass


@bot.command(r"/source")
def source(chat, match):
    """info about source code"""
    return chat.reply("""
This bot is Free Software under the LGPLv3.
It is powered by the awesome feedparser library: https://github.com/kurtmckee/feedparser
You can get the code from here:
https://github.com/franciscod/telegram-universal-feed-bot
""")


@bot.command(r"/help")
@bot.command(r"/start")
def help(chat, match):
    """view help text"""
    fns = uniquify(fn for re, fn in bot._commands)

    command_docstrings = ["/{} - {}".format(fn.__name__, fn.__doc__)
                          for fn in fns if fn.__doc__ is not None]

    return chat.reply('\n'.join([
        "Hello! This bot lets you subscribe to RSS/Atom feeds.",
        "Here's the commands:",
        *command_docstrings,
        "This bot is being worked on, so it may break sometimes. "
        "Contact @franciscod if you want to chat about it!"
    ]))

if __name__ == '__main__':
    sublogic.init()
    bot.run()
