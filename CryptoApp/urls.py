from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth

app_name = 'CryptoApp'
urlpatterns = [
    path('', views.index, name="index"),
    path('chart/', views.chart, name="chart"),
    path('coinDetail/<str:id>/<str:current_price>/<str:market_cap>', views.coinDetail, name="coinDetail"),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('buyForm/<str:id>/<str:price>/<str:market>', views.fetchFormData, name='fetchFormData')
]
