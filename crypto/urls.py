from django.urls import path
from .views import CustomLoginView, buy_cryptos, sell_cryptos, wallet
from .views import register_request, transactions_history, pdf_transactions, pdf_transactions_email
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', wallet, name='wallet'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('buy-crypto/', buy_cryptos, name='buycryptos'),
    path('sell-crypto/', sell_cryptos, name='sellcryptos'),
    path('register/', register_request, name='register'),
    path('transactions/', transactions_history, name='transactions'),
    path('transactions/pdf/', pdf_transactions, name='pdftransactions'),
    path('transactions/emailpdf', pdf_transactions_email, name='emailatt')
]
