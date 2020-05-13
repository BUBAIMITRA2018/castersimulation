
from logger import *
from observable import *
import logging

logger = logging.getLogger("main.log")

class AreaObserver:

    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self,  *args, **kwargs):
        for item in args[0]:
            item.Cond1Val = args[1].readgeneral.readsymbolvalue(item.cond1,'S7WLBit','PA')
            item.Cond2Val = args[1].readgeneral.readsymbolvalue(item.cond2, 'S7WLBit', 'PA')
            item.Cond3Val = args[1].readgeneral.readsymbolvalue(item.cond3, 'S7WLBit', 'PA')
            item.Cond4Val = args[1].readgeneral.readsymbolvalue(item.cond4, 'S7WLBit', 'PA')

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
            messege = "alldigitalprocessing" + " Error messege(process)" + str(e.args)
            # logger.log(level, messege)
            log_exception(e)



def readkeyandvalues(alldevice):

         digitaldictionary = alldevice.alldigitalsignalobjects.dictionary

         areas = list(digitaldictionary.keys())
         n = 0
         while n < len(areas):
             area = areas[n]
             devices = digitaldictionary[area]
             yield area,devices
             n = n + 1









