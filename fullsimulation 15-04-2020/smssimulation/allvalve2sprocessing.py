import logging
from logger import *
from observal import *

setup_logging_to_file("allvalve2sprocessing.log")
logger = logging.getLogger("main.log")


class AreaObserver:
    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self,  *args, **kwargs):
        for item in args[0]:
            item.opncomd = args[1].readgeneral.readtagvalue(item.opencmdtag)
            item.clscomd = args[1].readgeneral.readtagvalue(item.closecmdtag)


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
            messege = "allsov2sprocessing" + " Error messege(process)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)


def readkeyandvalues(alldevice):

         sovdictionary = alldevice.allsov2s.dictionary

         areas = list(sovdictionary.keys())
         n = 0
         while n < len(areas):
             area = areas[n]
             devices = sovdictionary[area]
             yield area,devices
             n = n + 1









