from observable import *
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

                if (len(item.cond1) > 3):
                    item.Cond1Val = args[1].readsymbolvalue(item.cond1, 'S7WLBit', 'PE')

                if (len(item.cond2) > 3):
                    item.Cond2Val = args[1].readsymbolvalue(item.cond2, 'S7WLBit', 'PE')

                if (len(item.cond3) > 3):
                    item.Cond3Val = args[1].readsymbolvalue(item.cond3, 'S7WLBit', 'PE')

                if (len(item.cond4) > 4):
                    item.Cond4Val = args[1].readsymbolvalue(item.cond4, 'S7WLBit', 'PE')

        except Exception as e:
            level = logging.ERROR
            messege = "process" + " Error messege(AreaObserver)" + str(e.args)
            logger.log(level, messege)








class digitalprocess:
    def __init__(self,alldevices,filename):
        self.alldevices = alldevices
        self.filename = filename
        self.subject = Observable()
        self.observer = AreaObserver(self.subject)
        self.client = Communication()
        self.sta_con_plc = self.client.opc_client_connect(filename)
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
            level = logging.ERROR
            messege = "process" + " Error messege(digitalprocess)" + str(e.args)
            logger.log(level, messege)


def readkeyandvalues(alldevice):

         digitaldictionary = alldevice.alldigitalsignals.dictionary
         areas = list(digitaldictionary.keys())
         n = 0
         while n < len(areas):
             area = areas[n]
             devices = digitaldictionary[area]
             yield area,devices
             n = n + 1









