from django.shortcuts import render
from django.shortcuts import get_object_or_404
from crypto.models import Balance, CryptoWallet, Transaction, BuyPrice, User
from django.http import HttpResponse
from rest_framework import viewsets, generics, mixins, status
from rest_framework.response import Response
from crypto.serializers import BalanceSerializer, CryptoWalletSerializer
from crypto.serializers import TransactionSerializer, BuyPriceSerializer, UserSerializer
from crypto.serializers import RegisterSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import AllowAny


#  USER
class UserCryptoWallet(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = CryptoWalletSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        return CryptoWallet.objects.filter(user=user)

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id=None):
        return self.destroy(request, id)


class UserBuyPrice(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = BuyPriceSerializer
    lookup_field = 'id'
    def get_queryset(self):
        user = self.request.user
        return BuyPrice.objects.filter(user=user)

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id=None):
        return self.destroy(request, id)


class UserTransactions(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.RetrieveModelMixin):
    serializer_class = TransactionSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=user)

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        return self.list(request)

    def post(self, request, id=None):
        return self.create(request)


class UserBalance(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    serializer_class = BalanceSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        return Balance.objects.filter(user=user)

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        return self.list(request)

    def post(self, request, id=None):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request)


#  REGISTER
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


#  ADMIN
class CryptoWalletView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = CryptoWalletSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUser]
    queryset = CryptoWallet.objects.all()

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id=None):
        return self.destroy(request, id)

class BuyPriceView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = BuyPriceSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUser]
    queryset = BuyPrice.objects.all()

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id=None):
        return self.destroy(request, id)


class TransactionsView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin):
    serializer_class = TransactionSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUser]
    queryset = Transaction.objects.all()

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        return self.list(request)

    def post(self, request, id=None):
        return self.create(request)


class BalancesView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    serializer_class = BalanceSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUser]
    queryset = Balance.objects.all()

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request):
        return self.update(request)


class UsersView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = UserSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        return self.list(request)
