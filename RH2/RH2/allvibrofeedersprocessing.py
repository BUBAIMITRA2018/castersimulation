
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
            item.OnCmd = args[1].readgeneral.readtagvalue(item.cmdtag,'digital')
            item.SpeedSetpoint = args[1].readgeneral.readtagvalue(item.SpeedSetpoint, 'analog')

class vibrofeederprocess:
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

         vfdictionary = alldevice.allvibrofeeder.dictionary

         areas = list(vfdictionary.keys())
         n = 0
         while n < len(areas):
             area = areas[n]
             devices = vfdictionary[area]
             yield area,devices
             n = n + 1









