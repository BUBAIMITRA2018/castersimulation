from observal import *
from clientcomm_v1 import *
from readgeneral_v2 import *


logger = logging.getLogger("main.log")



class AreaObserver:
    def __init__(self, observable):
        observable.register_observer(self)


    def notify(self,  *args, **kwargs):
        for item in args[0]:
            item.FwdOnlimit = args[1].readsymbolvalue(item.fwdlimitswttag,'S7WLBit','PE')
            item.RevOnlimit = args[1].readsymbolvalue(item.revlimitswttag,'S7WLBit','PE')

class railswitchprocess:
    def __init__(self,alldevices,filename):
        self.subject = Observable()
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

def readkeyandvalues(alldevice):
         railswitchdictionary = alldevice.allrailswitch.dictionary
         areas = list(railswitchdictionary.keys())
         n = 0
         while n < len(areas):
             area = areas[n]
             devices = railswitchdictionary[area]
             yield area,devices
             n = n + 1
