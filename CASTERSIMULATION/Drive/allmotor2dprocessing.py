
from observal import *
from clientcomm_v1 import *
from readgeneral_v2 import *
import gc



logger = logging.getLogger("main.log")



class AreaObserver:
    def __init__(self, observable):
        observable.register_observer(self)


    def notify(self,  *args, **kwargs):
        try:
            for item in args[0]:
                item.FwdOnCmd = args[1].readsymbolvalue(item.fwdcmdtag, 'S7WLBit', 'PA')
                item.RevOnCmd = args[1].readsymbolvalue(item.revcmdtag, 'S7WLBit', 'PA')

        except Exception as e:
            level = logging.INFO
            messege = 'AreaObserver' + ":" + " Exception rasied(process): " + str(e.args) + str(e)
            logger.log(level, messege)


class motor2dprocess:
    def __init__(self,alldevices,filename):
        self.subject = Observable()
        self.alldevices = alldevices
        self.client = Communication()
        self.sta_con_plc = self.client.opc_client_connect(filename)
        self.observer = AreaObserver(self.subject)
        self.readgeneral = ReadGeneral(self.sta_con_plc)

    def process(self):
        try:
            for area, devices in readkeyandvalues(self.alldevices):

                areavalue = self.readgeneral.readsymbolvalue(area, 'S7WLBit', 'PA')
                if areavalue == 1:
                    self.observer.notify(devices, self.readgeneral)



        except Exception as e:
            log_exception(e)
            level = logging.INFO
            messege = 'motor2dprocess' + ":" + " Exception rasied(process): " + str(e.args) + str(e)
            logger.log(level, messege)



def readkeyandvalues(alldevice):
         motordictionary = alldevice.allmotor2d.dictionary
         areas = list(motordictionary.keys())
         n = 0
         while n < len(areas):
             area = areas[n]
             devices = motordictionary[area]
             yield area,devices
             n = n + 1









