from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth

from .views import CancelView, SuccessView, ProductLandingPageView, CreateCheckoutSessionView

app_name = 'CryptoApp'
urlpatterns = [
    path('', views.index, name="index"),
    path('chart/', views.chart, name="chart"),
    path('coinDetail/<str:id>/<str:current_price>/<str:market_cap>', views.coinDetail, name="coinDetail"),
    path('login/', views.Login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.Logout, name='logout'),
    path('BuyForm/<str:id>/<str:price>/<str:market>', views.fetchFormData, name="fetchFormData"),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('landingPages/', ProductLandingPageView.as_view(), name='landing-page'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('landingPage/', views.handleLandingPage, name="landingPage")
]
