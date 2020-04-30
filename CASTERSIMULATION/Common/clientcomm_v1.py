from opcua import Client
from snap7 import client as c
from snap7.util import *
from snap7.snap7types import *
from logger import *
import logging
import pandas as pd
import threading


__all_ = ['communication']




class Communication:

    def __init__(self):
        self.is_connected = False
        self.plc = ""
        self.mylock = threading.Lock()


    # Connection method
    def opc_client_connect(self,filename):
        try:
            # df = pd.read_excel(r'C:\OPCUA\Working_VF1_5.xls', sheet_name='Tag List')
            df = pd.read_excel(filename, sheet_name='Tag List')
            # df = pd.read_excel(excelpath, sheet_name='Tag List')
            self.client = c.Client()
            ipaddress = str(df.iloc[0, 11])
            rackno = int(df.iloc[1, 11])
            slotno= int(df.iloc[2, 11])
            self.client.connect(ipaddress, rackno,slotno)

            # #  Read connection string for url
            # url = read_clienturl()

            # self.client = Client(url)
            # self.client.find_servers(uris='opc.tcp://WAP120153:55101/')
            # print(self.client)
            # self.client.connect()
            is_connected = True
            # root = self.client.get_root_node()
            # print(root)
            # objects = root.get_child('Objects')
            # symbols = objects.get_child('1:SYM:')
            # stnname,plcname = get_station_plc_name()
            # stnametostring = '7:' + stnname
            # plcnametostring = '7:' + plcname
            # station_name = symbols.get_child(stnametostring)
            # self.plc = station_name.get_child(plcnametostring)



        except Exception as e:
            is_connected = False

            print("My error is :",e)
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



































