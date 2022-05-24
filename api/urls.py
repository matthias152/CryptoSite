from django.urls import path
from .views import UserBalance, UserCryptoWallet, UserTransactions, UserBuyPrice
from .views import RegisterView, BalancesView, TransactionsView
from. views import CryptoWalletView, BuyPriceView, UsersView


urlpatterns = [
    #  USER
    path('crypto/user/', UserCryptoWallet.as_view(), name="cryptos-user"),
    path('crypto/user/<int:id>/', UserCryptoWallet.as_view(), name="cryptos-user-detail"),
    path('buyprice/user/', UserBuyPrice.as_view(), name="buyprices-user"),
    path('buyprice/user/<int:id>/', UserBuyPrice.as_view(), name="buyprices-user-detail"),
    path('transaction/user/', UserTransactions.as_view(), name="transaction-user"),
    path('transaction/user/<int:id>/', UserTransactions.as_view(), name="transaction-user-detail"),
    path('balance/user/', UserBalance.as_view(), name="balance-user"),
    path('balance/user/<int:id>/', UserBalance.as_view(), name="balance-user-detail"),
    path('register/', RegisterView.as_view(), name="registersite"),
    #  ADMIN
    path('users/', UsersView.as_view()),
    path('users/<int:id>', UsersView.as_view()),
    path('crypto/', CryptoWalletView.as_view(), name="cryptos"),
    path('crypto/<int:id>', CryptoWalletView.as_view(), name="cryptos-detail"),
    path('buyprice/', BuyPriceView.as_view()),
    path('buyprice/<int:id>', BuyPriceView.as_view()),
    path('transaction/', TransactionsView.as_view()),
    path('transaction/<int:id>', TransactionsView.as_view()),
    path('balance/', BalancesView.as_view()),
    path('balance/<int:id>', BalancesView.as_view()),

]
