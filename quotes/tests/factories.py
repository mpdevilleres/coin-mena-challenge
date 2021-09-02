import random
import datetime

import pytz
import factory

from quotes.models import Quote


def random_datetime(
        start=datetime.datetime(2000, 1, 1, tzinfo=pytz.UTC),
        end=datetime.datetime(2025, 12, 31, tzinfo=pytz.UTC)
):
    random_number_of_days = random.randrange((end - start).days)
    return start + datetime.timedelta(days=random_number_of_days)


class QuoteFactory(factory.django.DjangoModelFactory):
    from_currency_code = 'BTC'
    from_currency_name = 'Bitcoin'
    to_currency_code = 'USD'
    to_currency_name = 'United States Dollar'
    exchange_rate = factory.LazyAttribute(lambda x: random.uniform(10000.00000001, 999999.99999999))
    bid_price = factory.LazyAttribute(lambda x: random.uniform(10000.00000001, 999999.99999999))
    ask_price = factory.LazyAttribute(lambda x: random.uniform(10000.00000001, 999999.99999999))
    last_refreshed = factory.LazyAttribute(lambda x: random_datetime())

    class Meta:
        model = Quote
