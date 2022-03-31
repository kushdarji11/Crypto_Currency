from django.urls import path
from . import views

app_name = 'CryptoApp'
urlpatterns = [
    path('', views.index, name="index"),
    path('chart/', views.chart, name="chart"),
    path('coinDetail/<str:id>/<str:current_price>/<str:market_cap>', views.coinDetail, name="coinDetail")
]
