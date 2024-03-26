from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract



class ib_io(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self,self)
        self.req_id = 0
        self.stock_data_dict = {}

    # output error
    def error(self,reqId,errorCode,errorString,test):
        print("Error {} {} {}".format(reqId,errorCode,errorString))

   # requesting historical data
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