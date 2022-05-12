from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BalanceViewSet, CryptoWalletViewSet, TransactionViewSet
from .views import BuyPriceDetail, UserViewSet, CryptoWalletDetail


router = DefaultRouter()
router.register('balance', BalanceViewSet, basename='balance')
router.register('crypto', CryptoWalletViewSet, basename='crypto')
router.register('transaction', TransactionViewSet, basename='transaction')
router.register('user', UserViewSet, basename='user')

urlpatterns = [
    path('viewset/', include(router.urls)),
    path('viewset/<int:pk>/', include(router.urls)),
    path('generic/crypto/', CryptoWalletDetail.as_view()),
    path('generic/crypto/<int:id>/', CryptoWalletDetail.as_view()),
    path('generic/buyprice/', BuyPriceDetail.as_view()),
    path('generic/buyprice/<int:id>/', BuyPriceDetail.as_view()),

]
