from observable import *
from clientcomm_v1 import *
from readgeneral_v2 import *

logger = logging.getLogger("main.log")

class AreaObserver:

    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self,  *args, **kwargs):
        for item in args[0]:
            item.speedsetpoint = args[1].readsymbolvalue(item.Sptag,'S7WLWord','PA')

class cylinderprocess:
    def __init__(self,alldevices,filename):
        self.subject = Observable()
        self.alldevices = alldevices
        self.filename = filename
        self.observer = AreaObserver(self.subject)
        self.client = Communication()
        self.sta_con_plc = self.client.opc_client_connect(filename)
        self.readgeneral = ReadGeneral(self.sta_con_plc)


    # def callobserver(self,area,devices,filename):
    #     while True:
    #         try:
    #             client = Communication()
    #             sta_con_plc = self.client.opc_client_connect(filename)
    #             readgeneral = ReadGeneral(self.sta_con_plc)
    #             areavalue = self.readgeneral.readsymbolvalue(area,'S7WLWord','PA')
    #             if areavalue == 1:
    #                 self.observer.notify(devices, self.readgeneral)
    #
    #             sta_con_plc.disconnect()
    #
    #             # areavalue = self.readgeneral.readsymbolvalue(area, "digital")
    #             # if areavalue == 1:
    #             #     self.observer.notify(devices, self.readgeneral)
    #
    #         except Exception as e:
    #             level = logging.ERROR
    #             messege = "Cylinder" + " Error messege(Obsrver process)" + str(e.args)
    #             logger.log(level, messege)

    def process(self):

        for area, devices in readkeyandvalues(self.alldevices):
            print("doddododdododododododododododododo")
            # threading.Thread(target=self.callobserver, args=(area, devices, self.filename)).start()
            areavalue = self.readgeneral.readsymbolvalue(area, 'S7WLBit', 'PA')

            if areavalue == 1:
                self.observer.notify(devices, self.readgeneral)

def readkeyandvalues(alldevice):

         cylinderdictionary = alldevice.allcylinder.dictionary

         areas = list(cylinderdictionary.keys())
         n = 0
         while n < len(areas):
             area = areas[n]
             devices = cylinderdictionary[area]

             yield area,devices
             n = n + 1









