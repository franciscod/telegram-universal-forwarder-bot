import asyncio
from datetime import datetime

from .base import BaseResource
from peewee import IntegerField


class Clock(BaseResource):
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
    def validate(cls, arg):
        error = False

        if not arg:
            error = True
        try:
            arg = int(arg)
        except ValueError:
            error = True
        else:
            if arg < 1:
                error = True

        if error:
            raise RuntimeError('Please provide a positive integer (like 1, 5 or 60)')

    @classmethod
    def bring_up(cls, bot, arg):
        arg = int(arg)
        clock, created = cls.create_or_get(interval=arg)

        if created:
            clock.start(bot)

        return clock

    @property
    def sub_command(self):
        return '/{}sub {}'.format(self.name(), self.interval)

    def __str__(self):
        return "Clock with {}-minute interval".format(self.interval)
