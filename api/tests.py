import json
from django.urls import reverse
from django.contrib.auth.models import User
from crypto.models import CryptoWallet, BuyPrice, Balance, Transaction
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RegistrationTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("registersite")

    def test_registration(self):
        data = {"username": "testcase","password": "some_strong_psW1",
                "password2": "some_strong_psW1",
                "email": "test@gmail.com",
                "first_name": "Matthew", "last_name": "Mattest"}
        request = self.client.post(self.url, data)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)


class CryptoTestCase(APITestCase):

    def setUp(self):
        self.url = reverse("cryptos-user")
        self.superuser = User.objects.create_superuser('matt', 'matt@gmail.com', 'mattpassw')
        self.client.login(username="matt", password="mattpassw")
        self.crypto = CryptoWallet.objects.create(user=self.superuser, cryptoName="bitcoin", cryptoQuantity=10.0)

    def test_can_get_crypto(self):
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_cant_get_crypto_detail(self):
        request = self.client.get(reverse("cryptos-user-detail", kwargs={"id":1}))
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_cant_get_crypto_detail_2(self):
        request = self.client.get(reverse("cryptos-user-detail", kwargs={"id":2}))
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_create_crypto(self):
        request = self.client.post(self.url, {"user":1, "cryptoName":"bitcoin", "cryptoQuantity":2.0})
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_crypto_update(self):
        data = {"user":1, "cryptoName":"bitcoin", "cryptoQuantity":20.0}
        request = self.client.put(reverse("cryptos-user-detail", kwargs={"id":1}), data=data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_delete_crypto(self):
        request = self.client.delete(reverse("cryptos-user-detail", kwargs={"id":1}))
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)


class BuyPriceTestCase(APITestCase):

    def setUp(self):
        self.url = reverse("buyprices-user")
        self.user = User.objects.create_user(username="Matt", password="mattestpsW1")
        self.client.login(username="Matt", password="mattestpsW1")
        self.buyprice = BuyPrice.objects.create(user=self.user, day_created="2022-05-18",
                        time_created="12:00:00", cryptoName="bitcoin", cryptoQuantity=5,
                        price=29500)

    def test_get_prices(self):
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_price_detail(self):
        request = self.client.get(reverse("buyprices-user-detail", kwargs={"id":1}))
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_create_buyprice(self):
        request = self.client.post(self.url, {"user":1, "cryptoName":"stellar",
                            "cryptoQuantity":150, "price":0.1,
                            "day_created":"2022-05-18", "time_created":"12:00:00"})
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

class BalanceTestCase(APITestCase):

    def setUp(self):
        self.url = reverse("balance-user")
        self.user = User.objects.create_user(username="Matt", password="mattestpsW1")
        self.client.login(username="Matt", password="mattestpsW1")
        self.balance = Balance.objects.create(user=self.user, balance=1000)

    def test_get_balance(self):
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_update_balance(self):
        data = {"user":1, "balance":500}
        request = self.client.put(reverse("balance-user-detail", kwargs={"id":1}), data=data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)


class TransactionTestCase(APITestCase):

    def setUp(self):
        self.url = reverse("transaction-user")
        self.user = User.objects.create_user(username="Matt", password="mattestpsW1")
        self.client.login(username="Matt", password="mattestpsW1")

    def test_get_transactions(self):
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_create_transaction(self):
        request = self.client.post(self.url, {"user":1, "day_created":"2022-05-18",
                "time_created":"12:00:00", "type":"sell", "coin":"ethereum", "quantityCrypto":3.5,
                "price":3000, "balance_after":16000})
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
