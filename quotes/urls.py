from django.urls import path

from quotes.views import (
    quote_api_view,
    quote_latest_view
)

urlpatterns = [
    path("", view=quote_api_view),
    path("latest/", view=quote_latest_view),
]
