from django.shortcuts import render
from pycoingecko import CoinGeckoAPI
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import FileResponse, HttpResponse
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import date, datetime
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from .models import CryptoWallet, Balance, Transaction, BuyPrice
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

    trending_coins = []
    current_crypto_values = []
    profit_loss_all = {}

    trends = coingecko.get_search_trending()['coins']
    user_balance = Balance.objects.get(user=request.user)
    user_final_balance = float(user_balance.balance)
    user_cryptos = CryptoWallet.objects.filter(user=request.user)
    user_prices = BuyPrice.objects.filter(user=request.user)

    for i in user_prices:
        profit_loss = (i.cryptoQuantity * get_coin_price(i.cryptoName)) - (i.cryptoQuantity * i.price)
        profit_loss_all[str(i.cryptoName)] = profit_loss

    for i in user_cryptos:
        z = round(get_coin_price(i.cryptoName) * i.cryptoQuantity, 5)
        current_crypto_values.append(z)

    for i in range(7):
        coin = trends[i]['item']['name']
        trending_coins.append(coin)

    # CREATING FINAL TABLE
    names = []
    quantities = []
    values = profit_loss_all.values()
    values_list = list(values)

    for i in user_cryptos:
        names.append(i.cryptoName)
        quantities.append(i.cryptoQuantity)

    final_table = zip(names, quantities, current_crypto_values, values_list)
    ###

    return render(request, "wallet.html", {
        'trending': trending_coins,
        'user_final_balance': user_final_balance,
        'user': request.user,
        'final_table': final_table,
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
def transactions_history(request):
    user_transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'transactions.html', {
        'transactions': user_transactions,
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
