from django.shortcuts import render
from pycoingecko import CoinGeckoAPI

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

    })
