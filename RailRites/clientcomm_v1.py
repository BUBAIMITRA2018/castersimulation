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
            ipaddress = '192.168.10.11'
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

    def __getstate__(self):
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        del state['mylock']
        return state

    def __setstate__(self, state):
        # Restore instance attributes.
        self.__dict__.update(state)


    # Declear property of a module
    @property
    def PLC(self):
        return self.plc



# Read connection settings from excel

def read_clienturl():

        data = df.iloc[2, 11]
        print(data)
        return data


def get_station_plc_name():

    station_name = df.iloc[0, 11]
    plc_name = df.iloc[1, 11]
    return station_name,plc_name
# Main function call


if __name__ == "__main__":
    comm = Communication()

    # print(f'plc name is : {comm.PLC}')
    # while True:
    #     comm.opc_client_connect()
    #     browser_id = '7:' + 'AR SOV OPN LS'
    #     var = comm.PLC.get_child("7:AR SOV OPN LS")
    #     value = var.get_value()
    #     print("value is : ", value)
    #     comm.client.disconnect()



































