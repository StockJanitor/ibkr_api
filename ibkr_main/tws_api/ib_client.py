from ib_io import ib_io
from threading import Thread
import time

from ibapi.contract import Contract


class ib_client:
    def __init__(self,clientId = 1,port=7497,host="127.0.0.1") -> None:
        self.ib = ib_io()
        self.ib.connect(host,port,clientId)

        # establish on a thread
        ib_thread = Thread(target = self.run_loop,daemon=True)
        ib_thread.start()
        time.sleep(2)
        
    def run_loop(self):
        print("Connection Starts")
        self.ib.run()
        

    def close_loop(self):
        self.ib.disconnect()
        print("Connection Stops")

    # function - creating security
    # data_detail = {"sec_type": "STK", "currency": "USD", "exchange" : "ISLAND"}
    def security(self,symbol, data_detail):
        # note volume is in thousands
        contract = Contract()
        contract.symbol = symbol
        contract.secType = data_detail["sec_type"]
        contract.currency = data_detail["currency"]
        contract.exchange = data_detail["exchange"]
        return contract
    
    def stock_historical_data(self, symbol, duration = "1 M", candle_size="1 day"):
        '''
        Input: symbol, duration, candel size
        Output: stock dict

        initialize Contract
        request HistoriccalData
        return stock_data_dict
        '''
        contract = self.security(symbol,data_detail = {"sec_type": "STK", "currency": "USD", "exchange" : "ISLAND"})
        
        self.ib.reqHistoricalData(
            reqId=self.ib.req_id,
            contract=contract,
            endDateTime="",
            # Time Range; S = Seconds, D = day, M = Month, Y = Year; Ex - 1 M
            durationStr=duration,
            # https://interactivebrokers.github.io/tws-api/historical_bars.html
            # Tick Range; in link
            barSizeSetting=candle_size,
            whatToShow="ADJUSTED_LAST",
            # regular trading hours(RTH) = 1, ETH = 0
            useRTH=1,
            formatDate=1,
            keepUpToDate=0,
            chartOptions=[],
        )
        time.sleep(1)
        self.ib.req_id+=1
        return self.ib.stock_data_dict
    def option_chain(self, symbol):
        pass


# initialize client object
item = ib_client()

print(item.stock_historical_data("AAPL"))

# close loop
item.close_loop()