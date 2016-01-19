import datetime
from peewee import (Model, DateTimeField, ForeignKeyField, CharField, IntegerField)
from playhouse.gfk import Model as GFKModel, GFKField, ReverseGFK


class Meta(Model):
    version = IntegerField(default=1)


class Subscription(GFKModel):
    known_at = DateTimeField(default=datetime.datetime.now)

    subscriber_type = CharField(null=True)
    subscriber_id = IntegerField(null=True)
    subscriber = GFKField('subscriber_type', 'subscriber_id')

    resource_type = CharField(null=True)
    resource_id = IntegerField(null=True)
    resource = GFKField('resource_type', 'resource_id')

    last_update_type = CharField(null=True)
    last_update_id = IntegerField(null=True)
    last_update = GFKField('last_update_type', 'last_update_id')


class Feed(GFKModel):
    known_at = DateTimeField(default=datetime.datetime.now)
    subscriptions = ReverseGFK(Subscription, 'resource_type', 'resource_id')

    url = CharField(unique=True)
    title = CharField()


class Post(GFKModel):
    known_at = DateTimeField(default=datetime.datetime.now)
    feed = ForeignKeyField(Feed, related_name='updates')

    guid = CharField(unique=True)
    title = CharField()
    link = CharField()
    description = CharField()
    published = DateTimeField()  # TODO: feedparser will output a tuple


class TelegramChat(GFKModel):
    known_at = DateTimeField(default=datetime.datetime.now)
    subscriptions = ReverseGFK(Subscription, 'subscriber_type', 'subscriber_id')

    chat_id = IntegerField(unique=True)
    last_contact = DateTimeField(default=datetime.datetime.now)

    def touch_last_contact(self):
        self.last_contact = datetime.datetime.now()
        self.save()


def create_tables():
    for t in (Feed, TelegramChat, Subscription):
        t.create_table(fail_silently=True)
