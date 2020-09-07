from observal import *
from clientcomm_v1 import *
from readgeneral_v2 import *
from writegeneral_v2 import *


logger = logging.getLogger("main.log")

class AreaObserver:

    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self,  *args, **kwargs):
        try:
            for item in args[0]:
                item.Cond1Val = args[1].readsymbolvalue(item.cond1, 'S7WLBit', 'PA')
                item.Cond2Val = args[1].readsymbolvalue(item.cond2, 'S7WLBit', 'PA')
                item.Cond3Val = args[1].readsymbolvalue(item.cond3, 'S7WLBit', 'PA')
                item.Cond4Val = args[1].readsymbolvalue(item.cond4, 'S7WLBit', 'PA')

        except Exception as e:
            log_exception(e)
            level = logging.ERROR
            messege = "digitalprocess:" + " Exception rasied(AreaObserver): " + str(e.args) + str(e)
            logger.log(level, messege)


class digitalprocess:
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
                    self.observer.notify(devices, readgeneral)

        except Exception as e:
            log_exception(e)
            level = logging.ERROR
            messege = "digitalprocess:" + " Exception rasied(process): " + str(e.args) + str(e)
            logger.log(level, messege)





def readkeyandvalues(alldevice):

         digitaldictionary = alldevice.alldigitalsignalobjects.dictionary

         areas = list(digitaldictionary.keys())
         n = 0
         while n < len(areas):
             area = areas[n]
             devices = digitaldictionary[area]
             yield area,devices
             n = n + 1









