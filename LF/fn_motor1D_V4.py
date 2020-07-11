from logger import *
from event_V2 import *
from time import sleep
import logging
import threading
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import  general
logger = logging.getLogger("main.log")
__all__ = ['Fn_Motor1D']


class Fn_Motor1D(Eventmanager):

    def __init__(self, com, df, idxNo,filename):
        self._idxNo = idxNo
        self.gen = com
        self.df = df
        self.filename = filename
        self.devicename = df.iloc[self._idxNo, 0]
        self.setup()
        self._offcmdvalue = False
        self._oncmdvalue = False
        self._runFBvalue = False
        self.initilizedigitalinput()
        self.mylock = threading.Lock()
        super().__init__(lambda: self.motorprocess())

    def setup(self):

        try:


            for tag, col in self.readalltags():

                if col == 3:
                    self.area = str(tag)


                if col == 4:
                    self.oncmdtag = str(tag)

                if col == 5:
                    self.offcmdtag = str(tag)

                if col == 6:
                    self.runingFBtag = str(tag)

                if col == 7:
                    self.healthyFBtag = str(tag)

                if col == 8:
                    self.readyFBtag = str(tag)

                if col == 9:
                    self.mccbonFeedBacktag = str(tag)

                if col == 10:
                    self.overloadFeedBacktag = str(tag)

                if col == 11:
                    self.faultFBtag = str(tag)

                if col == 12:
                    self.delaytimetag = tag

                if col == 13:
                    self.plcreleasetag = str(tag)




        except Exception as e:
            level = logging.ERROR
            messege = "FN_MOTOR1D" + self.devicename + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)

    def initilizedigitalinput(self):
        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral( sta_con_plc)

            self._oncmdvalue = False

            self._runFBvalue = readgeneral.readsymbolvalue(self.runingFBtag,'S7WLBit','PE')

            if len(self.healthyFBtag) >= 3:
                writegeneral.writesymbolvalue(self.healthyFBtag, 1,'S7WLBit')
                level = logging.INFO
                messege = self.devicename + ":" + self.healthyFBtag + " is trigger by 1"
                logger.log(level, messege)

            else:
                pass

            if len(self.readyFBtag) > 3:
                writegeneral.writesymbolvalue(self.readyFBtag, 1,'S7WLBit')
                level = logging.INFO
                messege = self.devicename + ":" + self.readyFBtag + " is trigger by 1"
                logger.log(level, messege)
            else:
                pass

            if len(self.mccbonFeedBacktag) > 3:
                writegeneral.writesymbolvalue(self.mccbonFeedBacktag, 1,'S7WLBit')
                level = logging.INFO
                messege = self.devicename + ":" + self.mccbonFeedBacktag + " is trigger by 1"
                logger.log(level, messege)
            else:
                pass

            if len(self.overloadFeedBacktag) > 3:
                writegeneral.writesymbolvalue(self.overloadFeedBacktag, 0,'S7WLBit')
                level = logging.INFO
                messege = self.devicename + ":" + self.overloadFeedBacktag + " is trigger by 0"
                logger.log(level, messege)
            else:
                pass

            if len(self.faultFBtag) > 3:
                writegeneral.writesymbolvalue(self.faultFBtag, 0,'S7WLBit')
                level = logging.INFO
                messege = self.devicename + ":" + self.faultFBtag + " is trigger by 0"
                logger.log(level, messege)
            else:
                pass

            if len(self.plcreleasetag) > 3:
                writegeneral.writesymbolvalue(self.plcreleasetag, 1,'S7WLBit')
                level = logging.INFO
                messege = self.devicename + ":" + self.plcreleasetag + " is trigger by 1"
                logger.log(level, messege)
            else:
                pass

            sta_con_plc.disconnect()

        except Exception as e:
            level = logging.ERROR
            messege = "FN_MOTOR1D" + self.devicename + " Error messege(initilization)" + str(e.args)
            logger.log(level, messege)

    def motorprocess(self):

        try:

            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)

            if len(self.offcmdtag) > 3:
                self.offcmdvalue = readgeneral.readsymbolvalue(self.offcmdtag,'S7WLBit','PA')

            oncommandvalue = readgeneral.readsymbolvalue(self.oncmdtag,'S7WLBit','PA')
            runfbvalue = readgeneral.readsymbolvalue(self.runingFBtag,'S7WLBit','PE')
            if oncommandvalue == True and runfbvalue == False:

                writegeneral.writesymbolvalue(self.runingFBtag, 1,'S7WLBit')
                self.runFB = 1

                level2 = logging.WARNING
                messege2 = self.devicename + ":" + self.oncmdtag + " value is 1"
                logger.log(level2, messege2)

                level1 = logging.INFO
                messege1 = self.devicename + ":" + self.runingFBtag + " is trigger by 1"
                logger.log(level1, messege1)

            if runfbvalue == True and oncommandvalue == False:

                writegeneral.writesymbolvalue(self.runingFBtag, 0,'S7WLBit')
                self.runFB = 0

            if len(self.offcmdtag) > 3:
                if runfbvalue == True and self.offcmdvalue == True and len(self.offcmdtag) > 3:
                    writegeneral.writesymbolvalue(self.runingFBtag, 0, 'S7WLBit')
                    self.runFB = 0

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

    @property
    def OnCmd(self):
        return self._oncmdvalue

    @OnCmd.setter
    def OnCmd(self, value):
        print("on command value",value)
        print(self._oncmdvalue)
        if value != self._oncmdvalue:
            super().fire()
            self._oncmdvalue = value

    @property
    def OffCmd(self):
        return self._offcmdvalue

    @OffCmd.setter
    def OffCmd(self, value):
        if value != self._offcmdvalue:
            super().fire()
            self._offcmdvalue = value

    @property
    def runFB(self):
        return self._runFBvalue

    @runFB.setter
    def runFB(self, value):
        self._runFBvalue = value

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
