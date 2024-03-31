from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract



class ib_io(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self,self)
        self.req_id = 0
        # stock price data, stock option data, fundamental data
        self.stock_data_dict = {}


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
    def error(self,reqId,errorCode,errorString,test):
        print("Error {} {} {}".format(reqId,errorCode,errorString))

   # return of historical data
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

    