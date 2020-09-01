from observal import *
from clientcomm_v1 import *
from readgeneral_v2 import *
from writegeneral_v2 import *

threadlist = []

class AreaObserver:
    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self,  *args, **kwargs):
        for item in args[0]:
            thread = threading.Thread(target=self.callControlvalveprocess, args=[item])
            threadlist.append(thread)

    def callControlvalveprocess(self,item):
        while True:
            try:
                item.controlvalveprocess()

            except Exception as e:
                level = logging.INFO
                messege = "callControlvalveprocess" + ":" + " Exception rasied(process): " + str(e.args) + str(e)
                logger.log(level, messege)





class controlvalveprocess:
    def __init__(self,alldevices,filename):
        self.subject = Observable()
        self.observer = AreaObserver(self.subject)
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
            writegeneral = WriteGeneral(sta_con_plc)

            for area, devices in readkeyandvalues(self.alldevices):
                areavalue = readgeneral.readsymbolvalue(area, 'S7WLBit', 'PA')
                if areavalue == 1:
                    self.observer.notify(devices, readgeneral)


            for j in threadlist:
                j.start()


        except Exception as e:
            level = logging.ERROR
            messege = "process" +  " Error messege(controlvalveprocess)" + str(e.args)
            logger.log(level, messege)



def readkeyandvalues(alldevice):
    controlvalvedictionary = alldevice.allcontrolvalves.dictionary

    areas = list(controlvalvedictionary.keys())
    n = 0
    while n < len(areas):
        area = areas[n]
        devices = controlvalvedictionary[area]
        yield area, devices
        n = n + 1









