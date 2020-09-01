from observable import *
from clientcomm_v1 import *
from readgeneral_v2 import *


logger = logging.getLogger("main.log")

class AreaObserver:

    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self,  *args, **kwargs):
        for item in args[0]:
            item.Cond1Val = args[1].readsymbolvalue(item.cond1,'S7WLBit','PA')
            item.Cond2Val = args[1].readsymbolvalue(item.cond2, 'S7WLBit', 'PA')
            item.Cond3Val = args[1].readsymbolvalue(item.cond3, 'S7WLBit', 'PA')
            item.Cond4Val = args[1].readsymbolvalue(item.cond4, 'S7WLBit', 'PA')
#
# subject = Observable()
# observer = AreaObserver(subject)

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
        for area, devices in readkeyandvalues(alldevices):
                 areavalue = self.readgeneral.readsymbolvalue(area,'S7WLBit','PA')
                 if areavalue == 1:
                       observer.notify(devices,self.readgeneral)





def readkeyandvalues(alldevice):

         digitaldictionary = alldevice.alldigitalsignalobjects.dictionary

         areas = list(digitaldictionary.keys())
         n = 0
         while n < len(areas):
             area = areas[n]
             devices = digitaldictionary[area]
             yield area,devices
             n = n + 1









