from  clientcomm_v1 import *
import pandas as pd
import  time
import  time,traceback
__all__ = ['ReadGeneral']


# comm = Communication()

# All static method called here


# Get tags from excel sheet


class ReadGeneral():

    def __init__(self, client):
        self.client = client
        self.mylock = threading.Lock()



    def gettagfromexcel(func):
        def inner(self, idxno):
            data_to_read = df.iloc[idxno, 0]

            browser_id = '7:' + data_to_read

            return func( self,browser_id)
        return inner



    # Read tag value here

    # @gettagfromexcel
    # def readnodevalue(self, id):
    #     idtostring = str(id)
    #     try:
    #         # var = self.plcname.get_child(idtostring)
    #         # value = var.get_value()
    #         # return value
    #     except Exception as e:
    #         print(e.args)

    def readtagsymbol(self,tagname):
        n = 0
        while n < len(self.df.index):
            data = self.df.iloc[n, 1]
            if(data == tagname):
                byte = self.df.iloc[n, 3]
                bit = self.df.iloc[n, 4]
                datatype = self.df.iloc[n, 2]
                daat=self.df.iloc[n,5]
                return byte,bit,datatype,daat
            n = n + 1

    def readtagvalue(self,tagname):
        tag_id = str(tagname)
        # browser_id = '7:' + tag_id

        self.df = pd.read_excel(r'C:\OPCUA\Working_VF1_5.xls', sheet_name='OPERATION')
        self.byte, self.bit, self.datatype, self.daat = self.readtagsymbol(tagname)

        self.byte = int(self.byte)
        self.bit = int(self.bit)
        self.daat = str(self.daat)

        if self.datatype == 'S7WLBit':
            result = self.client.read_area(areas[self.daat], 0, self.byte, S7WLBit)
            return get_bool(result, 0, self.bit)
        elif self.datatype == 'S7WLByte' or self.datatype == 'S7WLWord':
            return get_int(self.result, 0)
        elif self.datatype == S7WLReal:
            return get_real(self.result, 0)
        elif self.datatype == S7WLDWord:
            return get_dword(self.result, 0)
        else:
            return None

        # value = var.get_value()
        # return value

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
        print('the byte ia ',self.byte)
        self.bit = int(addressconverted[12:13])
        print('the bit is ',self.bit)
        self.dataarea = int(addressconverted[2:5])
        print('the db naumbe ris ',self.dataarea)
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





    def __getstate__(self):
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        del state['mylock']
        return state

    # def __setstate__(self, state):
    #     # Restore instance attributes.
    #     self.__dict__.update(state)




# # Finall output
#
# def final_output():
#     comm.opc_client_connect()
#     readgeneral = ReadGeneral(comm.PLC)
#
#
#
#
#     def every(delay, task):
#         next_time = time.time() + delay
#         while True:
#             time.sleep(max(0, next_time - time.time()))
#             try:
#                 task()
#             except Exception:
#                 traceback.print_exc()
#             next_time += (time.time() - next_time)
#
#     def callreadgeneral():
#
#         for idxNo in df.index:
#             print("idx number is :", idxNo)
#             value = readgeneral.readnodevalue(idxNo)
#             tagname = df.iloc[idxNo, 0]
#             print(f" {tagname} value is : {value}")
#
#     threading.Thread(target=lambda: every(1, callreadgeneral)).start()
#
#
#
if __name__ == "__main__":
    import general
    from snap7 import client as c
    comm_object = general.General()
    A = comm_object.readgeneral.readsymbolvalue('11.6', 'S7WLBit', 'PA')
    B = comm_object.readgeneral.readDBvalue('2.2','S7WLBit','DB',102)
    print('the value of b is ',B)




























