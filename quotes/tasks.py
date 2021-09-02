import datetime
import pytz
from django.conf import settings
from celery.utils.log import get_task_logger
from alpha_vantage.foreignexchange import ForeignExchange
from django.utils.timezone import make_aware

from coin_mena_challenge.celery_app import app
from quotes.models import Quote

logger = get_task_logger(__name__)

FIELD_MAPPING_TABLE = {
    '1. From_Currency Code': 'from_currency_code',
    '2. From_Currency Name': 'from_currency_name',
    '3. To_Currency Code': 'to_currency_code',
    '4. To_Currency Name': 'to_currency_name',
    '5. Exchange Rate': 'exchange_rate',
    '6. Last Refreshed': 'last_refreshed',
    '7. Time Zone': 'timezone',
    '8. Bid Price': 'bid_price',
    '9. Ask Price': 'ask_price'
}


@app.task
def retrieve_rates_from_alpha_vantage():
    """
    Retrieve rates from Alpha Vantage and Store it in the database

    Sample Data from Alpha Vatange
    {
        '1. From_Currency Code': 'BTC',
        '2. From_Currency Name': 'Bitcoin',
        '3. To_Currency Code': 'USD',
        '4. To_Currency Name': 'United States Dollar',
        '5. Exchange Rate': '48327.17000000',
        '6. Last Refreshed': '2021-09-01 21:22:02',
        '7. Time Zone': 'UTC',
        '8. Bid Price': '48327.17000000',
        '9. Ask Price': '48327.18000000'
    }
    """
    foreign_exchange = ForeignExchange(key=settings.ALPHA_VANTAGE_API_KEY)
    data, _ = foreign_exchange.get_currency_exchange_rate(from_currency='BTC', to_currency='USD')
    if not data:
        logger.warning('enable to get rates from alpha vantage')

    # since the keys from alpha_vantage is not te same case and format to our database we need to transform it
    # we have multiple approach to address the transformation and we will choice to use a mapping table
    # for the reason that it is explicit and if at some point alpha vantage change we will get an explicit error
    # and can easily update the mapping table to address the issue
    # we don't use dict.get() here so that if the key is missing in the table we get an error
    data = {FIELD_MAPPING_TABLE[k]: v for k, v in data.items()}

    timezone = pytz.timezone(data.pop('timezone'))
    last_refreshed = datetime.datetime.strptime(data['last_refreshed'], '%Y-%m-%d %H:%M:%S')
    data['last_refreshed'] = make_aware(last_refreshed, timezone)
    # convert exchange_rate, bid_price, ask_price to float
    data = {k: float(v) if k in ['exchange_rate', 'bid_price', 'ask_price'] else v for k, v in data.items()}

    quote = Quote(**data)
    quote.save()
