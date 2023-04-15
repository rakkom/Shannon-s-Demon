import json
from datetime import datetime
from pybit import spot
import config

trading_pair = "BTCUSDC"
threshold = 0.02

def get_account_balance():
    current_balance = session_auth.get_wallet_balance()
    balance = {}
    for coin_balance in current_balance['result']['balances']:
        if coin_balance['coin'] in ['BTC', 'USDC']:
            balance[coin_balance['coin']] = float(coin_balance['total'])
    return balance

def get_current_price():
    price_info = session_auth.last_traded_price(symbol=trading_pair)
    return float(price_info['result']['price'])

def adjust_balances(btc_balance, usdc_balance, price):
    target_value = (btc_balance * price + usdc_balance) / 2
    btc_target = target_value / price
    usdc_target = target_value
    return btc_target, usdc_target

def trade(btc_target, btc_balance):
    side = "Buy" if btc_target > btc_balance else "Sell"
    quantity = abs(btc_target - btc_balance)
    order = session_auth.place_active_order(
        symbol=trading_pair,
        side=side,
        type="MARKET",
        qty=quantity,
        timeInForce="GTC"
    )
    print(f"{side} order executed: {quantity} BTC")

def check_and_adjust():
    balance = get_account_balance()
    price = get_current_price()

    btc_balance = balance['BTC']
    usdc_balance = balance['USDC']
    btc_value = btc_balance * price
    usdc_value = usdc_balance

    if abs((btc_value - usdc_value) / usdc_value) > threshold:
        btc_target, usdc_target = adjust_balances(btc_balance, usdc_balance, price)
        trade(btc_target, btc_balance)

if __name__ == "__main__":
    check_and_adjust()
