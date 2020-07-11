from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
logger = logging.getLogger("main.log")

__all__ = ['Fn_DummyBar']


class Fn_DummyBar():

    def __init__(self, filename):
        self.filename = filename
        self.setup()
        self.initilizedigitalinput()


    def setup(self):

        try:
            self.presetvalue_1 = float()
            self.tolerance_1 = float()
            self.presetvalue_2 = float()
            self.tolerance_2 = float()
            self.presetvalue_3 = float()
            self.tolerance_3 = float()
            self.currentpos = str()
            self.limitswitch_1 = str()
            self.limitswitch_2 = str()
            self.limitswitch_3 = str()






        except Exception as e:
            level = logging.ERROR
            messege = "FN_DUMMYBAR"+ " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)

    def initilizedigitalinput(self):

        pass

    def dummybarprocess(self):


        try:

            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)
            self.currentposvalue = readgeneral.readDBvalue(self.currentpos, 'S7WLReal')

            self.upperlimit_1 = self.presetvalue_1 + self.tolerance_1
            self.lowerlimit_1 = self.presetvalue_1 - self.tolerance_1

            self.upperlimit_2 = self.presetvalue_2 + self.tolerance_2
            self.lowerlimit_2 = self.presetvalue_2 - self.tolerance_2

            self.upperlimit_3 = self.presetvalue_3 + self.tolerance_3
            self.lowerlimit_3 = self.presetvalue_3 - self.tolerance_3


            if self.currentposvalue >= self.lowerlimit_1 and self.currentposvalue < self.upperlimit_1 :
                    writegeneral.writesymbolvalue(self.limitswitch_1, 1, 'S7WLBit')
                    writegeneral.writesymbolvalue(self.limitswitch_2, 0, 'S7WLBit')
                    writegeneral.writesymbolvalue(self.limitswitch_3, 0, 'S7WLBit')

            if self.currentposvalue >= self.lowerlimit_2 and self.currentposvalue < self.upperlimit_2:
                writegeneral.writesymbolvalue(self.limitswitch_1, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.limitswitch_2, 1, 'S7WLBit')
                writegeneral.writesymbolvalue(self.limitswitch_3, 0, 'S7WLBit')

            if self.currentposvalue >= self.lowerlimit_3 and self.currentposvalue < self.upperlimit_3:
                writegeneral.writesymbolvalue(self.limitswitch_1, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.limitswitch_2, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.limitswitch_3, 1, 'S7WLBit')


            sta_con_plc.disconnect()


        except Exception as e:
            log_exception(e)
            level = logging.INFO
            messege = "FN_DUMMYBAR" + ":" + " Exception rasied(process): " + str(e.args) + str(e)
            logger.log(level, messege)

