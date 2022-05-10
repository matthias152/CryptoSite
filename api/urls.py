from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BalanceViewSet

router = DefaultRouter()
router.register('balance', BalanceViewSet, basename='balance')

urlpatterns = [
    path('viewset/', include(router.urls)),
    path('viewset/<int:pk>/', include(router.urls))

]
