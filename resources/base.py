from models import BaseModel, Subscription, TelegramChat
from playhouse.gfk import ReverseGFK

from .util import future_replies, subscribe


class BaseResource(BaseModel):
    subscriptions = ReverseGFK(Subscription, 'resource_type', 'resource_id')

    @property
    def _should_run(self):
        return len(self.subscriptions) > 0

    @classmethod
    def name(cls):
        return cls.__name__.lower()

    @property
    def cmd_id(self):
        raise NotImplemented

    @classmethod
    def bootup(cls, bot):

        cls.create_table(fail_silently=True)

        for res in cls.select():
            res.start(bot)

        def subfn(chat, match):
            chat_model = TelegramChat.from_aiotg(chat)
            args = match.group(1).strip()

            with future_replies(chat) as add_reply:
                try:
                    cls.validate(args)
                except RuntimeError as e:
                    msg = ''.join(e.args)
                    add_reply("Whoops, that didn't work! {}".format(msg))
                    return

                res = cls.bring_up(bot, args)
                sub, sub_created = subscribe(chat_model, res)
                add_reply(
                    "OK, subscribed!" if sub_created
                    else "You were already subscribed to that one!")

        name = cls.name()
        subfn.__name__ = "sub_" + name
        subfn.__doc__ = "subscribe to a " + name
        bot.command("/" + subfn.__name__ + "(.*)")(subfn)
