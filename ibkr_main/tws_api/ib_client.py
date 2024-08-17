from ib_io import ib_io
from threading import Thread
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

from ibapi.contract import Contract


class ib_client:
    def __init__(self,clientId = 1,port=7497,host="127.0.0.1") -> None:
        """
        3 secions:
        1. mkt data section
        2. fundmental data section
        3. account section
        4. parsing section
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

############### 1. Market Data Section ###############
    # function - creating security(contract)
    # data_detail = {"sec_type": "STK", "currency": "USD", "exchange" : "ISLAND"}
    def security(self,symbol, data_detail=""):
        """
        Input: symbol, contract detail
            data_detail = {"sec_type": "STK", "currency": "USD", "exchange" : "ISLAND"}
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
        output: currently conId, contract details
        '''
        # security = self.security(symbol)
        self.ib.reqContractDetails(self.ib.req_id, security)
        self.ib.req_id+=1
        time.sleep(2) # this is crucial to wait for data to come
        return self.ib.contract_details


    # function - obtain stock historical data
    def req_stock_historical_data(self, symbol, data_detail=""):
        '''
        Input: symbol, duration, candel size
        data_details = {"duration" : "1 M", "candle_size" : "1 day"... security details}
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

        # create contract
        contract = self.security(symbol,data_detail = self.contract_data)

        self.ib.stock_data_dict[self.ib.req_id] = {"ticker" : symbol}


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
        time.sleep(10)

        # increment request id
        self.ib.req_id+=1
        return self.ib.stock_data_dict
    
    # obtain option chain
    def req_option_chain(self, symbol, data_detail=""):
        '''
        input: symbol, data_detail
        '''
        
        # process data_details if inserted
        if data_detail:
            self.process_data(data_detail)
        
        # create contract
        contract = self.security(symbol, self.contract_data)    
        # req contract details
        self.req_contract_details(contract)
        

        # returns option chain: expirations, strikes etc
        self.ib.reqSecDefOptParams(
            reqId=self.ib.req_id,
            underlyingSymbol=symbol,
            futFopExchange="",
            underlyingSecType=contract.secType,
            underlyingConId=self.ib.contract_details[symbol],
        )
        time.sleep(3)

        # increment request id
        self.ib.req_id+=1
        return self.ib.option_chain

    def option_details(self,symbol,contract_type="P"):
        '''
        
        
        tick types:
        https://interactivebrokers.github.io/tws-api/tick_types.html
        '''
        for i in self.ib.filtered_option_chain[symbol]["expirations"]:
            for j in self.ib.filtered_option_chain[symbol]["strikes"]:

                option_detail = {
                    "sec_type":"OPT",
                    "exchange":"BOX",
                    "contract_type":contract_type,
                    "strike":j,
                    "exp_date":i,
                    }
                
                print(f"current expiration {i} : current strike {j}")

                # create contract
                contract = self.security(symbol,option_detail)
                # request contract details
                self.req_contract_details(contract)
                time.sleep(3)


                

                self.ib.req_id+=1

############### 2. Fundamental Data Section ###############
    def req_fundamental_data(self,symbol):
        '''
        
        '''
        
        # create contract
        contract = self.security(symbol)

        # requesting fundamental data
        self.ib.reqFundamentalData(reqId=self.ib.req_id,
                                   contract = contract,
                                   reportType = "ReportsFinStatements",
                                   fundamentalDataOptions=[])
        print(1)
        time.sleep(5)
        self.ib.req_id+=1






############### 4. Parsing Section ###############
    def filter_option_chain(self,symbol,input_detail=""):
        price = 165.00
        lower_multiplier = 0.975 # 0.9 is nice
        upper_multiplier = 1.025

        # default data
        data_detail = {"month" : 1, "lower" :price*lower_multiplier,"upper":price*1.025}

        # updating data
        if input_detail:
            for i in input_detail:
                data_detail[i] = input_detail[i]

        self.ib.filtered_option_chain = self.ib.option_chain.copy()
        current_date = datetime.today() 
        future_date = current_date + relativedelta(months=data_detail["month"])
        current_date = current_date.strftime("%Y%m")
        future_date = future_date.strftime("%Y%m")

        self.ib.filtered_option_chain[symbol]["expirations"] = [_ for _ in self.ib.filtered_option_chain[symbol]["expirations"] if current_date <= _ <= future_date]
        self.ib.filtered_option_chain[symbol]["strikes"]= [_ for _ in self.ib.filtered_option_chain[symbol]["strikes"] if data_detail["lower"] <= _ <= data_detail["upper"]]
        return self.ib.filtered_option_chain


    def toJson(self, item:dict):
        import json
        import os
        # Get current working directory
        current_directory = os.path.dirname(os.path.abspath(__file__))

        for _ in item:
            for v in item[_]["stock_data"]:
                v["volume"] = float(v['volume'])
            with open(f"{current_directory}/data/{item[_]["ticker"]}.json", "w") as outfile: 
                json.dump(item, outfile,indent=4)







