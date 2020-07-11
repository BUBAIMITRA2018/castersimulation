from snap7.snap7types import areas, S7WLBit, S7WLWord
from  clientcomm_v1 import *
__all__ = ['ReadGeneral']



class ReadGeneral():

    def __init__(self, client):
        self.client = client
        self.mylock = threading.Lock()




    def readsymbolvalue(self, address, datatype, dataclass):

        addressconverted = float(address)
        self.byte = int(addressconverted)
        self.bit = round((addressconverted - self.byte)*10)
        self.daat = str(dataclass)
        if datatype == 'S7WLBit':
            self.result = self.client.read_area(areas[self.daat], 0, self.byte, S7WLBit)
            return get_bool(self.result, 0, self.bit)
        elif datatype == 'S7WLByte' or datatype == 'S7WLWord':
            self.result = self.client.read_area(areas[self.daat], 0, self.byte, S7WLWord)
            return get_int(self.result, 0)
        elif datatype == S7WLReal:
            return get_real(self.result, 0)
        elif datatype == S7WLDWord:
            return get_dword(self.result, 0)
        else:
            return None



    def readDBvalue(self, address, datatype):

        addressconverted = str(address)
        self.byte = int(addressconverted[9:11])
        self.bit = int(addressconverted[12:13])
        self.dataarea = int(addressconverted[2:5])

        if datatype == 'S7WLBit':
            self.result = self.client.read_area(areas['DB'], self.dataarea, self.byte, S7WLBit)
            return get_bool(self.result, 0, self.bit)
        elif datatype == 'S7WLByte' or datatype == 'S7WLWord':
            self.result = self.client.read_area(areas['DB'], self.dataarea, self.byte, S7WLWord)
            return get_int(self.result, 0)
        elif datatype == S7WLReal:
            return get_real(self.result, 0)
        elif datatype == S7WLDWord:
            return get_dword(self.result, 0)
        else:
            return None
































