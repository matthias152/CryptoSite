from django.urls import path
from .views import *

urlpatterns = [
    path('', show_crypto_prices),
    path('buy-crypto', buy_cryptos),
    path('sell-crypto', sell_cryptos),
]
