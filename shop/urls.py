import logging
from django.urls import path
from . import views

logger = logging.getLogger(__name__)
urlpatterns = [
    path("buy/<int:item_id>/", views.buy_item, name="buy-item"),
]
