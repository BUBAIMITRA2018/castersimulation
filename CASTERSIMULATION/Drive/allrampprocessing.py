from observal import *
from clientcomm_v1 import *
from readgeneral_v2 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *

class AreaObserver:
    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self,  *args, **kwargs):
        for item in args[0]:
            inverse_condition = False
            propotional_condition = False



            if len(item.cmdtag5) > 3:
                inverse_condition = (args[1].readsymbolvalue(item.cmdtag5, 'S7WLBit', 'PE')) \
                                    or (args[1].readsymbolvalue(item.cmdtag6, 'S7WLBit', 'PE')) \
                                    or (args[1].readsymbolvalue(item.cmdtag7, 'S7WLBit', 'PE')) \
                                    or (args[1].readsymbolvalue(item.cmdtag8, 'S7WLBit', 'PE'))
                print("inverse command",inverse_condition)


            print("tag is ", item.cmdtag1)


            if len(item.cmdtag1) > 3:

                propotional_condition = (args[1].readsymbolvalue(item.cmdtag1, 'S7WLBit', 'PE'))\
                                        and (args[1].readsymbolvalue(item.cmdtag2, 'S7WLBit', 'PE'))\
                                        and (args[1].readsymbolvalue(item.cmdtag3, 'S7WLBit', 'PE')) \
                                        and (args[1].readsymbolvalue(item.cmdtag4, 'S7WLBit', 'PE'))

                print("propotional command",propotional_condition)


            if len(item.cmdtag1) > 3:
                print(item.cmdtag1)
                item.IncreaseCmd = propotional_condition and not inverse_condition


            if len(item.cmdtag5) > 3:
                item.DecreaseCmd = inverse_condition and not propotional_condition
            else:
                print("lower limit",item.lowerlimit)
                print("process value",item.processvalue)
                item.DecreaseCmd = (not propotional_condition) and (item.lowerlimit < item.processvalue)




class rampprocess:

    def __init__(self,alldevices,filename):
        self.subject = Observable()
        self.observer = AreaObserver(self.subject)
        self.alldevices = alldevices
        self.client = Communication()
        self.sta_con_plc = self.client.opc_client_connect(filename)
        self.observer = AreaObserver(self.subject)
        self.readgeneral = ReadGeneral(self.sta_con_plc)


    def process(self):
        for area, devices in readkeyandvalues(self.alldevices):
            areavalue = self.readgeneral.readsymbolvalue(area, 'S7WLBit', 'PA')

            if areavalue == 1:

                self.observer.notify(devices, self.readgeneral)


def readkeyandvalues(alldevice):
    rampdictionary = alldevice.allrampobjects.dictionary
    areas = list(rampdictionary.keys())

    n = 0
    while n < len(areas):
        area = areas[n]
        devices = rampdictionary[area]
        yield area, devices
        n = n + 1









