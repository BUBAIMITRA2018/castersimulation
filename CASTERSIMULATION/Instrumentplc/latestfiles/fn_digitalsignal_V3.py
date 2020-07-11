from logger import *
from event_V2 import *
from time import sleep
import logging
import threading
from event_V2 import *
logger = logging.getLogger("main.log")
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
__all__ = ['Fn_digitalsignal']


class Fn_digitalsignal(Eventmanager):

    def __init__(self, com, df, idxNo, filename):
        self._idxNo = idxNo
        self.gen = com
        self.df = df
        self.filename = filename

        self.cond1_val = False
        self.cond2_val = False
        self.cond3_val = False
        self.cond4_val = False


        self.devicename = df.iloc[self._idxNo, 0]
        self.setup()
        self.initilizedigitalinput()
        super().__init__(lambda: self.digitalprocess())

    def setup(self):

        try:
            for tag, col in self.readalltags():

                if col == 3:
                    self.area = str(tag)

                if col == 4:
                    self.OutDigital = str(tag)

                if col == 5:
                    self.cond1 = str(tag)

                if col == 6:
                    self.cond2 = str(tag)

                if col == 7:
                    self.cond3 = str(tag)

                if col == 8:
                    self.cond4 = str(tag)


        except Exception as e:
            level = logging.ERROR
            messege = "FN_DIGITASLSIGNAL" + self.devicename + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)

    def initilizedigitalinput(self):
        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)

            writegeneral.writesymbolvalue(self.OutDigital, 0 , 'S7WLBit')

            sta_con_plc.disconnect()
        except Exception as e:
            level = logging.ERROR
            messege = "Fn_Digitalsignal" + self.devicename + " Error messege(initilization)" + str(e.args)
            logger.log(level, messege)

    def digitalprocess(self):

        client = Communication()
        sta_con_plc = client.opc_client_connect(self.filename)
        readgeneral = ReadGeneral(sta_con_plc)
        writegeneral = WriteGeneral(sta_con_plc)

        cond1_val = readgeneral.readsymbolvalue(self.cond1,'S7WLBit','PE')
        cond2_val = readgeneral.readsymbolvalue(self.cond2, 'S7WLBit', 'PE')
        cond3_val = readgeneral.readsymbolvalue(self.cond3, 'S7WLBit', 'PE')
        cond4_val = readgeneral.readsymbolvalue(self.cond4, 'S7WLBit', 'PE')

        if cond1_val and cond2_val and cond3_val and cond4_val:
            writegeneral.writesymbolvalue(self.OutDigital, 1, 'S7WLBit')
        else:
            pass

    @property
    def Cond1Val (self):
        return self.cond1_val

    @Cond1Val.setter
    def Cond1Val(self, value):
        if value != self.cond1_val:
            super().fire()
            self.cond1_val = value

    @property
    def Cond2Val(self):
        return self.cond2_val

    @Cond2Val.setter
    def Cond2Val(self, value):
        if value != self.cond2_val:
            super().fire()
            self.cond2_val = value

    @property
    def Cond3Val(self):
        return self.cond3_val

    @Cond3Val.setter
    def Cond3Val(self, value):
        if value != self.cond3_val:
            super().fire()
            self.cond3_val = value

    @property
    def Cond4Val(self):
        return self.cond4_val

    @Cond4Val.setter
    def Cond4Val(self, value):
        if value != self.cond4_val:
            super().fire()
            self.cond4_val = value

    @property
    def areaname(self):
        return self.area



    def readalltags(self):
        n = 3
        row, col = self.df.shape
        print(col)
        while n < col:
            data = self.df.iloc[self._idxNo, n]
            yield data, n
            n = n + 1

