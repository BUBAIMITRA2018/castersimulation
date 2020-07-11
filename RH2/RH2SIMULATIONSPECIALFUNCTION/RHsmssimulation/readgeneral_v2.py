from  clientcomm_v1 import *

__all__ = ['ReadGeneral']
class ReadGeneral():

    def __init__(self, client):
        self.client = client
        self.mylock = threading.Lock()


    def readsymbolvalue(self, address, datatype):       
            if datatype == "digital":
                add = int(address)
                self.state = self.client.read_coils(add, 1)


            if datatype == "analog":
                add = int(address)
                self.state = self.client.read_holding_registers(add, 1)


            return self.state[0]

        







































