from observal import *
from clientcomm_v1 import *
from readgeneral_v2 import *

class AreaObserver:
    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self,  *args, **kwargs):
        for item in args[0]:
            item.analogprocess()






class analogprocess:

    def __init__(self,alldevices,filename):
        self.subject = Observable()
        self.observer = AreaObserver(self.subject)
        self.alldevices = alldevices
        self.client = Communication()
        self.sta_con_plc = self.client.opc_client_connect(filename)
        self.observer = AreaObserver(self.subject)
        self.readgeneral = ReadGeneral(self.sta_con_plc)


    def process(self):

        for item in range(len(self.alldevices.allanalogsignalobjects.listofanalogobjects)):
            self.alldevices.allanalogsignalobjects.listofanalogobjects[item].analogprocess()


def readkeyandvalues(alldevice):
    analogdictionary = alldevice.allanalogs.dictionary
    areas = list(analogdictionary.keys())
    print('there area are',areas)
    n = 0
    while n < len(areas):
        area = areas[n]
        devices = analogdictionary[area]
        yield area, devices
        n = n + 1









