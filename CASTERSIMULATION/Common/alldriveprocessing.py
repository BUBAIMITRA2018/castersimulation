import pandas as pd
from logger import *
from observal import *
import calallABPdrives_V3
import logging
import general
dfANA = pd.read_excel(r'C:\OPCUA\Working_VF1_5.xls', sheet_name='AnalogTx')
commobject = general.General()



class AreaObserver:
    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self,  *args, **kwargs):
        for item in args[0]:
            item.analogprocess()


subject = Observable()
observer = AreaObserver(subject)

def process(logger):
    alldevices = calallABPdrives_V3.Cal_ABBDrives(dfANA,commobject)
    while True:
        for area, devices in readkeyandvalues(alldevices ):
            try:
                areavalue = commobject.readgeneral.readtagvalue(area)
                if areavalue == 1:
                    observer.notify(devices)

            except Exception as e:
                log_exception(e)
                level = logging.ERROR
                messege = "allmotor1dprocessing" + " Error messege(process)" + str(e.args)
                logger.log(level, messege)
                log_exception(e)

def readkeyandvalues(alldevice):

         dictionary = alldevice.listofdrives.dictionary

         areas = list(dictionary.keys())
         n = 0
         while n < len(areas):
             area = areas[n]
             devices = dictionary[area]
             yield area,devices
             n = n + 1









