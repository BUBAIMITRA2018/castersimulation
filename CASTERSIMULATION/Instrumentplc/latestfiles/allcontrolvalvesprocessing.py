from observal import *
from clientcomm_v1 import *
from readgeneral_v2 import *

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
        try:
            for area, devices in readkeyandvalues(self.alldevices):
                areavalue = self.readgeneral.readsymbolvalue(area, 'S7WLBit', 'PA')
                print(areavalue)
                if areavalue == 1:
                    self.observer.notify(devices, self.readgeneral)
        except Exception as e:
            log_exception(e)
            level = logging.ERROR
            messege = "controlvalveprocess:" + " Exception rasied(process): " + str(e.args) + str(e)
            logger.log(level, messege)


def readkeyandvalues(alldevice):
    controlvalvedictionary = alldevice.allcontrolvalves.dictionary

    areas = list(controlvalvedictionary.keys())
    n = 0
    while n < len(areas):
        area = areas[n]
        devices = controlvalvedictionary[area]
        yield area, devices
        n = n + 1









