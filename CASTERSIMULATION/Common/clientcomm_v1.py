
from snap7 import client as c
from snap7.util import *
from logger import *
import logging
import pandas as pd
import threading

logger = logging.getLogger("main.log")
__all_ = ['communication']




class Communication:

    def __init__(self):
        self.is_connected = False
        self.plc = ""
        self.mylock = threading.Lock()


    # Connection method
    def opc_client_connect(self,filename):
        try:
            df = pd.read_excel(filename, sheet_name='Tag List')
            self.client = c.Client()
            ipaddress = str(df.iloc[0, 11])
            rackno = int(df.iloc[1, 11])
            slotno= int(df.iloc[2, 11])
            self.client.connect(ipaddress, rackno,slotno)
            is_connected = True


        except Exception as e:

            is_connected = False
            log_exception(e)
            level = logging.ERROR
            messege = "Communication" + " Error messege(process)" + str(e.args)
            logger.log(level, messege)
            self.client.disconnect()


        finally:
            if is_connected:
                return self.client
















