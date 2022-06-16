from django.contrib import admin
from .models import CryptoWallet, Balance, Transaction, BuyPrice, WalletID
from .models import DepositWithdraw_Transaction, SendReceive_Transaction


admin.site.register(CryptoWallet)
admin.site.register(Balance)
admin.site.register(Transaction)
admin.site.register(BuyPrice)
admin.site.register(WalletID)
admin.site.register(DepositWithdraw_Transaction)
admin.site.register(SendReceive_Transaction)
