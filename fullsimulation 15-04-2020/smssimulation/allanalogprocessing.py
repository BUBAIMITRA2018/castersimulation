import pandas as pd
from logger import *
from observal import *
import calallanalog_V3
import logging
import general
from clientcomm_v1 import *
from readgeneral_v2 import *

# setup_logging_to_file("allanalogprocessing.log")
# logger = logging.getLogger("main.log")
# dfANA = pd.read_excel(r'C:\OPCUA\working_VF1_5.xls',sheet_name='AnalogTx')
# commobject = general.General('C:\OPCUA\working_VF1_5.xls')
# alanalogdevices = calallanalog_V3.Cal_AllAnalogInputs(dfANA,commobject)


class AreaObserver:
    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self,  *args, **kwargs):
        for item in args[0]:
            item.analogprocess()

class analogprocess:

    def __init__(self,alldevices,filename):
        self.subject = Observable()
        self.observer = AreaObserver(self.subject)
        self.alldevices = alldevices
        self.client = Communication()
        self.sta_con_plc = self.client.opc_client_connect(filename)
        self.observer = AreaObserver(self.subject)
        self.readgeneral = ReadGeneral(self.sta_con_plc)


    def process(self):

        for item in range(len(self.alldevices.allanalogsignalobjects.listofanalogobjects)):
            self.alldevices.allanalogsignalobjects.listofanalogobjects[item].analogprocess()

        # for area, devices in readkeyandvalues(self.alldevices):
        #    try:
        #     areavalue = self.readgeneral.readsymbolvalue(area, 'S7WLBit', 'PA')
        #     if areavalue == 1:
        #         self.observer.notify(devices, self.readgeneral)



           # except Exception as e:
           #      log_exception(e)
           #      level = logging.ERROR
           #      messege = "allanalogprocessing" + " Error messege(process)" + str(e.args)
           #      # logger.log(level, messege)
           #      log_exception(e)


def readkeyandvalues(alldevice):
    analogdictionary = alldevice.allanalogs.dictionary
    areas = list(analogdictionary.keys())
    print('there area are',areas)
    n = 0
    while n < len(areas):
        area = areas[n]
        devices = analogdictionary[area]
        yield area, devices
        n = n + 1









