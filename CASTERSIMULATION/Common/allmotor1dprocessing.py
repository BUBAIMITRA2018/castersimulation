
from logger import *
from observable import *
import logging

setup_logging_to_file("allmotor1dprocessing.log")
logger = logging.getLogger("main.log")

class AreaObserver:

    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self,  *args, **kwargs):
        for item in args[0]:
            item.OnCmd = args[1].readgeneral.readtagvalue(item.oncmdtag)
            if len(item.offcmdtag) > 3:
                item.OffCmd = args[1].readgeneral.readtagvalue(item.offcmdtag)


subject = Observable()
observer = AreaObserver(subject)

def process(comobject,alldevices):
    for area, devices in readkeyandvalues(alldevices):
        try:
            areavalue = comobject.readgeneral.readtagvalue(area)
            print(area,areavalue)
            if areavalue == 1:
                observer.notify(devices,comobject)

        except Exception as e:
            log_exception(e)
            level = logging.ERROR
            messege = "allmotor1dprocessing" + " Error messege(process)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)


def readkeyandvalues(alldevice):

         motordictionary = alldevice.allmotor1d.dictionary

         areas = list(motordictionary.keys())
         n = 0
         while n < len(areas):
             area = areas[n]
             devices = motordictionary[area]
             yield area,devices
             n = n + 1









