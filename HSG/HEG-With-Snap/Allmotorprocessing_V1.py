
from logger import *
from observal import *
import general

comobject  = general.General()


class AreaObserver:
    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self,  *args, **kwargs):
        for item in args[0]:
            item.OnCmd = args[1].readgeneral.readtagvalue(item.cmdtag)


subject = Observable()
observer = AreaObserver(subject)

def process():
    for area, devices in readkeyandvalues(alldevices):
        try:

            areavalue = comobject.readgeneral.readtagvalue(area)

            if areavalue == 1:
                observer.notify(devices,comobject)



        except Exception as e:
            log_exception(e)




# Helper function

def onvaluechange(objects,gen):
    for item in objects:
        item.OnCmd = gen.readgeneral.readtagvalue(item.cmdtag)


def readkeyandvalues(alldevice):

         motordictionary = alldevice.allmotor1d.dictionary

         areas = list(motordictionary.keys())
         n = 0
         while n < 3:
             area = areas[n]
             devices = motordictionary[area]
             yield area,devices
             n = n + 1









