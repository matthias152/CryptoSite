#  https://github.com/man-c/pycoingecko
#  https://www.coingecko.com/pl/api/documentation
from pycoingecko import CoinGeckoAPI
from datetime import date, time, datetime

coingecko = CoinGeckoAPI()

bitcoin = coingecko.get_price(ids = 'bitcoin', vs_currencies = 'usd')
z = datetime.now().time()

print(z)
