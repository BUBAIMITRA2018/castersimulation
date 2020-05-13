import logging
from logger import *
from observal import *
from clientcomm_v1 import *
from readgeneral_v2 import *


logger = logging.getLogger("main.log")


class AreaObserver:
    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self,  *args, **kwargs):
        for item in args[0]:
            item.opncomd = args[1].readsymbolvalue(item.opencmdtag)
            item.clscomd = args[1].readsymbolvalue(item.closecmdtag)


subject = Observable()
observer = AreaObserver(subject)



class sov2sprocess:
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

         sovdictionary = alldevice.allsov2s.dictionary

         areas = list(sovdictionary.keys())
         n = 0
         while n < len(areas):
             area = areas[n]
             devices = sovdictionary[area]
             yield area,devices
             n = n + 1









