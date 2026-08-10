import logging
from django.db import models

logger = logging.getLogger(__name__)

class Item(models.Model):
    name = models.CharField()
    description = models.TextField()
    price = models.DecimalField()
    def __str__(self):
        return self.name
