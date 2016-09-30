import os
import asyncio

from aiotg import Bot

import models
import resources
from resources.util import future_texts

# http://www.peterbe.com/plog/uniqifiers-benchmark -- by Lukáš, 13 January 2016. thank you!


def uniquify(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def default(chat, msg):
    return chat.reply("Hello! Check out my commands with /help")


def listsubs(chat, match):
    """lists current subscriptions"""
    chat_model = models.TelegramChat.from_aiotg(chat)

    if len(chat_model.subscriptions) == 0:
        return chat.reply('This chat has no subscriptions!')

    l = []
    for sub in chat_model.subscriptions:
        res = sub.resource
        l.append("- {}".format(res))
    return chat.reply('\n'.join(l))


@asyncio.coroutine
def export(chat, match):
    """sends you the proper commands that contains commands for restoring your subscriptions"""
    chat_model = models.TelegramChat.from_aiotg(chat)

    if len(chat_model.subscriptions) == 0:
        return chat.reply('This chat has no subscriptions!')

    yield from chat.reply('Here are your subscription commands. You can forward them to me!')

    with future_texts(chat) as add_text:
        for sub in chat_model.subscriptions:
            add_text(sub.resource.sub_command)


def unsub(chat, match):
    """unsubscribe from things you've subscribed earlier"""

    chat_model = models.TelegramChat.from_aiotg(chat)

    if len(chat_model.subscriptions) == 0:
        return chat.reply('This chat has no subscriptions!')

    l = []
    for sub in chat_model.subscriptions:
        res = sub.resource
        l.append('/unsub_{} - {}'.format(res.cmd_id, res))
    return chat.reply('\n'.join(l))


def unsub_do(chat, match):
    chat_model = models.TelegramChat.from_aiotg(chat)

    cmd_id = ' '.join(match.groups(1))

    for sub in chat_model.subscriptions:
        if sub.resource.cmd_id == cmd_id:
            break
    else:
        return chat.reply("Whoops! That didn't work")

    res = sub.resource
    sub.delete_instance()
    msg = "Removed subscription to {}".format(res)

    if len(res.subscriptions) == 0:
        res.delete_instance()

    return chat.reply(msg)


def wipe(chat, match):
    """the bot forgets all the data about you"""
    chat_model = models.TelegramChat.from_aiotg(chat)

    for sub in chat_model.subscriptions:
        sub.delete_instance()

    chat_model.delete_instance(recursive=True)
    return chat.reply('Okay, goodbye!')


def source(chat, match):
    """info about source code"""
    return chat.reply("""
This bot is Free Software under the LGPLv3.
You can get the code from here:
https://github.com/franciscod/telegram-universal-forwarder-bot
""")


def help(chat, match):
    """view help text"""
    fns = uniquify(fn for re, fn in bot._commands)

    command_docstrings = ["/{} - {}".format(fn.__name__, fn.__doc__)
                          for fn in fns if fn.__doc__ is not None]

    return chat.reply('\n'.join([
        "Hello! This bot lets you subscribe to various feeds.",
        "Here's the commands:",
        *command_docstrings,
        "This bot is being worked on, so it may break sometimes. "
        "Contact @franciscod if you want to chat about it!"
    ]))


def base_bootup(bot):
    bot.default(default)
    bot.command("/listsubs")(listsubs)
    bot.command("/export")(export)
    bot.command("/unsub$")(unsub)
    bot.command("/unsub_(.*)")(unsub_do)
    bot.command("/wipe")(wipe)
    bot.command("/source")(source)
    bot.command('/help')(help)
    bot.command('/start')(help)
    pass


if __name__ == '__main__':
    models.create_tables()
    bot = Bot(os.environ["TG_BOT_TOKEN"])
    resources.Clock.bootup(bot)

    base_bootup(bot)
    bot.run()
