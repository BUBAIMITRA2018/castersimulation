from snap7.snap7types import areas, S7WLBit, S7WLWord, S7WLReal
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
        data1 = addressconverted[addressconverted.find("b") + 1:addressconverted.find(".")]
        data2 = addressconverted[addressconverted.find("d", 2) + 1:]
        data3 = data2[data2.find("b") + 1:]
        data3 = float(data3[1:])
        self.byte = int(data3)

        self.bit = round((data3 - self.byte) * 10)

        self.dataarea = int(data1)

        if datatype == 'S7WLBit':
            self.result = self.client.read_area(areas['DB'], self.dataarea, self.byte, S7WLBit)
            return get_bool(self.result, 0, self.bit)
        elif datatype == 'S7WLByte' or datatype == 'S7WLWord':
            self.result = self.client.read_area(areas['DB'], self.dataarea, self.byte, S7WLWord)
            return get_int(self.result, 0)
        elif datatype == 'S7WLReal':
            self.result = self.client.read_area(areas['DB'], self.dataarea, self.byte, S7WLReal)
            return get_real(self.result, 0)
        elif datatype == "S7WLDWord":
            return get_dword(self.result, 0)
        else:
            return None

    def __getstate__(self):
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        del state['mylock']
        return state


if __name__ == "__main__":
    import general
    from snap7 import client as c
    comm_object = general.General()
    A = comm_object.readgeneral.readsymbolvalue('11.6', 'S7WLBit', 'PA')
    B = comm_object.readgeneral.readDBvalue('2.2','S7WLBit','DB',102)
    print('the value of b is ',B)




























