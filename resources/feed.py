import asyncio


def init(bot):
    @bot.command(r"/feedsub(.*)")
    def feedsub(chat, match):
        """subscribes to a feed"""
        urls = match.group(1).split()

        if not urls:
            return chat.reply("Use /feedsub <url> [<url>...]")

        for url in urls:
            asyncio.ensure_future(chat.reply("Subscribing to {}...".format(url)))
            # FIXME sublogic.subscribe(telegram_chat_id=chat.id, feed_url=url)

            asyncio.ensure_future(chat.reply("Done! Subscribed to FEED TITLE".format(url)))  # TODO

    @bot.command(r"/feedunsub")
    def feedunsub(chat, match):
        """unsubscribes from a feed"""
        # TODO get the chat subscriptions and show them as clickable commands
        # with /feedunsub_1, /feedunsub_2. /feedunsub_3 and so on
        # TODO potentially this would use a custom keyboard
        pass

    @bot.command(r"/feedunsub_(.*)")
    def unsub_do(chat, match):
        # url = match.group(1)
        # FIXME sublogic.unsubscribe(telegram_chat_id=chat.id, feed_url=url)
        pass
