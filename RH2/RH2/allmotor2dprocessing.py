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
        self.alldevices = alldevices
        self.client = Communication()
        self.sta_con_plc = self.client.opc_client_connect(filename)
        self.observer = AreaObserver(self.subject)
        self.readgeneral = ReadGeneral(self.sta_con_plc)

    def process(self):

        for area, devices in readkeyandvalues(self.alldevices):

            areavalue = self.readgeneral.readsymbolvalue(area, "digital")
            if areavalue == 1:
                self.observer.notify(devices, self.readgeneral)









# def process(comobject,alldevices,filename):
#     readgeneral = ReadGeneral(comobject.sta_con_plc)
#
#     for area, devices in readkeyandvalues(alldevices):
#         areavalue = readgeneral.readsymbolvalue(area, 'S7WLBit', 'PA')
#         if areavalue == 1:
#             observer.notify(devices, readgeneral)
        # try:
        #
        #     areavalue = comobject.readgeneral.readsymbolvalue(area,'S7WLBit','PA')
        #     print("areavalue for Motor2D",areavalue)
        #
        #     if areavalue == 1:
        #         observer.notify(devices,comobject)
        #
        # except Exception as e:
        #     log_exception(e)
        #     level = logging.ERROR
        #     messege = "allmotor2dprocessing" + " Error messege(process)" + str(e.args)
        #     # logger.log(level, messege)
        #     # log_exception(e)


def readkeyandvalues(alldevice):
         motordictionary = alldevice.allmotor2d.dictionary
         areas = list(motordictionary.keys())
         n = 0
         while n < len(areas):
             area = areas[n]
             devices = motordictionary[area]
             yield area,devices
             n = n + 1









