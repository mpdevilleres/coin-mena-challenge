from unittest.mock import patch

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from quotes.models import Quote
from quotes.tests.factories import QuoteFactory

User = get_user_model()


class QuoteTestCase(APITestCase):

    def setUp(self):
        super(QuoteTestCase, self).setUp()
        self.quotes = QuoteFactory.create_batch(20)
        self.user = User.objects.create_user('random_user', 'random_user@random_domain.com', 'random_password')

    def tearDown(self):
        self.user.delete()
        Quote.objects.all().delete()
        super(QuoteTestCase, self).tearDown()

    @property
    def headers(self):
        response = self.client.post(
            '/api/v1/token/',
            data={
                'username': 'random_user',
                'password': 'random_password',
            }
        )
        payload = response.json()
        return {'HTTP_AUTHORIZATION': f"Bearer {payload['access']}"}

    @patch('quotes.views.retrieve_rates_from_alpha_vantage.delay')
    def test_trigger_retrieve_rates_from_alpha_vantage(self, mock_retrieve_rates_from_alpha_vantage):
        response = self.client.post('/api/v1/quotes/', **self.headers)
        assert response.status_code == 202
        assert mock_retrieve_rates_from_alpha_vantage.call_count == 1

    def test_get_quote_list(self):
        response = self.client.get('/api/v1/quotes/', **self.headers)
        assert response.status_code == 200

        payload = response.json()
        assert isinstance(payload, list)
        assert len(payload) == 20

        # check if sorting is correct
        last_refreshed_dates = [i['last_refreshed'] for i in payload]
        assert last_refreshed_dates == sorted(last_refreshed_dates, reverse=True)

    def test_get_quote_latest(self):
        response = self.client.get('/api/v1/quotes/latest/', **self.headers)
        assert response.status_code == 200

        payload = response.json()
        assert isinstance(payload, dict)

        expected_quote = Quote.objects.order_by('-last_refreshed').first()
        actual_quote = Quote(**payload)
        assert expected_quote == actual_quote
