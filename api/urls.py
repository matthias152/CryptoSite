from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BalanceViewSet, CryptoWalletViewSet, TransactionViewSet
from .views import BuyPriceViewSet, UserViewSet


router = DefaultRouter()
router.register('balance', BalanceViewSet, basename='balance')
router.register('crypto', CryptoWalletViewSet, basename='crypto')
router.register('transaction', TransactionViewSet, basename='transaction')
router.register('buyprice', BuyPriceViewSet, basename='buyprice')
router.register('user', UserViewSet, basename='user')

urlpatterns = [
    path('viewset/', include(router.urls)),
    path('viewset/<int:pk>/', include(router.urls)),

]
