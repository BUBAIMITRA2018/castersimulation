from logger import *
from observal import *
import logging
logger = logging.getLogger("main.log")

class AreaObserver:
    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self,  *args, **kwargs):
        for item in args[0]:
            item.BreakOpenCmd = args[1].readgeneral.readsymbolvalue(item.breakopentag,'S7WLBit','PA')


subject = Observable()
observer = AreaObserver(subject)

def process(comobject,alldevices):
    for area, devices in readkeyandvalues(alldevices):
        try:
            areavalue = comobject.readgeneral.readsymbolvalue(area,'S7WLBit','PA')

            if areavalue == 1:
                observer.notify(devices,comobject)

        except Exception as e:
            log_exception(e)
            level = logging.ERROR
            messege = "allencoderprocessing" + " Error messege(process)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)


def readkeyandvalues(alldevice):
         encoderdictionary = alldevice.allencoders.dictionary
         areas = list(encoderdictionary.keys())
         n = 0
         while n < len(areas):
             area = areas[n]
             devices = encoderdictionary[area]
             yield area,devices
             n = n + 1

