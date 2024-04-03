from ib_io import ib_io
from threading import Thread
import time

from ibapi.contract import Contract


class ib_client:
    def __init__(self,clientId = 1,port=7497,host="127.0.0.1") -> None:
        """
        3 secions:
        1. mkt data section
        2. fundmental data section
        3. account section
        """
        
        self.ib = ib_io()
        self.ib.connect(host,port,clientId)

        # establish on a thread
        ib_thread = Thread(target = self.run_loop,daemon=True)
        ib_thread.start()
        time.sleep(2)
        
        # contract data dict default - STK USD ISLAND
        self.contract_data = {
            "sec_type": "STK", 
            "currency": "USD", 
            "exchange" : "ISLAND",
            "duration" : "1 M", 
            "candle_size":"1 day",
            }

    def run_loop(self):
        print("Connection Starts")
        self.ib.run()
        

    def close_loop(self):
        self.ib.disconnect()
        print("Connection Stops")

    def process_data(self, data):
        for key, value in data.items():
            self.contract_data[key] = value


    # function - creating security(contract)
    # data_detail = {"sec_type": "STK", "currency": "USD", "exchange" : "ISLAND"}
    def security(self,symbol, data_detail=""):
        """
        Input: symbol, contract detail
            data_detail - sec_type, currency, exchange, contract_type,strike,exp_date

        Output: contract

        """
        if data_detail:
        # update contract details
            self.process_data(data_detail)


        # note volume is in thousands
        contract = Contract()
        contract.symbol = symbol
        contract.secType = self.contract_data["sec_type"]
        contract.currency = self.contract_data["currency"]
        contract.exchange = self.contract_data["exchange"]

        if contract.secType == "OPT":
            # call or put - C / P
            contract.right=self.contract_data["contract_type"]
            contract.strike = self.contract_data["strike"]
            if self.contract_data["exp_date"]:
                contract.lastTradeDateOrContractMonth = self.contract_data["exp_date"]
            contract.multiplier=100
            


        return contract
    
    def req_contract_details(self,security):
        '''
        
        input: contract

        output: idk

        
        '''
        # security = self.security(symbol)
        self.ib.reqContractDetails(self.ib.req_id, security)
        self.ib.req_id+=1
        time.sleep(1)
        return self.ib.contract_details


    # function - obtain stock historical data
    def req_stock_historical_data(self, symbol, data_detail=""):
        '''
        Input: symbol, duration, candel size
        stock_historical_data("aapl","1 M","1 day")
        https://interactivebrokers.github.io/tws-api/historical_bars.html
        
        Output: stock dict

        initialize Contract
        request HistoriccalData
        return stock_data_dict
        '''

        # print(data_detail)

        if data_detail:
        # update contract details
            self.process_data(data_detail)

        # print("data: {} \n\n".format(self.contract_data))

        contract = self.security(symbol,data_detail = self.contract_data)
        
        self.ib.reqHistoricalData(
            reqId=self.ib.req_id,
            contract=contract,
            endDateTime="",
            # Time Range; S = Seconds, D = day, M = Month, Y = Year; Ex - 1 M
            durationStr=self.contract_data["duration"],
            # https://interactivebrokers.github.io/tws-api/historical_bars.html
            # Tick Range; in link
            barSizeSetting=self.contract_data["candle_size"],
            whatToShow="ADJUSTED_LAST",
            # regular trading hours(RTH) = 1, ETH = 0
            useRTH=1,
            formatDate=1,
            keepUpToDate=0,
            chartOptions=[],
        )

        # give 1 second to load data
        time.sleep(3)



        # increment request id
        self.ib.req_id+=1
        return self.ib.stock_data_dict
    
    # obtain option chain
    def req_option_chain(self, symbol, data_detail=""):
        
        # process data_details if inserted
        if data_detail:
            self.process_data(data_detail)
        
        # create contract
        contract = self.security(symbol, self.contract_data)    
        # req contract details
        self.req_contract_details(contract)

        self.ib.reqSecDefOptParams(
            reqId=self.ib.req_id,
            underlyingSymbol=symbol,
            futFopExchange="",
            underlyingSecType=contract.secType,
            underlyingConId=self.ib.contract_details[symbol],
            # 265598

        )
        time.sleep(1)


        # increment request id
        self.ib.req_id+=1
        return self.ib.option_chain


