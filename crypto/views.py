from django.shortcuts import render
from pycoingecko import CoinGeckoAPI
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import FileResponse
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import date, datetime
import io
import random
import string
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from .models import CryptoWallet, Balance, Transaction, BuyPrice, WalletID
from .models import DepositWithdraw_Transaction, SendReceive_Transaction
from .forms import NewUserForm


coingecko = CoinGeckoAPI()
today = date.today()


def get_coin_price(coin):
    coin_price = coingecko.get_price(ids=str(coin).lower(), vs_currencies='usd')[str(coin).lower()]['usd']
    return float(coin_price)


def CreateBuyTransaction(user, day, time, bcoin, type, qb, bce, ufb):
    new_transaction = Transaction()
    new_transaction.user = user
    new_transaction.day_created = day
    new_transaction.time_created = time
    new_transaction.coin = bcoin
    new_transaction.type = type
    new_transaction.quantityCrypto = float(qb) / float(bce)
    new_transaction.price = bce
    new_transaction.balance_after = ufb - float(qb)
    new_transaction.save()


def CreateSellTransaction(user, day, time, scoin, type, sq, sce, ufb):
    new_transaction = Transaction()
    new_transaction.user = user
    new_transaction.day_created = day
    new_transaction.time_created = time
    new_transaction.coin = scoin
    new_transaction.type = type
    new_transaction.quantityCrypto = sq
    new_transaction.price = sce
    new_transaction.balance_after = ufb + float(sq) * float(sce)
    new_transaction.save()


def CollectBuyPrices(user, day, time, crypto, cq, price):
    bPrice = BuyPrice()
    bPrice.user = user
    bPrice.day_created = day
    bPrice.time_created = time
    bPrice.cryptoName = crypto
    bPrice.cryptoQuantity = cq
    bPrice.price = price
    bPrice.save()


def CreateDepositWithdrawTransaction(user, day, time, type, quantity):
    new_transaction = DepositWithdraw_Transaction()
    new_transaction.user = user
    new_transaction.day_created = day
    new_transaction.time_created = time
    new_transaction.type = type
    new_transaction.quantity = quantity
    new_transaction.save()


def CreateSendReceiveTransaction(user, day, time, type, name, quantity):
    new_transaction = SendReceive_Transaction()
    new_transaction.user = user
    new_transaction.day_created = day
    new_transaction.time_created = time
    new_transaction.type = type
    new_transaction.cryptoName = name
    new_transaction.quantity = quantity
    new_transaction.save()


