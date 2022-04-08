from django.shortcuts import render, redirect
from pycoingecko import CoinGeckoAPI
from .models import CryptoWallet, Balance
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView


coingecko = CoinGeckoAPI()



def register_request(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return render(request, 'index.html')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form":form})


class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return ('http://127.0.0.1:8000/')


@login_required(login_url='http://127.0.0.1:8000/login')
def show_crypto_prices(request):
    TRENDING_COINS = []
    current_crypto_values = []
    profit_loss = []
    trends = coingecko.get_search_trending()['coins']
    cryptos = CryptoWallet.objects.all()
    user_cryptos = cryptos.filter(user=request.user)
    balances = Balance.objects.all()
    user_balance = balances.get(user=request.user)
    user_final_balance = float(user_balance.balance)

    for i in user_cryptos:
        z = round(coingecko.get_price(ids=str(
        i.cryptoName).lower(), vs_currencies='usd')[str(i.cryptoName).lower()]
        ['usd'] * i.cryptoQuantity - i.quantityDollars, 3)
        profit_loss.append(z)

    for i in user_cryptos:
        z = round(coingecko.get_price(ids=str(i.cryptoName).lower(),
        vs_currencies='usd')[str(i.cryptoName).lower()]
        ['usd'] * i.cryptoQuantity, 5)
        current_crypto_values.append(z)

    for i in range(7):
        coin = trends[i]['item']['name']
        TRENDING_COINS.append(coin)

    if request.method == 'POST':
        coin_id = request.POST.get('textfield', None)
        coin = coingecko.get_price(ids=coin_id, vs_currencies='usd')[str(coin_id)]['usd']

    return render(request, "index.html", {
        'trending': TRENDING_COINS,
        'search_coin': coin,
        'ALL_CRYPTOS': cryptos,
        'current_crypto_values': current_crypto_values,
        'user_cryptos': user_cryptos,
        'user_final_balance': user_final_balance,
        'profit_loss': profit_loss,
        'user': request.user,

    })


@login_required(login_url='http://127.0.0.1:8000/login')
def buy_cryptos(request):
    if request.method == 'POST':
        if request.POST.get('cryptoNameBuy') and request.POST.get('quantityDollarsBuy'):
            balances = Balance.objects.all()
            user_balance = balances.get(user=request.user)
            user_final_balance = float(user_balance.balance)
            buying_coin = request.POST.get('cryptoNameBuy', None)
            buying_coin_exchange = coingecko.get_price(ids=buying_coin, vs_currencies='usd')[str(buying_coin)]['usd']
            quantity_bought = request.POST.get('quantityDollarsBuy')
            cryptos = CryptoWallet.objects.all()
            user_cryptos = cryptos.filter(user=request.user)
            user_cryptos_list = []
        for i in user_cryptos:
            z = str(i.cryptoName)
            user_cryptos_list.append(z)
        if float(quantity_bought) < user_final_balance:
            if str(buying_coin) in user_cryptos_list:
                y = user_cryptos.get(cryptoName=buying_coin)
                y.cryptoQuantity += float(quantity_bought) / float(buying_coin_exchange)
                y.quantityDollars += float(quantity_bought)
                y.save()
                user_balance.balance -= float(quantity_bought)
                user_balance.save()
                return render(request, 'buy-crypto.html')
            else:
                new_cryp = CryptoWallet()
                new_cryp.user = request.user
                new_cryp.cryptoName = buying_coin
                new_cryp.quantityDollars = quantity_bought
                new_cryp.cryptoQuantity = float(quantity_bought) / float(buying_coin_exchange)
                new_cryp.save()
                user_balance.balance -= float(quantity_bought)
                user_balance.save()
                return render(request, 'buy-crypto.html')
        return render(request, 'buy-crypto.html')
    return render(request, 'buy-crypto.html')


@login_required(login_url='http://127.0.0.1:8000/login')
def sell_cryptos(request):
    if request.method == 'POST':
        if request.POST.get('cryptoNameSell') and request.POST.get('cryptoQuantitySell'):
            balances = Balance.objects.all()
            user_balance = balances.get(user=request.user)
            selling_coin = request.POST.get('cryptoNameSell')
            selling_coin_exchange = coingecko.get_price(ids=selling_coin, vs_currencies='usd')[str(selling_coin)]['usd']
            selling_quantity = request.POST.get('cryptoQuantitySell')
            cryptos = CryptoWallet.objects.all()
            user_cryptos = cryptos.filter(user=request.user)
            user_cryptos_list = []
            y = user_cryptos.get(cryptoName=selling_coin)
            for i in user_cryptos:
                z = str(i.cryptoName)
                user_cryptos_list.append(z)
            if str(selling_coin) in user_cryptos_list:
                if float(y.cryptoQuantity) > float(selling_quantity):
                    y.cryptoQuantity -= float(selling_quantity)
                    y.save()
                    user_balance.balance += float(selling_quantity) * float(selling_coin_exchange)
                    user_balance.save()
                    return render(request, 'sell-crypto.html')
                else:
                    return render(request, 'sell-crypto.html')
            else:
                return render(request, 'sell-crypto.html')
        return render(request, 'sell-crypto.html')
    return render(request, 'sell-crypto.html')
