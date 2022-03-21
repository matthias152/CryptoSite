#  https://github.com/man-c/pycoingecko
#  https://www.coingecko.com/pl/api/documentation
from pycoingecko import CoinGeckoAPI

coingecko = CoinGeckoAPI()

bitcoin = coingecko.get_price(ids = 'bitcoin', vs_currencies = 'usd')

print(bitcoin)
