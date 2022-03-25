from django.db import models


# Create your models here.


class CryptoWallet(models.Model):
    cryptoName = models.CharField(max_length=30, unique=True)
    quantityDollars = models.FloatField()
    cryptoQuantity = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'{self.cryptoName}'


class CashWallet(models.Model):
    dollars = models.FloatField()

    def __str__(self):
        return f'Balance {self.dollars}'
