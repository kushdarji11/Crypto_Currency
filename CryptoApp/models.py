from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Portfolio(models.Model):
    coin_id = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    market_cap = models.CharField(max_length=200)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_price_int = models.FloatField(default=0)

    def __str__(self):
        return f"{self.client} {self.coin_id} {self.price}"
