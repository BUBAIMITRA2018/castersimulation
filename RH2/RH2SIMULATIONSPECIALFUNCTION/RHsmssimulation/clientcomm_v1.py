import logging
import pandas as pd
import threading
import logger
from pyModbusTCP.client import ModbusClient

__all_ = ['communication']

class Communication:

    def __init__(self):
        self.is_connected = False
        self.plc = ""
        self.mylock = threading.Lock()


    # Connection method
    def opc_client_connect(self,filename):
        is_connected = False
        try:
            df = pd.read_excel(filename, sheet_name='Tag List')
            ipaddress = str(df.iloc[0, 11])
            portno = int(df.iloc[1, 11])


            self.client = ModbusClient(host=ipaddress, port=portno, auto_open=True)
            self.client.open()
            is_connected = self.client.is_open()    

        except Exception as e:
            is_connected = False
            logger.log_exception(e)
            level = logging.ERROR
            messege = "Communication" + " Error messege(process)" + str(e.args)
            logging.log(level, messege)
            self.client.close()


        finally:
            if is_connected:
                return self.client




































