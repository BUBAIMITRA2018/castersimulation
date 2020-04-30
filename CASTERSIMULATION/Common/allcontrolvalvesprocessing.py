import pandas as pd
from logger import *
from observal import *
import calallcontrolvalves_V3
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import logging
import general

# setup_logging_to_file("allanalogprocessing.log")
# logger = logging.getLogger("main.log")
# dfCNTRLVALVES = pd.read_excel(r'C:\OPCUA\Working_VF1_5.xls', sheet_name='ControlValves')
# commobject = general.General('C:\OPCUA\Working_VF1_5.xls')
# allcontrolvalvesdevies = calallcontrolvalves_V3.Cal_AllControlValves(dfCNTRLVALVES,commobject)

class AreaObserver:
    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self,  *args, **kwargs):
        for item in args[0]:
            item.controlvalveprocess()




class controlvalveprocess:
    def __init__(self,alldevices,filename):
        self.subject = Observable()
        self.observer = AreaObserver(self.subject)
        self.alldevices = alldevices
        self.client = Communication()
        self.sta_con_plc = self.client.opc_client_connect(filename)
        self.observer = AreaObserver(self.subject)
        self.readgeneral = ReadGeneral(self.sta_con_plc)

    def process(self):

        for area, devices in readkeyandvalues(self.alldevices):
            areavalue = self.readgeneral.readsymbolvalue(area, 'S7WLBit', 'PA')
            if areavalue == 1:
                self.observer.notify(devices, self.readgeneral)






# def process(comobject,alldevices):
#
#     while True:
#         for area, devices in readkeyandvalues(alldevices):
#             try:
#                 areavalue = comobject.readgeneral.readsymbolvalue(area,'S7WLBit','PA')
#                 if areavalue == 1:
#                     observer.notify(devices,comobject)
#
#             except Exception as e:
#                 log_exception(e)
#                 level = logging.ERROR
#                 messege = "allcontrolvalvesprocessing" + " Error messege(process)" + str(e.args)
#                 # logger.log(level, messege)
#                 # log_exception(e)
#

def readkeyandvalues(alldevice):
    controlvalvedictionary = alldevice.allcontrolvalves.dictionary

    areas = list(controlvalvedictionary.keys())
    n = 0
    while n < len(areas):
        area = areas[n]
        devices = controlvalvedictionary[area]
        yield area, devices
        n = n + 1









