from observal import *
from clientcomm_v1 import *
from readgeneral_v2 import *
import  threading
logger = logging.getLogger("main.log")


class AreaObserver:
    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self,  *args, **kwargs):
        for item in args[0]:
            inverse_condition = False
            propotional_condition = False

            cond1 = (len(item.cmdtag5)> 3)
            cond2 = (len(item.cmdtag1) >= 3) and (args[1].readsymbolvalue(item.cmdtag1, 'S7WLBit', 'PE'))

            if cond1:
                inverse_condition = (args[1].readsymbolvalue(item.cmdtag5, 'S7WLBit', 'PE')) \
                                    or (args[1].readsymbolvalue(item.cmdtag6, 'S7WLBit', 'PE')) \
                                    or (args[1].readsymbolvalue(item.cmdtag7, 'S7WLBit', 'PE')) \
                                    or (args[1].readsymbolvalue(item.cmdtag8, 'S7WLBit', 'PE'))

            if cond2:
                propotional_condition = (args[1].readsymbolvalue(item.cmdtag1, 'S7WLBit', 'PE'))\
                                        and (args[1].readsymbolvalue(item.cmdtag2, 'S7WLBit', 'PE'))\
                                        and (args[1].readsymbolvalue(item.cmdtag3, 'S7WLBit', 'PE')) \
                                        and (args[1].readsymbolvalue(item.cmdtag4, 'S7WLBit', 'PE'))



            if len(item.cmdtag1) >= 3:
                item.IncreaseCmd = propotional_condition and not inverse_condition


            if len(item.cmdtag5) > 3:
                item.DecreaseCmd = inverse_condition and not propotional_condition
            else:
                item.DecreaseCmd = (not propotional_condition)




class rampprocess:

    def __init__(self,alldevices,filename):
        self.subject = Observable()
        self.observer = AreaObserver(self.subject)
        self.alldevices = alldevices
        self.filename = filename
        self.client = Communication()
        self.sta_con_plc = self.client.opc_client_connect(filename)
        self.observer = AreaObserver(self.subject)
        self.readgeneral = ReadGeneral(self.sta_con_plc)


    def callobserver(self,area,devices,filename):
        while True:
            try:
                client = Communication()
                sta_con_plc = self.client.opc_client_connect(filename)
                readgeneral = ReadGeneral(self.sta_con_plc)
                areavalue =   readgeneral.readsymbolvalue(area, 'S7WLBit', 'PA')
                if areavalue == 1:
                    self.observer.notify(devices, readgeneral)

                sta_con_plc.disconnect()



            except Exception as e:
                level = logging.ERROR
                messege = "Ramp" + " Error messege(Obsrver process)" + str(e.args)
                # logger.log(level, messege)





    def process(self):
        for area, devices in readkeyandvalues(self.alldevices):
            threading.Thread(target=self.callobserver, args= (area,devices,self.filename)).start()


def readkeyandvalues(alldevice):
    rampdictionary = alldevice.allrampobjects.dictionary
    areas = list(rampdictionary.keys())

    n = 0
    while n < len(areas):
        area = areas[n]
        devices = rampdictionary[area]
        yield area, devices
        n = n + 1