def register_request(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return render(request, 'wallet.html')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(
        request=request, template_name="register.html", context={"register_form": form})


class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return ('/')


@login_required(login_url='/login')
def wallet(request):

    current_crypto_values = []
    profit_loss_all = {}

    try:
        user_balance = Balance.objects.get(user=request.user)
        user_final_balance = float(user_balance.balance)
    except:
        user_balance = False
        user_final_balance = 0

    user_cryptos = CryptoWallet.objects.filter(user=request.user)
    user_prices = BuyPrice.objects.filter(user=request.user)

    for i in user_prices:
        profit_loss = (i.cryptoQuantity * get_coin_price(i.cryptoName)) - (i.cryptoQuantity * i.price)
        profit_loss_all[str(i.cryptoName)] = profit_loss

    for i in user_cryptos:
        z = round(get_coin_price(i.cryptoName) * i.cryptoQuantity, 5)
        current_crypto_values.append(z)

    # CREATING FINAL TABLE
    names = []
    quantities = []
    values = profit_loss_all.values()
    values_list = list(values)
    portfolio_summary = sum(current_crypto_values)

    for i in user_cryptos:
        names.append(i.cryptoName)
        quantities.append(i.cryptoQuantity)

    final_table = zip(names, quantities, current_crypto_values, values_list)
    ###

    return render(request, "wallet.html", {
        'user_balance': user_balance,
        'user_final_balance': round(user_final_balance, 2),
        'user': request.user,
        'final_table': final_table,
        'values_summary': round(portfolio_summary, 2),
    })


@login_required(login_url='/login')
def buy_cryptos(request):
    if request.method == 'POST':
        if request.POST.get('cryptoNameBuy') and request.POST.get('quantityDollarsBuy'):
            buying_coin = request.POST.get('cryptoNameBuy', None)
            quantity_bought = request.POST.get('quantityDollarsBuy')

            user_balance = Balance.objects.get(user=request.user)
            user_cryptos = CryptoWallet.objects.filter(user=request.user)
            user_final_balance = float(user_balance.balance)

            buying_coin_exchange = get_coin_price(buying_coin)
            cryptoQuantityBought = float(quantity_bought) / float(buying_coin_exchange)
            user_cryptos_list = []

        for i in user_cryptos:
            z = str(i.cryptoName)
            user_cryptos_list.append(z)

        if float(quantity_bought) <= user_final_balance:
            if str(buying_coin) in user_cryptos_list:
                y = user_cryptos.get(cryptoName=buying_coin)
                y.cryptoQuantity += float(quantity_bought) / float(buying_coin_exchange)
                y.save()
                user_balance.balance -= float(quantity_bought)
                user_balance.save()
                curr_time = datetime.now().time()
                CreateBuyTransaction(request.user, today, curr_time,
                    buying_coin, "buy", quantity_bought, buying_coin_exchange, user_final_balance)
                CollectBuyPrices(request.user, today, curr_time, buying_coin, cryptoQuantityBought, buying_coin_exchange)
                return render(request, 'success-buy.html', {
                    "buying_coin": buying_coin,
                    "money": quantity_bought,
                    "cryptoQuantity": cryptoQuantityBought,
                })
            else:
                new_cryp = CryptoWallet()
                new_cryp.user = request.user
                new_cryp.cryptoName = buying_coin
                new_cryp.cryptoQuantity = float(quantity_bought) / float(buying_coin_exchange)
                new_cryp.save()
                user_balance.balance -= float(quantity_bought)
                user_balance.save()
                curr_time = datetime.now().time()
                CreateBuyTransaction(request.user, today, curr_time,
                    buying_coin, "buy", quantity_bought, buying_coin_exchange, user_final_balance)
                CollectBuyPrices(request.user, today, curr_time, buying_coin, cryptoQuantityBought, buying_coin_exchange)
                return render(request, 'success-buy.html', {
                    "buying_coin": buying_coin,
                    "money": quantity_bought,
                    "cryptoQuantity": cryptoQuantityBought
                })
        return render(request, 'buy-crypto.html')
    return render(request, 'buy-crypto.html')


@login_required(login_url='/login')
def sell_cryptos(request):
    if request.method == 'POST':
        if request.POST.get('cryptoNameSell') and request.POST.get('cryptoQuantitySell'):
            selling_coin = request.POST.get('cryptoNameSell')
            selling_quantity = request.POST.get('cryptoQuantitySell')

            user_balance = Balance.objects.get(user=request.user)
            user_cryptos = CryptoWallet.objects.filter(user=request.user)
            user_prices = BuyPrice.objects.filter(user=request.user, cryptoName=selling_coin)
            user_final_balance = float(user_balance.balance)

            selling_coin_exchange = get_coin_price(selling_coin)
            money = float(selling_quantity) * float(selling_coin_exchange)
            y = user_cryptos.get(cryptoName=selling_coin)
            user_cryptos_list = []

            for i in user_cryptos:
                z = str(i.cryptoName)
                user_cryptos_list.append(z)

            if str(selling_coin) in user_cryptos_list:
                if float(y.cryptoQuantity) >= float(selling_quantity):
                    y.cryptoQuantity -= float(selling_quantity)
                    y.save()
                    if y.cryptoQuantity == 0:
                        y.delete()
                    user_balance.balance += float(selling_quantity) * float(selling_coin_exchange)
                    user_balance.save()
                    curr_time = datetime.now().time()
                    CreateSellTransaction(request.user, today, curr_time, selling_coin, "sell",
                        selling_quantity, selling_coin_exchange, user_final_balance)
                    sellingq = float(selling_quantity)

                    for i in range(0, len(user_prices)):
                        if sellingq > user_prices[i].cryptoQuantity:
                            sellingq -= user_prices[i].cryptoQuantity
                            user_prices[i].delete()
                        else:
                            user_prices[i].cryptoQuantity -= sellingq
                            user_prices[i].save()
                            break
                    return render(request, 'success-sell.html', {
                        "selling_coin": selling_coin,
                        "selling_quantity": selling_quantity,
                        "money": money,
                    })
                else:
                    return render(request, 'sell-crypto.html')
            else:
                return render(request, 'sell-crypto.html')
        return render(request, 'sell-crypto.html')
    return render(request, 'sell-crypto.html')


@login_required(login_url='/login')
def send_crypto(request):
    if request.method == 'POST':
        if request.POST.get('cryptoName') and request.POST.get('cryptoQuantity') and request.POST.get('walletID'):

            sending_coin = request.POST.get('cryptoName')
            sending_coin_quantity = request.POST.get('cryptoQuantity')
            sending_walletid = request.POST.get('walletID')
            curr_time = datetime.now().time()
            fl_send = float(sending_coin_quantity)

            sender_crypto = CryptoWallet.objects.get(user=request.user, cryptoName=str(sending_coin))
            sender_buyprices = BuyPrice.objects.filter(user=request.user, cryptoName=sending_coin)

            receiver_wallet = WalletID.objects.get(unique_id=sending_walletid)

            try:
                receiver_crypto = CryptoWallet.objects.get(user=receiver_wallet.user, cryptoName=sending_coin)
            except:
                receiver_crypto = False

            if sender_crypto.cryptoQuantity > float(sending_coin_quantity):
                if receiver_crypto:
                    sender_crypto.cryptoQuantity -= float(sending_coin_quantity)
                    sender_crypto.save()
                    CreateSendReceiveTransaction(request.user, today, curr_time,
                        "send", sending_coin, sending_coin_quantity)
                    receiver_crypto.cryptoQuantity += float(sending_coin_quantity)
                    receiver_crypto.save()
                    CreateSendReceiveTransaction(receiver_wallet.user, today,
                        curr_time, "receive", sending_coin, sending_coin_quantity)

                    for i in range(0, len(sender_buyprices)):
                        if fl_send > sender_buyprices[i].cryptoQuantity:
                            fl_send -= sender_buyprices[i].cryptoQuantity
                            sender_buyprices[i].delete()
                        else:
                            sender_buyprices[i].cryptoQuantity -= fl_send
                            sender_buyprices[i].save()
                            break
                else:
                    sender_crypto.cryptoQuantity -= float(sending_coin_quantity)
                    sender_crypto.save()
                    CreateSendReceiveTransaction(request.user, today, curr_time,
                        "send", sending_coin, sending_coin_quantity)
                    new_crypto = CryptoWallet()
                    new_crypto.user = receiver_wallet.user
                    new_crypto.cryptoName = sending_coin
                    new_crypto.cryptoQuantity = float(sending_coin_quantity)
                    new_crypto.save()
                    CreateSendReceiveTransaction(receiver_wallet.user, today,
                        curr_time, "receive", sending_coin, sending_coin_quantity)

                    for i in range(0, len(sender_buyprices)):
                        if fl_send > sender_buyprices[i].cryptoQuantity:
                            fl_send -= sender_buyprices[i].cryptoQuantity
                            sender_buyprices[i].delete()
                        else:
                            sender_buyprices[i].cryptoQuantity -= fl_send
                            sender_buyprices[i].save()
                            break
                return render(request, 'success-send.html', {
                    'sending_coin': sending_coin,
                    'sending_coin_quantity': sending_coin_quantity,
                    'walletid': sending_walletid,
                })
            else:
                return render(request, 'send-crypto.html')
        return render(request, 'send-crypto.html')
    return render(request, 'send-crypto.html')


@login_required(login_url='/login')
def user_profile(request):
    username = request.user.username
    user_email = request.user.email
    try:
        user_balance = Balance.objects.get(user=request.user)
        user_final_balance = float(user_balance.balance)
    except:
        user_balance = False
        user_final_balance = 0
    user_cryptos = CryptoWallet.objects.filter(user=request.user)
    portfolio_summary_list = []
    user_walletid = WalletID.objects.filter(user=request.user)

    for i in user_cryptos:
        z = round(get_coin_price(i.cryptoName) * i.cryptoQuantity, 5)
        portfolio_summary_list.append(z)

    portfolio_summary = sum(portfolio_summary_list)

    return render(request, 'userprofile.html',{
        'username': username,
        'user_email': user_email,
        'user_balance': user_final_balance,
        'user_portfolio': portfolio_summary,
        'user_walletid': user_walletid,
    })


@login_required(login_url='/login')
def transactions_history(request):
    user_transactions = Transaction.objects.filter(user=request.user)
    user_deposit_withdraw_transactions = DepositWithdraw_Transaction.objects.filter(user=request.user)
    user_sendreceive_transactions = SendReceive_Transaction.objects.filter(user=request.user)

    return render(request, 'transactions.html', {
        'transactions': user_transactions,
        'deposit_withdraw': user_deposit_withdraw_transactions,
        'send_receive': user_sendreceive_transactions,
    })


@login_required(login_url='/login')
def deposit(request):
    if request.method == 'POST':
        if request.POST.get('addBalanceFunds'):
            balance_add = request.POST.get('addBalanceFunds')
            curr_time = datetime.now().time()

            try:
                balance_check = Balance.objects.get(user=request.user)
            except:
                balance_check = False

            if balance_check:
                balance_check.balance += float(balance_add)
                balance_check.save()
                CreateDepositWithdrawTransaction(request.user, today, curr_time, "deposit", balance_add)
            else:
                new_balance = Balance()
                new_balance.user = request.user
                new_balance.balance = balance_add
                new_balance.save()
                CreateDepositWithdrawTransaction(request.user, today, curr_time, "deposit", balance_add)
            return render(request, 'balance-success.html', {
                'balance_suc': balance_add,
            })
    return render(request, 'balance-add.html')


@login_required(login_url='/login')
def generate_walletid(request):
    if request.method == 'POST':
        z = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=25))
        new_wallet_id = WalletID()
        new_wallet_id.user = request.user
        new_wallet_id.unique_id = z
        new_wallet_id.save()
        return render(request, 'walletid-success.html', {
            'walletid': z
        })

    user_walletid = WalletID.objects.filter(user=request.user)

    return render(request, 'generate-walletid.html', {
        'user_walletid': user_walletid,
    })



