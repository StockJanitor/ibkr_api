# Section 1 ibapi
from ibapi.client import *
from ibapi.common import SetOfFloat, SetOfString, TickerId
from ibapi.wrapper import *
from ibapi.contract import Contract, ContractDetails
import time


class ib_io(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self,self)
        self.req_id = 0

        self.contract_details = {}

        # stock price data, stock option data, fundamental data
        self.stock_data_dict = {}

        # option chain
        self.option_chain = {}
        self.filtered_option_chain= {}

        self.option_details = {}
        # data = {"aapl": {"item1": {"bid": 2, "ask": 1}, "item2": {"bid": 3, "ask": 1}},
        #          "amz": {"item3": {"bid": 7, "ask": 1}, "item5": {"bid": 8, "ask": 1}},}
        #        
        #
        # {"aapl": {"030201C0012000":{bid:2, ask:2}},}
        self.stock_option_data = {}
        
        """
        idea of converting to a flat df
        # Create a list of dictionaries
dict_list = [
    {"company": company, "item": item, "bid": values["bid"], "ask": values["ask"]}
    for company, items in data.items()
    for item, values in items.items()
]

# Convert the list of dictionaries into a DataFrame
df = pd.DataFrame(dict_list)


        """
        
        self.stock_fundamental_data = {}

        
        self.portfolio_data = {}
        self.portfolio_update_complete = False

    # output error
    def error(self,reqId,errorCode,errorString,test=""):
        print("Error {} {} {}".format(reqId,errorCode,errorString))
        # time.sleep(7)
        # self.disconnect()

    # Request portfolio
    def updatePortfolio(self, contract: Contract, position: float, marketPrice: float, marketValue: float,
                        averageCost: float, unrealizedPNL: float, realizedPNL: float, accountName: str):
        """Callback for portfolio updates."""
        symbol = contract.symbol
        sec_type = contract.secType
        expiry = contract.lastTradeDateOrContractMonth if contract.lastTradeDateOrContractMonth else ""
        strike = contract.strike if contract.strike else 0.0
        right = contract.right if contract.right else ""

        # Store portfolio data
        self.portfolio_data[symbol] = {
            "symbol": symbol,
            "sec_type": sec_type,
            "expiry": expiry,
            "strike": strike,
            "right": right,
            "position": position,
            "market_price": marketPrice,
            "market_value": marketValue,
            "average_cost": averageCost,
            "unrealized_pnl": unrealizedPNL,
            "realized_pnl": realizedPNL,
            "account_name": accountName
        }
        print(f"Portfolio Update: {symbol}, Position: {position}, Market Price: {marketPrice}")

    def accountDownloadEnd(self, accountName: str):
        """Callback to indicate portfolio update is complete."""
        self.portfolio_update_complete = True
        print(f"Portfolio download complete for account: {accountName}")

    def position(self, account: str, contract: Contract, position: float, avgCost: float):
        """Callback for position details (optional)."""
        symbol = contract.symbol
        print(f"Position: {symbol}, Account: {account}, Position: {position}, Avg Cost: {avgCost}")
        # Optionally store position data if needed



    def contractDetails(self, reqId, contractDetails):
        # time.sleep(1)
        contract_id = contractDetails.contract.conId
        symbol = contractDetails.contract.symbol
        # print("this is contract id: ", contract_id)
        self.contract_details[symbol]= contract_id
        # time.sleep(1)
        self.contract_details[reqId] = contractDetails.contract
        print(f"contract detail{reqId}, {self.contract_details[reqId]}")
        self.reqMktData(reqId, contractDetails.contract, "", False, False, [])
        time.sleep(3)
    
    def contractDetailsEnd(self, reqId):
        print("Contract Details End")
        # self.disconnect()


   # return of stock price historical data
    def historicalData(self, reqId, bar):
        # store item in self.stock_data_dict
        # if reqId not in self.stock_data_dict:
        if "stock_data" not in self.stock_data_dict[reqId]:
            self.stock_data_dict[reqId]["stock_data"] = [{
                "date":bar.date,
                "open":bar.open,
                "high":bar.high,
                "low":bar.low,
                "close":bar.close,
                "volume":bar.volume
            }]
            
        # elif reqId in self.stock_data_dict:
        if "stock_data" in self.stock_data_dict[reqId]:
            self.stock_data_dict[reqId]["stock_data"].append(
                {
                    "date":bar.date,
                    "open":bar.open,
                    "high":bar.high,
                    "low":bar.low,
                    "close":bar.close,
                    "volume":bar.volume
                }
            )

    
    def securityDefinitionOptionParameter(self, reqId: int, exchange: str, underlyingConId: int, tradingClass: str, multiplier: str, expirations: set, strikes: set):
        # print("security def option param executed.")
        # print("Exchange:", exchange)
        # print("Underlying ConId:", underlyingConId)
        # print("Trading Class:", tradingClass)
        # print("Multiplier:", multiplier)
        # print("Expirations:", expirations)
        # print("Strikes:", strikes)
        
        time.sleep(1)
        exp_sorted = list(expirations)
        exp_sorted.sort()
        self.option_chain[tradingClass] = {"expirations":list(exp_sorted),"strikes":list(strikes)}
        time.sleep(1)
        return super().securityDefinitionOptionParameter(reqId, exchange, underlyingConId, tradingClass, multiplier, expirations, strikes)
    
    def securityDefinitionOptionParameterEnd(self, reqId: int):
        print("Option Chain End")
        # self.disconnect()
        return super().securityDefinitionOptionParameterEnd(reqId)
    
    def tickPrice(self, reqId, tickType, price, attrib):
        contract = self.contract_details[reqId]
        symbol = contract.symbol
        expiry = contract.lastTradeDateOrContractMonth
        strike = contract.strike
        right = contract.right

        print(f"{reqId}, tickType: {TickTypeEnum.to_str(tickType)}, price {price}, att {attrib}")
        # if tickType == 1:  # Bid price
        #     print("Bid Price for", symbol, expiry, strike, right, ":", price)
        # elif tickType == 2:  # Ask price
        #     print("Ask Price for", symbol, expiry, strike, right, ":", price)
        # elif tickType == 4:  # Last price
        #     print("Last Price for", symbol, expiry, strike, right, ":", price)
        # elif tickType == 24:  # Implied volatility
        #     print("Implied Volatility for", symbol, expiry, strike, right, ":", price)

    def tickOpenOrder(self, reqId, contract, order, orderState):
        symbol = contract.symbol
        print("Open Interest for", symbol, ":", orderState.openOrderQty)

    def tickOptionComputation(self, reqId, tickType, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice):
        contract = self.contract_details[reqId]
        symbol = contract.symbol
        expiry = contract.lastTradeDateOrContractMonth
        strike = contract.strike
        right = contract.right

        print("Delta for", symbol, expiry, strike, right, ":", delta)
        print("Gamma for", symbol, expiry, strike, right, ":", gamma)
        print("Theta for", symbol, expiry, strike, right, ":", theta)

    def fundamentalData(self, reqId: int, data: str):
        print(reqId, data)
        print(2)
        return super().fundamentalData(reqId, data)
    