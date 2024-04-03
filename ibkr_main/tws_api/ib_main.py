from ib_client import ib_client

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

############### Program Codes ###############
# initialize client object
item = ib_client()

# item.contract_details("AAPL")
print(item.req_option_chain("AAPL"))

# close loop
item.close_loop()





