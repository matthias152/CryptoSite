from django.contrib import admin
from .models import CryptoWallet, Balance

# Register your models here.


admin.site.register(CryptoWallet)
admin.site.register(Balance)
