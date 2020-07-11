from logger import *
from event_V2 import *
from time import sleep
import logging
import threading
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import  general
setup_logging_to_file("dummybar.log")
logger = logging.getLogger("main.log")
__all__ = ['Fn_DummyBar']


class Fn_DummyBar(Eventmanager):

    def __init__(self, com, df, idxNo,filename):
        print('the dummybarwas here')
        self._idxNo = idxNo
        self.gen = com
        self.df = df
        self._currentpos = 0
        self.filename = filename
        self.devicename = df.iloc[self._idxNo, 0]
        self.setup()
        self.initilizedigitalinput()
        self.mylock = threading.Lock()
        super().__init__(lambda: self.dummybarprocess())
        print('herehrehre')

    def setup(self):

        try:

            for item, col in self.readalltags():

                if col == 3:
                    self.area = str(item)


                if col == 4:
                    self.presetvalue = int(item)

                if col == 5:
                    self.tolerance = int(item)

                if col == 6:
                    self.currentpos = str(item)

                if col == 7:
                    self.limitswitch = str(item)






        except Exception as e:
            level = logging.ERROR
            messege = "FN_DUMMYBAR" + self.devicename + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)

    def initilizedigitalinput(self):


        pass

    def dummybarprocess(self):
        print('hello the process of summybar started')

        try:

            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)

            if len(self.currentpos) > 3:
                self.currentposvalue = readgeneral.readDBvalue(self.currentpos,'S7WLWord')
                print(self.currentposvalue)
                self.postsetvalue =  self.presetvalue +  self.tolerance

            if self.currentposvalue > self.presetvalue and self.currentposvalue < self.postsetvalue :
                print("1")

                writegeneral.writesymbolvalue(self.limitswitch, 1,'S7WLBit')

                level2 = logging.WARNING
                messege2 = self.devicename + ":" + self.limitswitch + " value is 1"
                logger.log(level2, messege2)

            if self.currentposvalue < self.presetvalue or self.currentposvalue > self.postsetvalue :

                writegeneral.writesymbolvalue(self.limitswitch, 0,'S7WLBit')

            sta_con_plc.disconnect()



        except Exception as e:
            log_exception(e)
            level = logging.INFO
            messege = self.devicename + ":" + " Exception rasied(process): " + str(e.args) + str(e)
            logger.log(level, messege)

    def __getstate__(self):
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        del state['mylock']
        return state

    # def __setstate__(self, state):
    #     # Restore instance attributes.
    #     self.__dict__.update(state)

    @property
    def CurrentPos(self):
        return self._currentpos

    @CurrentPos.setter
    def CurrentPos(self, value):
        print("on command value",value)
        # print(self._currentpos)
        if value != self._currentpos:
            super().fire()
            self._currentpos = value

    @property
    def areaname(self):
        return self.area

    def readalltags(self):
        n = 3
        row, col = self.df.shape
        while n < col:
            data = self.df.iloc[self._idxNo, n]
            yield data, n
            n = n + 1