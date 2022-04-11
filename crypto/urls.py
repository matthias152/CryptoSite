from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', wallet),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('buy-crypto', buy_cryptos),
    path('sell-crypto', sell_cryptos),
    path('register', register_request),
    path('transactions', transactions),
]
