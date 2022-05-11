from django.shortcuts import render
from django.shortcuts import get_object_or_404
from crypto.models import Balance, CryptoWallet, Transaction, BuyPrice, User
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from crypto.serializers import BalanceSerializer, CryptoWalletSerializer
from crypto.serializers import TransactionSerializer, BuyPriceSerializer, UserSerializer
from rest_framework import status


class BalanceViewSet(viewsets.ViewSet):
    def list(self, request):
        balances = Balance.objects.all()
        serializer = BalanceSerializer(balances, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = BalanceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user = self.request.user
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


class CryptoWalletViewSet(viewsets.ViewSet):
    def list(self, request):
        cryptos = CryptoWallet.objects.all()
        serializer = CryptoWalletSerializer(cryptos, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CryptoWalletSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = CryptoWallet.objects.all()
        crypto = get_object_or_404(queryset, pk=pk)

        serializer = CryptoWalletSerializer(crypto)
        return Response(serializer.data)

    def update(self, request, pk=None):
        crypto = CryptoWallet.objects.get(pk=pk)
        serializer = CryptoWalletSerializer(crypto, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionViewSet(viewsets.ViewSet):
    def list(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = TransactionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Transaction.objects.all()
        transaction = get_object_or_404(queryset, pk=pk)

        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    def update(self, request, pk=None):
        transaction = Transaction.objects.get(pk=pk)
        serializer = TransactionSerializer(transaction, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BuyPriceViewSet(viewsets.ViewSet):
    def list(self, request):
        buy_prices = BuyPrice.objects.all()
        serializer = BuyPriceSerializer(buy_prices, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = BuyPriceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = BuyPrice.objects.all()
        buyprice = get_object_or_404(queryset, pk=pk)

        serializer = BuyPriceSerializer(buyprice)
        return Response(serializer.data)

    def update(self, request, pk=None):
        buyprice = BuyPrice.objects.get(pk=pk)
        serializer = BuyPriceSerializer(buyprice, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
