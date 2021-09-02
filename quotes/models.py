from django.db import models


class Quote(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    # iso standard for currency code is 3 characters
    # https://www.iban.com/currency-codes
    from_currency_code = models.CharField(max_length=3)
    from_currency_name = models.TextField()
    to_currency_code = models.CharField(max_length=3)
    to_currency_name = models.TextField()
    # if exchange_rate becomes the bottleneck
    # we can consider implementing wei,
    # same way most cryptocurrency are handled
    # https://www.investopedia.com/terms/w/wei.asp
    exchange_rate = models.DecimalField(max_digits=16, decimal_places=8)
    bid_price = models.DecimalField(max_digits=16, decimal_places=8)
    ask_price = models.DecimalField(max_digits=16, decimal_places=8)
    last_refreshed = models.DateTimeField()
