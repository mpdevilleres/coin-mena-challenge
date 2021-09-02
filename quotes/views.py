from rest_framework.status import HTTP_202_ACCEPTED
from rest_framework.views import APIView
from rest_framework.response import Response

from quotes.models import Quote
from quotes.serializers import QuotesSerializer
from quotes.tasks import retrieve_rates_from_alpha_vantage


class QuoteAPIView(APIView):

    def get(self, request, format=None):  # noqa
        """
        Return a list of all quotes.
        """
        # TODO consider adding pagination
        quotes = Quote.objects.order_by('-last_refreshed').all()
        serializer = QuotesSerializer(quotes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):  # noqa
        """
        Trigger Fetching of rates from alpha vantage
        """
        retrieve_rates_from_alpha_vantage.delay()
        return Response(status=HTTP_202_ACCEPTED)


quote_api_view = QuoteAPIView.as_view()


class QuoteLatestView(APIView):
    def get(self, request, format=None):  # noqa
        """
        Return the latest quote
        """
        quotes = Quote.objects.order_by('-last_refreshed').first()
        serializer = QuotesSerializer(quotes)
        return Response(serializer.data)


quote_latest_view = QuoteLatestView.as_view()
