from  clientcomm_v1 import *


__all__ = ['WriteGeneral']



class WriteGeneral():
    def __init__(self, client):
        self.client = client
        self.mylock = threading.Lock()

    def writesymbolvalue(self, address,datatype,value):
        if datatype == "digital":
            add = int(address)
            val = int(value)
            self.state = self.client.write_single_coil(add,val)

        if datatype == "analog":
            add = int(address)
            val = int(value)
            self.state = self.client.write_single_register(add,val)











