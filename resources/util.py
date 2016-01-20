import asyncio
from contextlib import contextmanager

from models import Subscription


@contextmanager
def future_replies(chat):
    texts = []

    yield (lambda t: texts.append(t))

    asyncio.ensure_future(
        asyncio.gather(*[chat.reply(text) for text in texts])
    )


@contextmanager
def future_texts(chat):
    texts = []

    yield (lambda t: texts.append(t))

    asyncio.ensure_future(
        asyncio.gather(*[chat.send_text(text) for text in texts])
    )


def subscribe(subscriber, resource):
    # HACK workaround for using get_or_create / create_or_get with GFKFields.
    try:
        # HACK workaround for querying equality of GFKField. I'd love to do the following:
        # Subscription.get(
        #     (Subscription.subscriber == subscriber) &
        #     (Subscription.resource == resource))

        sub = Subscription.get(
            (Subscription.subscriber_id == subscriber._get_pk_value()) &
            (Subscription.subscriber_type == subscriber._meta.db_table) &
            (Subscription.resource_id == resource._get_pk_value()) &
            (Subscription.resource_type == resource._meta.db_table))

        created = False

    except Subscription.DoesNotExist:
        sub = Subscription.create(
            subscriber=subscriber,
            resource=resource,
        )

        created = True

    return sub, created
