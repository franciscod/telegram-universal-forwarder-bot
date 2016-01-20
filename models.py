import datetime
from peewee import (Model, DateTimeField, CharField, IntegerField)
from playhouse.gfk import Model as GFKModel, GFKField, ReverseGFK

from aiotg import TgChat


class Meta(Model):
    version = IntegerField(default=1)


class BaseModel(GFKModel):
    known_at = DateTimeField(default=datetime.datetime.now)


class Subscription(BaseModel):
    subscriber_type = CharField(null=True)
    subscriber_id = IntegerField(null=True)
    subscriber = GFKField('subscriber_type', 'subscriber_id')

    resource_type = CharField(null=True)
    resource_id = IntegerField(null=True)
    resource = GFKField('resource_type', 'resource_id')

    extra_type = CharField(null=True)
    extra_id = IntegerField(null=True)
    extra = GFKField('extra_type', 'extra_id')

    class Meta:
        indexes = (
            ((
                'subscriber_type',
                'subscriber_id',
                'resource_type',
                'resource_id',
            ), True),
        )


class TelegramChat(BaseModel):
    subscriptions = ReverseGFK(Subscription, 'subscriber_type', 'subscriber_id')

    chat_id = IntegerField(unique=True)
    chat_type = CharField()
    last_contact = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def from_aiotg(cls, chat):
        obj, _ = cls.create_or_get(chat_id=chat.id, chat_type=chat.type)
        return obj

    def touch_last_contact(self):
        self.last_contact = datetime.datetime.now()
        self.save()

    def aiotg_chat(self, bot):
        return TgChat(bot, self.chat_id, self.chat_type)


def create_tables():
    for t in (Subscription, TelegramChat):
        t.create_table(fail_silently=True)
