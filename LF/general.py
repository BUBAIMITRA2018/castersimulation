from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *


__all__ = ['General']

class General():
    def __init__(self,filename):
        self.client = Communication()
        self.sta_con_plc = self.client.opc_client_connect(filename)
        self.readgeneral = ReadGeneral(self.sta_con_plc)
        self.writegeneral = WriteGeneral(self.sta_con_plc)

