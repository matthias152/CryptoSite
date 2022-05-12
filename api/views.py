from django.shortcuts import render
from django.shortcuts import get_object_or_404
from crypto.models import Balance, CryptoWallet, Transaction, BuyPrice, User
from django.http import HttpResponse
from rest_framework import viewsets, generics, mixins, status
from rest_framework.response import Response
from crypto.serializers import BalanceSerializer, CryptoWalletSerializer
from crypto.serializers import TransactionSerializer, BuyPriceSerializer, UserSerializer


class BalanceViewSet(viewsets.ViewSet):
    def list(self, request):
        user_balance = Balance.objects.get(user=request.user)
        serializer = BalanceSerializer(user_balance)
        return Response(serializer.data)

    def create(self, request):
        serializer = BalanceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Balance.objects.all()
        balance = get_object_or_404(queryset, pk=pk)

        serializer = BalanceSerializer(balance)
        return Response(serializer.data)

    def update(self, request, pk=None):
        balance = Balance.objects.get(pk=pk)
        serializer = BalanceSerializer(balance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionViewSet(viewsets.ViewSet):
    def list(self, request):
        user_transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(user_transactions, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = TransactionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CryptoWalletViewSet(viewsets.ViewSet):
    def list(self, request):
        user = self.request.user
        cryptos = CryptoWallet.objects.filter(user=user)
        serializer = CryptoWalletSerializer(cryptos, many=True)
        return Response(serializer.data)


class CryptoWalletDetail(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = CryptoWalletSerializer
    queryset = CryptoWallet.objects.all()
    lookup_field = 'id'

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


class BuyPriceDetail(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = BuyPriceSerializer
    queryset = BuyPrice.objects.all()
    lookup_field = 'id'

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


class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)

        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
