from  clientcomm_v1 import *
from opcua import ua
import pandas as pd
import  time

__all__ = ['writenodevalue']



# All static method called here

# df = pd.read_excel(r'D:\OPCUA\Working_VF1.xls', sheet_name='ReadGeneral')


# Get tags from excel sheet

# def gettagfromexcel(func):
#     def inner(plc, idxno):
#         data_to_read = df.iloc[idxno - 2, 0]
#
#         browser_id = '7:' + data_to_read
#
#         return func(plc, browser_id)
#
#     return inner


# Read tag value here



def write_tagmodifier(func):
    def inner(plc_name,tagname,setvalue):
        browser_id = '7:' + tagname
        print(f"browser id: {browser_id}")
        return func(plc_name,browser_id,setvalue)
    return inner

@write_tagmodifier
def writenodevalue(plcname,tagname: str,setvalue):
    covertvalue = 0
    idtostring = str(id)
    var = plcname.get_child(tagname)
    print(f"var id is:{var}")
    value = var.get_value()
    print(f"present value is:{value}")
    variantType =  var.get_data_type_as_variant_type()
    print(f"present varriant is:{variantType}")

    if str(variantType) == "VariantType.Float":
        covertvalue = float(setvalue)

    else:
        covertvalue = int(setvalue)


    dv = ua.DataValue(ua.Variant(covertvalue, variantType))
    print(f"data value is : {dv}")
    var.set_value(dv)
    return True


# Finall output

def final_output():
    comm = Communication()
    client = comm.opc_client_connect()
    if client :
        tag_name = str(input("please enter the tag name :"))

        writenodevalue(comm.PLC,tag_name,1)






if __name__ == "__main__":


    final_output()
