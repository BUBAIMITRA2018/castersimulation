
from logger import *
from observal import *
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



subject = Observable()
observer = AreaObserver(subject)

def process(comobject,alldevices):
    for area, devices in readkeyandvalues(alldevices):
        try:

            areavalue = comobject.readgeneral.readtagvalue(area)

            if areavalue == 1:
                observer.notify(devices,comobject)

        except Exception as e:
            log_exception(e)
            level = logging.ERROR
            messege = "allabbdriveprocessing" + " Error messege(process)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)


def readkeyandvalues(alldevice):

         dictionary = alldevice.alldrives.dictionary

         areas = list(dictionary.keys())
         n = 0
         while n < len(areas):
             area = areas[n]
             devices = dictionary[area]
             yield area,devices
             n = n + 1









