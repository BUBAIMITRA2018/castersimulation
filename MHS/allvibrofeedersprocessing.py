
from logger import *
from observal import *
from clientcomm_v1 import *
from readgeneral_v2 import *
from writegeneral_v2 import *
import logging

logger = logging.getLogger("main.log")

class AreaObserver:
    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self,  *args, **kwargs):
        try:
            for item in args[0]:
                item.OnCmd = args[1].readsymbolvalue(item.cmdtag, 'S7WLBit', 'PA')

        except Exception as e:
            log_exception(e)
            level = logging.ERROR
            messege = "allvibrofeederprocessing" + " Error messege(AreaObserver)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)






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

        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)

            for area, devices in readkeyandvalues(self.alldevices):
                areavalue = readgeneral.readsymbolvalue(area, 'S7WLBit', 'PA')


                if areavalue == 1:

                    self.observer.notify(devices, self.readgeneral)



        except Exception as e:
            log_exception(e)
            level = logging.ERROR
            messege = "allvibrofeederprocessing" + " Error messege(process)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)


def readkeyandvalues(alldevice):

         vfdictionary = alldevice.allvibrofeeders.dictionary

         areas = list(vfdictionary.keys())
         n = 0
         while n < len(areas):
             area = areas[n]
             devices = vfdictionary[area]
             yield area,devices
             n = n + 1









