from django.shortcuts import render, redirect
from pycoingecko import CoinGeckoAPI
from .models import CryptoWallet, Balance
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView


# Create your views here.
coingecko = CoinGeckoAPI()


def color_counting(price):
    if price > 0:
        return "#77ff00"
    elif price < 0:
        return "red"
    else:
        return "gray"


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
    user_balance = balances.filter(user=request.user)

    for i in user_cryptos:
        z = i.quantityDollars - coingecko.get_price(ids=str(i.cryptoName).lower(), vs_currencies='usd')[str(i.cryptoName).lower()]['usd'] * i.cryptoQuantity
        profit_loss.append(z)

    for i in user_cryptos:
        z = coingecko.get_price(ids=str(i.cryptoName).lower(), vs_currencies='usd')[str(i.cryptoName).lower()]['usd'] * i.cryptoQuantity
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
        'user_balance': user_balance,
        'profit_loss': profit_loss,
        'user': request.user,

    })


@login_required(login_url='http://127.0.0.1:8000/login')
def buy_cryptos(request):
    if request.method == 'POST':
        if request.POST.get('cryptoNameBuy') and request.POST.get('quantityDollarsBuy'):
            buying_coin = request.POST.get('cryptoNameBuy', None)
            final_coin = coingecko.get_price(ids=buying_coin, vs_currencies='usd')[str(buying_coin)]['usd']
            quantity_bought = request.POST.get('quantityDollarsBuy')
            cryp = CryptoWallet()
            cryp.user = request.user
            cryp.cryptoName = request.POST.get('cryptoNameBuy')
            cryp.quantityDollars = request.POST.get('quantityDollarsBuy')
            cryp.cryptoQuantity = float(quantity_bought) / float(final_coin)
            cryp.save()
            return render(request, 'buy-crypto.html')
        else:
            return render(request, 'buy-crypto.html')

    return render(request, "buy-crypto.html")


@login_required(login_url='http://127.0.0.1:8000/login')
def sell_cryptos(request):
    if request.method == 'POST':
        if request.POST.get('cryptoNameSell') and request.POST.get('cryptoQuantitySell'):
            selling_coin = request.POST.get('cryptoNameSell')
            print(selling_coin)
            selling_coin_quant = request.POST.get('cryptoQuantitySell')
            print(selling_coin_quant)
            cryp = CryptoWallet()
            cryptosell = cryp.objects.get(name=str(selling_coin))
            print(cryptosell)
            cryptosell.user = request.user
            cryptosell.cryptoQuantity = float(selling_coin_quant)
            cryptosell.save()
            return render(request, 'sell-crypto .html')
        else:
            return render(request, 'sell-crypto.html')

    return render(request, 'sell-crypto.html')
