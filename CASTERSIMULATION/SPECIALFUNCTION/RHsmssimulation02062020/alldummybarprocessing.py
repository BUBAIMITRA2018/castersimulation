from logger import *
from observable import *
import logging
import time
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *




# setup_logging_to_file("allmotor1dprocessing.log")
logger = logging.getLogger("main.log")

class AreaObserver:

    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self,  *args, **kwargs):
        print("Hello subrata")
        for item in args[0]:


            item.CurrentPos = args[1].readDBvalue(item.currentpos,'S7WLWord')
            print('the value is',item.CurrentPos)


class dummybardprocess:
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

        for area, devices in readkeyandvalues(self.alldevices):
            print('the call funtion is working', area)
            areavalue = self.readgeneral.readsymbolvalue(area,'S7WLBit', 'PA')
            print(area, areavalue)

            if areavalue == 1:
                self.observer.notify(devices, self.readgeneral)









        # except Exception as e:
        #     log_exception(e)
        #     level = logging.ERROR
        #     messege = "allmotor1dprocessing" + " Error messege(process)" + str(e.args)
        #     # logger.log(level, messege)
        #     log_exception(e)



def readkeyandvalues(alldevice):

         dummybardictionary = alldevice.alldummybar.dictionary



         areas = list(dummybardictionary.keys())
         n = 0
         while n < len(areas):
             area = areas[n]
             devices = dummybardictionary[area]

             yield area,devices
             n = n + 1