import re
from math import floor

from typing import Any

from django.conf import settings
import xml
from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
import json

from django.template.loader import get_template
from django.utils.datetime_safe import date
from django.views import View
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


from CryptoApp.forms import UserRegisterForm, BuyForm
from CryptoApp.models import Portfolio


def chart(request):
    dict_table = []
    api_data = requests.get('https://api.coingecko.com/api/v3/search/trending')
    data = json.loads(api_data.content)
    labels = []
    price_btc = []
    market_cap_rank = []
    for key, values in data.items():
        for item in values:
            for k, v in item.items():
                for _, _ in v.items():
                    if v not in dict_table:
                        dict_table.append(v)
                    if v['name'] not in labels:
                        labels.append(v['name'])
                    if v['market_cap_rank'] not in market_cap_rank:
                        market_cap_rank.append(v['market_cap_rank'])
                    if v['price_btc'] not in price_btc:
                        price_btc.append(v['price_btc'])

    return render(request, 'chart.html', {'dict_table': dict_table, 'labels': labels, 'chartData': market_cap_rank,
                                          'secondChartData': price_btc})


def getUserDetails(request):
    global coin_id, total_price
    dict_item = {}
    list_dict = []
    labels = []
    chartData = []

    getDetails = Portfolio.objects.filter(client_id=request.user)

    for coin in getDetails.all():
        coin_id = coin.coin_id

        dict_item['id'] = coin_id
        if coin_id not in labels:
            labels.append(coin_id)

        total_price = sum(coin.total_price_int for coin in Portfolio.objects.filter(client_id=request.user)
                          .filter(coin_id=coin_id))
        if total_price not in chartData:
            int_price_int = total_price
            chartData.append(int_price_int)
        total_price_str = "{:,}".format(total_price)
        dict_item['price'] = total_price_str

        if dict_item not in list_dict:
            list_dict.append(dict_item)
            dict_item = {}
    return render(request, 'portfolio.html', {'list_dict': list_dict, 'labels': labels, 'chartData': chartData})


def coinDetail(request, id, current_price, market_cap):
    context = {}
    lowercaseId = id.lower()
    api_data = requests.get("https://api.coingecko.com/api/v3/coins/" + lowercaseId + "")
    data = json.loads(api_data.content)
    api_chart = requests.get(
        "https://api.coingecko.com/api/v3/coins/" + lowercaseId + "/market_chart?vs_currency=usd&days=12")
    chart_data = json.loads(api_chart.content)
    market_cap_val = []
    if 'image' in data:
        for key, value in data['image'].items():
            if key == 'small':
                img_val = value
        for key, value in data['description'].items():
            if key == 'en':
                desc = value
        for key, values in chart_data.items():
            if key == 'prices':
                for inner_value in values:
                    market_cap_val.append(inner_value[1])
        cleanExpression = re.compile('<.*?>')
        cleantext = re.sub(cleanExpression, '', desc)
        context['market_cap_val'] = market_cap_val
        context['labels'] = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7', 'Day 8', 'Day 9', 'Day 10',
                             'Day 11', 'Day 12']
        context['desc'] = cleantext
        context['img_val'] = img_val
        context['market_cap_rank'] = data['market_cap_rank']
        context['liquidity_score'] = data['liquidity_score']
        context['coin_id'] = id
        context['current_price'] = current_price
        context['market_cap_size'] = market_cap
    else:
        context['coin_id'] = id
        context['current_price'] = current_price
        context['market_cap_size'] = market_cap
    return render(request, 'detail.html', context)


def index(request):
    global active_cryptocurrencies, market_cap_change_percentage_24h_usd
    market_cap_value = 0
    d_list = {}

    api_baseData = requests.get("https://api.coingecko.com/api/v3/global")
    api_data = requests.get(
        "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=1h")
    data = json.loads(api_data.content)
    baseData = json.loads(api_baseData.content)

    for key, values in baseData.items():
        for inner_Key, inner_val in values.items():
            d_list[inner_Key] = inner_val
    active_cryptocurrencies = d_list['active_cryptocurrencies']
    market_cap_change_percentage_24h_usd = d_list['market_cap_change_percentage_24h_usd']

    for key, value in d_list['total_market_cap'].items():
        market_cap_value += value
    page_num = request.GET.get('page', 1)
    paginator = Paginator(data, 10)

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'page_obj': page_obj, 'active_cryptocurrencies': active_cryptocurrencies,
                                          'market_cap_change_percentage_24h_usd': market_cap_change_percentage_24h_usd,
                                          'total_market_cap': market_cap_value})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            htmly = get_template('Email.html')
            d = {'username': username}
            subject, from_email, to = 'welcome', 'your_email@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('CryptoApp:login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form, 'title': 'Reqister here'})


def Logout(request):
    logout(request)
    return redirect('CryptoApp:index')


def Login(request):
    if request.method == 'POST':

        # AuthenticationForm_can_also_be_used__

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('CryptoApp:index')
        else:
            messages.info(request, f'account done not exit plz sign in')
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'title': 'log in'})


def fetchFormData(request, id, price, market):
    form = BuyForm()
    market_price = "{:,}".format(float(market))
    market_price_str = '$' + market_price
    curr_price = "{:,}".format(float(price))
    curr_price_str = '$' + curr_price

    form.fields['coin_id'].initial = id
    form.fields['price'].initial = curr_price_str
    form.fields['market_cap'].initial = market_price_str
    return render(request, 'buyForm.html', {'form': form, 'curr_price': price})


def handleLandingPage(request):
    global totalPriceValue, totalPrice, selected_currency
    if request.method == "POST":
        form = BuyForm(request.POST)
        form.instance.client = request.user
        if form.is_valid():
            selected_currency = form.cleaned_data.get("coin_id")
            current_price = form.cleaned_data.get("price")
            current_price_no_dollar = current_price.replace("$", "")
            current_price_no_dollar_comma = current_price_no_dollar.replace(",", "")
            current_price_int = float(current_price_no_dollar_comma)
            quantity_str = request.POST.get('click')
            quantity = float(quantity_str)
            totalPrice = (current_price_int * quantity)
            totalPrice_str = '$' + str(totalPrice)
            form.instance.price = totalPrice_str
            form.instance.total_price_int = totalPrice
            form.save()
    return redirect('CryptoApp:index')
