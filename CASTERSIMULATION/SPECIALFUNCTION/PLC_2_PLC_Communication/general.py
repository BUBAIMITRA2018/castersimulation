from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *


__all__ = ['General']

class General():
    def __init__(self,):
        self.client = Communication()

        self.sta_con_drvplc = self.client.opc_client_connect('10.17.13.235', 0, 3)
        self.readgeneral_drvplc = ReadGeneral(self.sta_con_drvplc)
        self.writegeneral_drvplc = WriteGeneral(self.sta_con_drvplc)

        self.sta_con_tcsplc = self.client.opc_client_connect('10.17.13.237', 0, 3)
        self.readgeneral_tcsplc = ReadGeneral(self.sta_con_tcsplc)
        self.writegeneral_tcsplc = WriteGeneral(self.sta_con_tcsplc)


