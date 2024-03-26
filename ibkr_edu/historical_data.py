from admin.ib.ibkr_api.ibkr_main.tws_api.ib_io import ib_output

import threading


connection_object = ib_output()
connection_object.connect("127.0.0.1", 7497, clientId=1) # 7497 should be paper account, please verify
connection_thread = threading.Thread(target=websocket)