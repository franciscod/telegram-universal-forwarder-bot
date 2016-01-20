from models import Resource, IntegerField, TelegramChat
from datetime import datetime

import asyncio


class Clock(Resource):
    interval = IntegerField(unique=True)

    @property
    def seconds_to_next_tick(self):
        now = datetime.utcnow().timestamp()
        return abs(int(now % (self.interval * -60)))

    async def loop(self, bot):
        def tick(bot):
            futs = []
            for s in self.subscriptions:
                chat = s.subscriber.aiotg_chat(bot)
                futs.append(
                    chat.send_text("The {} minute clock is ticking!".format(self.interval)))

            return asyncio.gather(*futs)

        while True:
            await asyncio.sleep(self.seconds_to_next_tick)
            await tick(bot)

    def start(self, bot):
        asyncio.ensure_future(self.loop(bot))

    @classmethod
    def bring_up(cls, interval):
        try:
            interval = int(interval)
        except ValueError:
            raise TypeError

        if interval < 1:
            raise ValueError

        self, created = cls.create_or_get(interval=interval)
        return self


def init(bot):
    Clock.create_table(fail_silently=True)

    for clock in Clock.select():
        clock.start(bot)

    bind(bot)


def bind(bot):
    @bot.command(r"/clocksub(.*)")
    def clocksub(chat, match):
        """subscribes to one or more clocks"""
        minutes = match.group(1).split()

        if not minutes:
            return chat.reply("Use /clocksub <minute> [<minute>...]")

        futs = []

        for minute in minutes:

            try:
                clock = Clock.bring_up(minute)
            except TypeError:
                futs.append(
                    chat.reply((
                        "Adding a clock with '{}' minutes didn't work. "
                        "Please provide an integer amount of like 1 or 5 or 60."
                    ).format(minute)))
                continue
            except ValueError:
                futs.append(
                    chat.reply(
                        "You can't subscribe to a clock with intervals less than 1!"))

            clock.start(bot)
            subscribed = clock._subscribe(TelegramChat.from_aiotg(chat))

            if subscribed:
                futs.append(
                    chat.reply((
                        "OK! Subscribed to a clock with interval of {} minutes."
                    ).format(minute)))
            else:
                futs.append(
                    chat.reply((
                        "You were already subscribed to a clock with interval of {} minutes!"
                    ).format(minute)))

        return asyncio.gather(*futs)

    @bot.command(r"/clockunsub")
    def clockunsub(chat, match):
        """unsubscribes from a clock"""
        # TODO get the chat subscriptions and show them as clickable commands
        # with /clockunsub_1, /clockunsub_2. /clockunsub_3 and so on
        # TODO potentially this would use a custom keyboard
        pass

    @bot.command(r"/clockunsub_(.*)")
    def unsub_do(chat, match):
        # minute = match.group(1)
        # FIXME sublogic.unsubscribe(telegram_chat_id=chat.id, clock_minute=minute)
        pass
