from  clientcomm_v1 import *
from opcua import ua
import pandas as pd
import  time

__all__ = ['WriteGeneral']



class WriteGeneral():

    def __init__(self, client):
        self.client = client
        self.mylock = threading.Lock()




    def writenodevalue(self, address, tagvalue,datatype):
        addressconverted = float(address)
        self.byte = int(addressconverted)
        self.bit =  addressconverted - self.byte

        if datatype == 'S7WLBit':
                self.result = self.client.read_area(areas['PE'], 0, self.byte,S7WLBit )
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


    # def __getstate__(self):
    #     state = self.__dict__.copy()
    #     # Remove the unpicklable entries.
    #     del state['mylock']
    #     return state
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
    from clientcomm_v1 import *
    comm = Communication()
    client = comm.opc_client_connect()

    writegeneral = WriteGeneral(client)

    writegeneral.writenodevalue(tagname,tagvalue)












# if __name__ == "__main__":
#
#
#     final_output()
