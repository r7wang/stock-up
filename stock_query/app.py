import requests

from stock_query import settings

r = requests.get('https://finnhub.io/api/v1/quote?symbol=SHOP&token={}'.format(settings.TOKEN))
print(r.json())
