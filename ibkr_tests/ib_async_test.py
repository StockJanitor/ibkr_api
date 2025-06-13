from ib_async import IB, Contract
from ib_async import util
import asyncio

def get_option_bid_ask(symbol, expiry, strike, right):
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)

    contract = Contract(symbol=symbol, lastTradeDateOrContractMonth=expiry,
                         strike=strike, right=right, secType='OPT', exchange='SMART', currency='USD')

    ticker = ib.reqTickers(contract)
    bid = ticker[0].bid
    ask = ticker[0].ask

    ib.disconnect()
    return bid, ask


symbol = 'AAPL'
expiry = '20240421'
strike = 170
right = 'C'

bid, ask = get_option_bid_ask(symbol, expiry, strike, right)
print(f'Bid: {bid}, Ask: {ask}')