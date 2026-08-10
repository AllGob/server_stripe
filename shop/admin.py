import logging
from django.contrib import admin
from .models import Item

logger = logging.getLogger(__name__)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price")
    search_fields = ("name",)
