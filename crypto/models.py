from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class CryptoWallet(models.Model):
    user = models.ForeignKey(
            User, on_delete=models.CASCADE, null=True, blank=True)
    cryptoName = models.CharField(max_length=30)
    quantityDollars = models.FloatField()
    cryptoQuantity = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'{self.cryptoName}'


class Balance(models.Model):
    user = models.ForeignKey(
            User, on_delete=models.CASCADE, null=True, blank=True)
    balance = models.FloatField()

    def __str__(self):
        return f'{self.balance}'
