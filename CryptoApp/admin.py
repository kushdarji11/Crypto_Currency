from django.contrib import admin
from .models import Product

# Register your models here.
from CryptoApp.models import Portfolio

admin.site.register(Portfolio)
admin.site.register(Product)