def pdf_transactions(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 7)

    lines = ["name   date          hour                   type    coin     qCoin   price    balance"]

    pdftra = Transaction.objects.filter(user=request.user)

    for i in pdftra:
        lines.append(str(i.user) + " " + str(i.day_created) + " "
            + str(i.time_created) + " " + i.type + " " + i.coin
            + " " + str(round(i.quantityCrypto, 3)) + " " + str(round(i.price, 3)) + " "
            + str(round(i.balance_after, 3)))
        lines.append(" ")

    for i in lines:
        textob.textLine(i)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='transactions.pdf')


def pdf_transactions_email(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 7)

    lines = ["name   date          hour                   type    coin     qCoin   price    balance"]

    pdftra = Transaction.objects.filter(user=request.user)

    for i in pdftra:
        lines.append(str(i.user) + " " + str(i.day_created) + " "
            + str(i.time_created) + " " + i.type + " " + i.coin
            + " " + str(round(i.quantityCrypto, 3)) + " " + str(round(i.price, 3)) + " "
            + str(round(i.balance_after, 3)))
        lines.append(" ")

    for i in lines:
        textob.textLine(i)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    pdf_to_email = buf.getvalue()
    buf.close()

    subject = "CryptoSite transactions"
    message = "Hello, below is PDF file with your history of transactions."

    user = request.user
    usermail = str(user.email)
    emails = [usermail]
    mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, emails)
    mail.attach('generated.pdf', pdf_to_email, 'application/pdf')

    mail.send(fail_silently = False)
    return render(request, 'email-success.html')
