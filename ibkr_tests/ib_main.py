# Section 3 execution
import sys
import os

# Add the 'lib' directory to sys.path
current_dir = os.getcwd()
lib_path = os.path.abspath(os.path.join(current_dir,"ibkr_api", 'ibkr_lib'))
sys.path.append(lib_path)
print(lib_path)

from ib_client import ib_client
import time


############### Inputs ###############
ite1 = {
    "sec_type" : "OPT",
    "exchange":"BOX",
    "duration":"2 D", 
    "candle_size":"4 hours",
    "contract_type" :"C",
    "strike" : 150,
    #"exp_date" : "date"
    
    }
tickers = "AAPL"
############### Program Codes ###############
# initialize client object
item = ib_client(port=7496)

##### ---------- Req Portfolio ---------- #####


##### ---------- STOCKS ---------- #####

# request historical price
# Example: data_details = {"duration" : "1 M", "candle_size" : "1 day"... security details}
# data = {"duration": "5 D"}
# item.req_stock_historical_data(tickers, data_detail=data)

# print(item.ib.stock_data_dict)
# item.toJson(item.ib.stock_data_dict)



# request fundamental data
# item.req_fundamental_data(tickers)





##### ---------- OPTIONS ---------- #####

# # obtain full option chain
# item.req_option_chain(tickers)
# time.sleep(2)

# print(1)
# # filter option chain
# print(item.filter_option_chain(tickers))
# print(2)


# # # obtain option data
# item.option_details(tickers)

##### CLOSE #####
# time.sleep(10)
# print(item.ib.contract_details)


# close loop
item.close_loop()




############### TEST CODES ###############

# from ibapi.client import EClient
# from ibapi.wrapper import EWrapper
# from ibapi.contract import Contract

# class MyWrapper(EWrapper):
#     def __init__(self):
#         EWrapper.__init__(self)
#         self.contract_details = {}

#     def contractDetails(self, reqId, contractDetails):
#         self.contract_details[reqId] = contractDetails.contract
#         self.reqMktData(reqId, contractDetails.contract, "", False, False, [])

#     def tickPrice(self, reqId, tickType, price, attrib):
#         if tickType == 1:  # Bid price
#             print("Bid Price for", self.contract_details[reqId].symbol, ":", price)
#         elif tickType == 2:  # Ask price
#             print("Ask Price for", self.contract_details[reqId].symbol, ":", price)
#         elif tickType == 4:  # Last price
#             print("Last Price for", self.contract_details[reqId].symbol, ":", price)
#         elif tickType == 24:  # Implied volatility
#             print("Implied Volatility for", self.contract_details[reqId].symbol, ":", price)

#     def tickOpenOrder(self, orderId, contract, order, orderState):
#         print("Open Interest for", contract.symbol, ":", orderState.openOrderQty)

#     def tickOptionComputation(self, reqId, tickType, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice):
#         print("Delta for", self.contract_details[reqId].symbol, ":", delta)
#         print("Gamma for", self.contract_details[reqId].symbol, ":", gamma)
#         print("Theta for", self.contract_details[reqId].symbol, ":", theta)

# def main():
#     wrapper = MyWrapper()
#     client = EClient(wrapper)
#     client.connect("127.0.0.1", 7497, clientId=1)

#     option_chain = {
#         1: {"symbol": "AAPL", "strike": 150, "expiry": "20230421"},
#         2: {"symbol": "AAPL", "strike": 155, "expiry": "20230421"}
#     }

#     for reqId, contract_details in option_chain.items():
#         contract = Contract()
#         contract.symbol = contract_details["symbol"]
#         contract.secType = "OPT"
#         contract.exchange = "SMART"
#         contract.currency = "USD"
#         contract.lastTradeDateOrContractMonth = contract_details["expiry"]
#         contract.strike = contract_details["strike"]
#         contract.right = "C"  # Call option

#         client.reqContractDetails(reqId, contract)

#     client.run()

# if __name__ == "__main__":
#     main()