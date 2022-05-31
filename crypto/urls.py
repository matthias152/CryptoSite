from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', wallet),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('buy-crypto/', buy_cryptos, name='buycryptos'),
    path('sell-crypto/', sell_cryptos, name='sellcryptos'),
    path('register/', register_request, name='register'),
    path('transactions/', transactions, name='transactions'),
    path('transactions/pdf/', pdf_transactions, name='pdftransactions'),
]
