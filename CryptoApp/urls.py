from django.urls import path
from . import views

app_name = 'CryptoApp'
urlpatterns = [
    path('', views.index, name="index")
]