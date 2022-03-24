from django.contrib import admin
from .models import CryptoWallet, CashWallet

# Register your models here.


admin.site.register(CryptoWallet)

admin.site.register(CashWallet)
