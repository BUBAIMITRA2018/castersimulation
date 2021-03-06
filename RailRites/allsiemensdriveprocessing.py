

from observable import *
import logging
from clientcomm_v1 import *
from readgeneral_v2 import *

logger = logging.getLogger("main.log")
threadlist = []

class AreaObserver:

    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self,  *args, **kwargs):
        for item in args[0]:
            try:

                # threading = multiprocessing.Process(target=self.callmotor2dprocess,args=(item))

                thread = threading.Thread(target=self.callsiemendsdriveprocess, args=[item])
                threadlist.append(thread)

            except Exception as e:

                level = logging.INFO

                messege = "NOTIFY" + ":" + " Exception rasied(process): " + str(e.args) + str(e)

                logger.log(level, messege)

    def callsiemendsdriveprocess(self, item):
        while True:
            try:
                item.driveprocess



            except Exception as e:
                level = logging.INFO

                messege = "calldriveprocess" + ":" + " Exception rasied(process): " + str(e.args) + str(e)

                logger.log(level, messege)


def __init__(self, alldevices, filename):
    self.subject = Observable()
    self.alldevices = alldevices

    self.client = Communication()
    self.sta_con_plc = self.client.opc_client_connect(filename)
    self.observer = AreaObserver(self.subject)
    self.readgeneral = ReadGeneral(self.sta_con_plc)


def process(self, filename):
    try:
        for area, devices in readkeyandvalues(self.alldevices):

            areavalue = self.readgeneral.readsymbolvalue(area, 'S7WLBit', 'PA')
            if areavalue == 1:
                self.observer.notify(devices, filename)

        for j in threadlist:
            j.start()



    except Exception as e:
        level = logging.INFO
        messege = "PROCCESS" + ":" + " Exception rasied(process): " + str(e.args) + str(e)
        logger.log(level, messege)



def readkeyandvalues(alldevice):

         siemensdrivedictionary = alldevice.allsiemensdrives.dictionary
         areas = list(siemensdrivedictionary.keys())
         n = 0
         while n < len(areas):
             area = areas[n]
             devices = siemensdrivedictionary[area]
             yield area,devices
             n = n + 1









