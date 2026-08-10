import logging
from django.db import models

logger = logging.getLogger(__name__)

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(upload_to="item_pictures/", null=True, blank=True)
    def __str__(self):
        return self.name
class Tax(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    stripe_tax_rate_id = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return f"{self.name} ({self.percentage}%)"
class Order(models.Model):
    items = models.ManyToManyField(Item, related_name="orders")
    tax = models.ForeignKey(Tax, null=True, blank=True, on_delete=models.SET_NULL, related_name="orders")
    def total_price(self):
        return sum(item.price for item in self.items.all())
    def __str__(self):
        return f"Order: {self.id}"