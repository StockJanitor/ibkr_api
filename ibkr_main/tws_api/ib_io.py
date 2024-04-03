from ibapi.client import EClient
from ibapi.common import SetOfFloat, SetOfString
from ibapi.wrapper import EWrapper
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

    # output error
    def error(self,reqId,errorCode,errorString,test=""):
        print("Error {} {} {}".format(reqId,errorCode,errorString))



    def contractDetails(self, reqId, contractDetails):
        contract_id = contractDetails.contract.conId
        symbol = contractDetails.contract.symbol

        self.contract_details[symbol]= contract_id

    
    def contractDetailsEnd(self, reqId):
        print("Contract Details End")
        # self.disconnect()


   # return of stock price historical data
    def historicalData(self, reqId, bar):
    
        # store item in self.stock_data_dict
        if reqId not in self.stock_data_dict:
            self.stock_data_dict[reqId] = [{
                "date":bar.date,
                "open":bar.open,
                "high":bar.high,
                "low":bar.low,
                "close":bar.close,
                "volume":bar.volume
            }]
            
        elif reqId in self.stock_data_dict:
            self.stock_data_dict[reqId].append(
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
        exp_sorted = list(expirations)
        exp_sorted.sort()
        self.option_chain[tradingClass] = {"expirations":list(exp_sorted),"strikes":list(strikes)}
        return super().securityDefinitionOptionParameter(reqId, exchange, underlyingConId, tradingClass, multiplier, expirations, strikes)
    
    def securityDefinitionOptionParameterEnd(self, reqId: int):
        print("Option Chain End")
        # self.disconnect()
        return super().securityDefinitionOptionParameterEnd(reqId)