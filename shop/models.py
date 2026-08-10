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
