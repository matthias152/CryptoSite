from django.shortcuts import render
from pycoingecko import CoinGeckoAPI
from .models import CryptoWallet, CashWallet

# Create your views here.
coingecko = CoinGeckoAPI()


def color_counting(price):
    if price > 0:
        return "#77ff00"
    elif price < 0:
        return "red"
    else:
        return "gray"


def show_crypto_prices(request):
    TRENDING_COINS = []
    trends = coingecko.get_search_trending()['coins']
    cryptos = CryptoWallet.objects.all()
    crypto_values = []

    for i in cryptos:
        z = coingecko.get_price(ids=str(i.cryptoName).lower(), vs_currencies='usd')[str(i.cryptoName).lower()]['usd'] * i.cryptoQuantity
        crypto_values.append(z)

    print(crypto_values)
    # print(cryptos)
    # current_prices = []
    #
    # for j in cryptos:
    #     name = j.getattr(CryptoWallet, 'cryptoName')
    #     print(j)
    #     print(name)
    #     quan = j.getattr(CryptoWallet, 'quantityDollars')
    #     print("good")
    #     fina = coingecko.get_price(ids=name, vs_currencies='usd')[str(name)]['usd']
    #     finalprice = quan / fina
    #     current_prices.append(finalprice)
    #
    for i in range(7):
        coin = trends[i]['item']['name']
        TRENDING_COINS.append(coin)

    bitcoin = coingecko.get_price(ids='bitcoin', vs_currencies='usd')['bitcoin']['usd']
    btcdiff = (bitcoin * 0.02437757945262583) - 1000
    btccolor = color_counting(btcdiff)
    ethereum = coingecko.get_price(ids='ethereum', vs_currencies='usd')['ethereum']['usd']
    ethdiff = (ethereum * 0.17805570294610965) - 500
    ethcolor = color_counting(ethdiff)
    stellar = coingecko.get_price(ids='stellar', vs_currencies='usd')['stellar']['usd']
    xlmdiff = (stellar * 1591.1742866235281) - 300
    xlmcolor = color_counting(xlmdiff)
    ripple = coingecko.get_price(ids='ripple', vs_currencies='usd')['ripple']['usd']
    ripplediff = (ripple * 565.7303201279304) - 450
    ripplecolor = color_counting(ripplediff)
    total = btcdiff + ethdiff + xlmdiff + ripplediff
    totalcolor = color_counting(total)

    if request.method == 'POST':
        coin_id = request.POST.get('textfield', None)
        coin = coingecko.get_price(ids=coin_id, vs_currencies='usd')[str(coin_id)]['usd']


    return render(request, "index.html", {
        'btc': bitcoin,
        'btc_at_buy': 40904,
        'btc_diff': round(btcdiff, 5),
        'btc_color': btccolor,
        'eth': ethereum,
        'eth_at_buy': 2806,
        'eth_diff': round(ethdiff, 5),
        'eth_color': ethcolor,
        'xlm': stellar,
        'xlm_at_buy': 0.188577,
        'xlm_diff': round(xlmdiff, 5),
        'xlm_color': xlmcolor,
        'xrp': ripple,
        'xrp_at_buy': 0.795633,
        'xrp_diff': round(ripplediff, 5),
        'xrp_color': ripplecolor,
        'totalpl': round(total, 5),
        'total_color': totalcolor,
        'trending': TRENDING_COINS,
        'search_coin': coin,
        'ALL_CRYPTOS': cryptos,
        # 'current': current_prices,
        'crypto_values': crypto_values,

    })


def buy_cryptos(request):
    if request.method == 'POST':
        if request.POST.get('cryptoName') and request.POST.get('quantityDollars'):
            buying_coin = request.POST.get('cryptoName', None)
            final_coin = coingecko.get_price(ids=buying_coin, vs_currencies='usd')[str(buying_coin)]['usd']
            quantity_bought = request.POST.get('quantityDollars')
            cryp = CryptoWallet()
            cryp.cryptoName = request.POST.get('cryptoName')
            cryp.quantityDollars = request.POST.get('quantityDollars')
            cryp.cryptoQuantity =  float(quantity_bought) / float(final_coin)
            cryp.save()
            return render(request, 'buy-crypto.html')
        else:
            return render(request, 'buy-crypto.html')

    return render(request, "buy-crypto.html")
