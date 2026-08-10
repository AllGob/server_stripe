import logging
from django.contrib import admin
from django.urls import include, path
logger = logging.getLogger(__name__)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("shop.urls")),
]
