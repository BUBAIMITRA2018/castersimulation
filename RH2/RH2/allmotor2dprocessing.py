import logging
from logger import *
from observal import *
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *

logger = logging.getLogger("main.log")



class AreaObserver:
    def __init__(self, observable):
        observable.register_observer(self)


    def notify(self,  *args, **kwargs):
        for item in args[0]:
            item.FwdOnCmd= args[1].readsymbolvalue(item.fwdcmdtag,"digital")
            item.RevOnCmd = args[1].readsymbolvalue(item.revcmdtag,"digital")

class motor2dprocess:
    def __init__(self,alldevices,filename):
        self.subject = Observable()
        self.filename = filename

        self.alldevices = alldevices
        self.client = Communication()
        self.sta_con_plc = self.client.opc_client_connect(filename)
        self.observer = AreaObserver(self.subject)
        self.readgeneral = ReadGeneral(self.sta_con_plc)

    def process(self):

        try:

            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)

            for area, devices in readkeyandvalues(self.alldevices):
                areavalue = readgeneral.readsymbolvalue(area, 'digital')
                if areavalue == 1:
                    self.observer.notify(devices, readgeneral)

            sta_con_plc.close()




        except Exception as e:
            level = logging.ERROR
            messege = "Motor2dprocessing" + " Error messege(Motor2dProcess)" + str(e.args)
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









