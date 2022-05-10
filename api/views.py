from django.shortcuts import render
from django.shortcuts import get_object_or_404
from crypto.models import Balance
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from crypto.serializers import BalanceSerializer
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
        queryset = Balance.objects.all()
        balance = get_object_or_404(queryset, pk=pk)

        serializer = BalanceSerializer(balance)
        return Response(serializer.data)

    def update(self, request, pk=None):
        Balance = Balance.objects.get(pk=pk)
        serializer = BalanceSerializer(Balance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
