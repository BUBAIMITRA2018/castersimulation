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
            set_int(self.result, 0,tagvalue)
        elif datatype == 'S7WLReal':
            self.result = self.client.read_area(areas['PE'], 0, self.byte, S7WLBit)
            set_real(self.result, 0, tagvalue)
        elif datatype == 'S7WLDWord':
            self.result = self.client.read_area(areas['PE'], 0, self.byte, S7WLBit)
            set_dword(self.result, 0, tagvalue)
        self.client.write_area(areas['PE'], 0, self.byte, self.result)

    def writeDBvalue(self, address, tagvalue, datatype, dataarea):
        addressconverted = str(address)
        data1 = addressconverted[addressconverted.find("b") + 1:addressconverted.find(".")]
        data2 = addressconverted[addressconverted.find("d", 2) + 1:]
        data3 = data2[data2.find("b") + 1:]
        data3 = float(data3[1:])
        self.byte = int(data3)
        self.bit = round((data3 - self.byte) * 10)
        self.dataarea = int(data1)

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




















