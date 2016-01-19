import models


def init():
    models.create_tables()


def subscribe(telegram_chat_id=None, feed_url=None):
    print("STUB: subscribe")  # TODO


def unsubscribe(telegram_chat_id=None, feed_url=None):
    print("STUB: unsubscribe")  # TODO
