from snap7.snap7types import areas, S7WLBit
from  clientcomm_v1 import *
import pandas as pd


__all__ = ['WriteGeneral']



class WriteGeneral():

    def __init__(self, client):
        self.client = client
        self.mylock = threading.Lock()




    def writesymbolvalue(self, address, tagvalue, datatype):
        addressconverted = float(address)
        self.byte = int(addressconverted)
        self.bit = round((addressconverted - self.byte)*10)
        if datatype == 'S7WLBit':
            self.result = self.client.read_area(areas['PE'], 0, self.byte, S7WLBit)
            set_bool(self.result, 0, self.bit, tagvalue)
        elif datatype == 'S7WLByte' or datatype == 'S7WLWord':
            self.result = self.client.read_area(areas['PE'], 0, self.byte, S7WLBit)
            set_int(self.result, 0, tagvalue)
        elif datatype == 'S7WLReal':
            self.result = self.client.read_area(areas['PE'], 0, self.byte, S7WLBit)
            set_real(self.result, 0, tagvalue)
        elif datatype == 'S7WLDWord':
            self.result = self.client.read_area(areas['PE'], 0, self.byte, S7WLBit)
            set_dword(self.result, 0, tagvalue)
        self.client.write_area(areas['PE'], 0, self.byte, self.result)

    def writeallvalue(self, address, tagvalue, datatype,dataclass):
        addressconverted = float(address)
        self.byte = int(addressconverted)
        self.bit = round((addressconverted - self.byte)*10)
        self.daat = str(dataclass)
        if datatype == 'S7WLBit':
            self.result = self.client.read_area(areas[self.daat], 0, self.byte, S7WLBit)
            set_bool(self.result, 0, self.bit, tagvalue)
        elif datatype == 'S7WLByte' or datatype == 'S7WLWord':
            self.result = self.client.read_area(areas[self.daat], 0, self.byte, S7WLBit)
            set_int(self.result, 0, tagvalue)
        elif datatype == 'S7WLReal':
            self.result = self.client.read_area(areas[self.daat], 0, self.byte, S7WLBit)
            set_real(self.result, 0, tagvalue)
        elif datatype == 'S7WLDWord':
            self.result = self.client.read_area(areas[self.daat], 0, self.byte, S7WLBit)
            set_dword(self.result, 0, tagvalue)
        self.client.write_area(areas[self.daat], 0, self.byte, self.result)

    def writeDBvalue(self, address, tagvalue, datatype, dataarea):
        addressconverted = float(address)
        self.byte = int(addressconverted)
        self.bit = round((addressconverted - self.byte) * 10)
        self.dataarea = int(dataarea)

        if datatype == 'S7WLBit':
            self.result = self.client.read_area(areas['DB'], self.dataarea, self.byte, S7WLBit)
            set_bool(self.result, 0, self.bit, tagvalue)
        elif datatype == 'S7WLByte' or datatype == 'S7WLWord':
            self.result = self.client.read_area(areas['DB'], self.dataarea, self.byte, S7WLBit)
            set_int(self.result, 0, tagvalue)
        elif datatype == 'S7WLReal':
            self.result = self.client.read_area(areas['DB'], self.dataarea, self.byte, S7WLBit)
            set_real(self.result, 0, tagvalue)
        elif datatype == 'S7WLDWord':
            self.result = self.client.read_area(areas['DB'], self.dataarea, self.byte, S7WLBit)
            set_dword(self.result, 0, tagvalue)
        self.client.write_area(areas['DB'], self.dataarea, self.byte, self.result)




















