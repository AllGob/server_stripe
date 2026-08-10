import logging
from django.contrib import admin
from .models import Item, Order,Tax

logger = logging.getLogger(__name__)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price")
    search_fields = ("name",)
@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "percentage","stripe_tax_rate_id")
    readonly_fields = ("stripe_tax_rate_id",)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "total_price","tax")
    filter_horizontal = ("items",)