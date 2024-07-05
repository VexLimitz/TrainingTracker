from binance.client import Client

from config import settings


client = Client(settings.BINANCE_API_KEY, settings.BINANCE_API_SECRET)

account = client.get_account()

print(account['balances'])