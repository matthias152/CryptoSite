from django.contrib import admin
from .models import CryptoWallet, Balance, Transaction

# Register your models here.


admin.site.register(CryptoWallet)
admin.site.register(Balance)
admin.site.register(Transaction)
