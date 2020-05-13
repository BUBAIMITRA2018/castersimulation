
from observable import *
from clientcomm_v1 import *
from readgeneral_v2 import *





# setup_logging_to_file("allmotor1dprocessing.log")
logger = logging.getLogger("main.log")

class AreaObserver:

    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self,  *args, **kwargs):

        for item in args[0]:
            item.OnCmd = args[1].readsymbolvalue(item.oncmdtag,"digital")
            if len(item.offcmdtag) > 3:
                item.OffCmd = args[1].readsymbolvalue(item.offcmdtag,"digital")


class motor1dprocess:
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
         motordictionary = alldevice.allmotor1d.dictionary
         areas = list(motordictionary.keys())
         n = 0
         while n < len(areas):
             area = areas[n]
             devices = motordictionary[area]

             yield area,devices
             n = n + 1









