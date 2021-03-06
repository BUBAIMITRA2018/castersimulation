
from logger import *
from observal import *
from clientcomm_v1 import *
from readgeneral_v2 import *
import logging

logger = logging.getLogger("main.log")

class AreaObserver:
    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self,  *args, **kwargs):
        for item in args[0]:
            item.controlword = args[1].readgeneral.readtagvalue(item.cw)
            item.speedsetpoint = args[1].readgeneral.readtagvalue(item.speedSP)

            if len(item.brakeopncmd) > 3:
                item.breakopencmd = args[1].readgeneral.readtagvalue(item.brakeopncmd)
            if len(item.startcmdtag) > 3:
                item.StartCmd = args[1].readgeneral.readtagvalue(item.startcmdtag)
            if len(item.stopcmdtag) > 3:
                item.StopCmd = args[1].readgeneral.readtagvalue(item.stopcmdtag)

class abpdriveprocessing :

    def __init__(self, alldevices, filename):
        self.subject = Observable()
        self.alldevices = alldevices
        self.observer = AreaObserver(self.subject)
        self.client = Communication()
        self.sta_con_plc = self.client.opc_client_connect(filename)
        self.observer = AreaObserver(self.subject)
        self.readgeneral = ReadGeneral(self.sta_con_plc)

    def process(self):

        for area, devices in readkeyandvalues(self.alldevices):
            areavalue = self.readgeneral.readsymbolvalue(area, 'S7WLBit', 'PA')
            if areavalue == 1:
                self.observer.notify(devices, self.readgeneral)






def readkeyandvalues(alldevice):

         dictionary = alldevice.alldrives.dictionary

         areas = list(dictionary.keys())
         n = 0
         while n < len(areas):
             area = areas[n]
             devices = dictionary[area]
             yield area,devices
             n = n + 1









