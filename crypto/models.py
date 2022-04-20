from django.db import models
from django.contrib.auth.models import User


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


class Transaction(models.Model):
    user = models.ForeignKey(
            User, on_delete=models.CASCADE, null=True, blank=True)
    day_created = models.DateField()
    time_created = models.TimeField()
    type = models.CharField(max_length=30)
    coin = models.CharField(max_length=30)
    quantityCrypto = models.FloatField()
    quantityDollars = models.FloatField()
    balance_after = models.FloatField()

    class Meta:
        ordering = ['-day_created', '-time_created']
