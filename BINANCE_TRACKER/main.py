from binance.client import Client

from config import settings

client = Client(settings.BINANCE_API_KEY, settings.BINANCE_API_SECRET)


def get_non_zero_balances():
    try:
        account_info = client.get_account()
        balances = account_info['balances']
        
        non_zero_balances = []
        for balance in balances:
            free = float(balance['free'])
            locked = float(balance['locked'])
            if free > 0 or locked > 0:
                non_zero_balances.append(balance)
        
        return non_zero_balances
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    non_zero_balances = get_non_zero_balances()
    for balance in non_zero_balances:
        asset = balance['asset']
        free = balance['free']
        locked = balance['locked']
        print(f"Asset: {asset}, Free: {free}, Locked: {locked}")