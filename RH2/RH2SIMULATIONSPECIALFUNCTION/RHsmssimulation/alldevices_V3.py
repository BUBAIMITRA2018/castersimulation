import callLTC1
import callLTC2
import  callLTC1Standby
import  callLTC2Standby
import   callLanceStandbyOperation
import  callLanceOperation



class AllDevices:

    def __init__(self,import_file_path):



        self.LTC1objects = callLTC1.Cal_LTC1(import_file_path)
        self.LTC2objects = callLTC2.Cal_LTC2(import_file_path)
        self.LTC1Standbyobjects = callLTC1Standby.Cal_LTC1Standby(import_file_path)
        self.LTC2Standbyobjects = callLTC2Standby.Cal_LTC2Standby(import_file_path)
        self.Lanceobjects = callLanceOperation.Cal_Lanceoperation(import_file_path)
        self.Lancestandbyobjects = callLanceStandbyOperation.Cal_Lancestandbyoperation(import_file_path)




    @property
    def CallTC1(self):
        return self.LTC1objects

    @property
    def CallTC2(self):
        return self.LTC2objects

    @property
    def Callltc1stanby(self):
        return self.LTC1Standbyobjects

    @property
    def Callltc2stanby(self):
        return self.LTC2Standbyobjects

    @property
    def Calllance(self):
        return self.Lanceobjects

    @property
    def Calllancestandby(self):
        return self.Lancestandbyobjects







