from  clientcomm_v1 import *
from opcua import ua
import pandas as pd
import  time

__all__ = ['WriteGeneral']



class WriteGeneral():

    def __init__(self, client):
        self.client = client
        self.mylock = threading.Lock()

    # def write_tagmodifier(func):
    #     def inner(self, tagname, setvalue):
    #         browser_id = '7:' + tagname
    #         return func(self, browser_id, setvalue)
    #     return inner

    # @write_tagmodifier



    def readtagsymbol(self,tagname):
        n = 0
        while n < len(self.df.index):
            data = self.df.iloc[n, 1]
            if(data == tagname):
                byte = self.df.iloc[n, 3]
                bit = self.df.iloc[n, 4]
                datatype = self.df.iloc[n, 2]
                return byte,bit,datatype
            n = n + 1


    def writenodevalue(self, tagname, tagvalue):
        tag_id = str(tagname)
        self.df = pd.read_excel(r'C:\OPCUA\Working_VF1_5.xls', sheet_name='OPERATION')
        self.byte, self.bit, self.datatype = self.readtagsymbol(tagname)
        self.byte = int(self.byte)
        self.bit = int(self.bit)
        if self.datatype == 'S7WLBit':
                self.result = self.client.read_area(areas['PE'], 0, self.byte,S7WLBit )
                set_bool(self.result, 0, self.bit, tagvalue)
        elif self.datatype == 'S7WLByte' or self.datatype == 'S7WLWord':
                self.result = self.client.read_area(areas['PE'], 0, self.byte, S7WLBit)
                set_int(self.result, 0, tagvalue)
        elif self.datatype == 'S7WLReal':
                self.result = self.client.read_area(areas['PE'], 0, self.byte, S7WLBit)
                set_real(self.result, 0, tagvalue)
        elif self.datatype == 'S7WLDWord':
                self.result = self.client.read_area(areas['PE'], 0, self.byte, S7WLBit)
                set_dword(self.result, 0, tagvalue)
        self.client.write_area(areas['PE'], 0, self.byte, self.result)


    def writesymbolvalue(self, address, tagvalue, datatype):
        addressconverted = float(address)
        print(addressconverted)
        self.byte = int(addressconverted)
        print(self.byte)

        self.bit = round((addressconverted - self.byte)*10)
        print(self.bit)
        if datatype == 'S7WLBit':
            self.result = self.client.read_area(areas['PE'], 0, self.byte, S7WLBit)
            print("hi")
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

    def __getstate__(self):
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        del state['mylock']
        return state
    #     try:
    #         covertvalue = 0
    #         var = self.plcname.get_child(tagname)
    #
    #         value = var.get_value()
    #
    #         variantType = var.get_data_type_as_variant_type()
    #
    #         if str(variantType) == "VariantType.Float":
    #             covertvalue = float(setvalue)
    #
    #         else:
    #             covertvalue = int(setvalue)
    #
    #         dv = ua.DataValue(ua.Variant(covertvalue, variantType))
    #
    #         var.set_value(dv)
    #         return True
    #     except Exception as e:
    #         print("WRITE GENERAL ERROR IS :",e.args)
    #
    # def __getstate__(self):
    #     state = self.__dict__.copy()
    #     # Remove the unpicklable entries.
    #     del state['mylock']
    #     return state
    #
    # # def __setstate__(self, state):
    # #     # Restore instance attributes.
    # #     self.__dict__.update(state)










# Finall output

# def final_output():
#     comm = Communication()
#     client = comm.opc_client_connect()
#     if client :
#         tag_name = str(input("please enter the tag name :"))
#         writegenral = WriteGeneral(comm.PLC)
#         writegenral.writenodevalue(tag_name,1)
if __name__ == "__main__":
    import general
    from snap7 import client as c
    comm_object = general.General()
    comm_object.writegeneral.writesymbolvalue('4.6',1,'S7WLBit')











