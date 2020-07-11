
from logger import *
from observable import *
import logging
from clientcomm_v1 import *
from readgeneral_v2 import *


logger = logging.getLogger("main.log")

class AreaObserver:

    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self,  *args, **kwargs):
        for item in args[0]:

            if (len(item.cond1) > 3):
                item.Cond1Val = args[1].readsymbolvalue(item.cond1, "digital")

            if (len(item.cond2) > 3):
                item.Cond2Val = args[1].readsymbolvalue(item.cond2, "digital")

            if (len(item.cond3) > 3):
                item.Cond3Val = args[1].readsymbolvalue(item.cond3, "digital")

            if (len(item.cond4) > 4):
                item.Cond4Val = args[1].readsymbolvalue(item.cond4, "digital")



class digitalprocess:
    def __init__(self,alldevices,filename):
        self.subject = Observable()
        self.alldevices = alldevices
        self.filename = filename
        self.subject = Observable()
        self.observer = AreaObserver(self.subject)
        self.client = Communication()
        self.sta_con_plc = self.client.opc_client_connect(filename)
        self.observer = AreaObserver(self.subject)
        self.readgeneral = ReadGeneral(self.sta_con_plc)

    def process(self):

        for area, devices in readkeyandvalues(self.alldevices):
            areavalue = self.readgeneral.readsymbolvalue(area, "digital")

            if areavalue == 1:
                self.observer.notify(devices, self.readgeneral)




def readkeyandvalues(alldevice):

         digitaldictionary = alldevice.alldigitalsignalobjects.dictionary

         areas = list(digitaldictionary.keys())
         n = 0
         while n < len(areas):
             area = areas[n]
             devices = digitaldictionary[area]
             yield area,devices
             n = n + 1









