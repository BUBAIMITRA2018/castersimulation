from logger import *
from event_V2 import *
from time import sleep
import logging
import threading
logger = logging.getLogger("main.log")
__all__ = ['Fn_Motor1D']


class Fn_Motor1D(Eventmanager):

    def __init__(self, com, df, idxNo, ):
        self._idxNo = idxNo
        self.gen = com
        self.df = df
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

            self._oncmdvalue = self.gen.readgeneral.readtagvalue(self.oncmdtag)

            self._runFBvalue = self.gen.readgeneral.readtagvalue(self.runingFBtag)

            if len(self.healthyFBtag) > 3:
                self.gen.writegeneral.writenodevalue(self.healthyFBtag, 1)
                level = logging.INFO
                messege = self.devicename + ":" + self.healthyFBtag + " is trigger by 1"
                logger.log(level, messege)

            else:
                pass

            if len(self.readyFBtag) > 3:
                self.gen.writegeneral.writenodevalue(self.readyFBtag, 1)
                level = logging.INFO
                messege = self.devicename + ":" + self.readyFBtag + " is trigger by 1"
                logger.log(level, messege)
            else:
                pass

            if len(self.mccbonFeedBacktag) > 3:
                self.gen.writegeneral.writenodevalue(self.mccbonFeedBacktag, 1)
                level = logging.INFO
                messege = self.devicename + ":" + self.mccbonFeedBacktag + " is trigger by 1"
                logger.log(level, messege)
            else:
                pass

            if len(self.overloadFeedBacktag) > 3:
                self.gen.writegeneral.writenodevalue(self.overloadFeedBacktag, 0)
                level = logging.INFO
                messege = self.devicename + ":" + self.overloadFeedBacktag + " is trigger by 0"
                logger.log(level, messege)
            else:
                pass

            if len(self.faultFBtag) > 3:
                self.gen.writegeneral.writenodevalue(self.faultFBtag, 1)
                level = logging.INFO
                messege = self.devicename + ":" + self.faultFBtag + " is trigger by 1"
                logger.log(level, messege)
            else:
                pass

            if len(self.plcreleasetag) > 3:
                self.gen.writegeneral.writenodevalue(self.plcreleasetag, 0)
                level = logging.INFO
                messege = self.devicename + ":" + self.plcreleasetag + " is trigger by 0"
                logger.log(level, messege)
            else:
                pass

        except Exception as e:
            level = logging.ERROR
            messege = "FN_MOTOR1D" + self.devicename + " Error messege(initilization)" + str(e.args)
            logger.log(level, messege)

    def motorprocess(self):

        try:
            if len(self.offcmdtag) > 3:
                self.offcmdvalue = self.gen.readgeneral.readtagvalue(self.offcmdtag)

            oncommandvalue = self.gen.readgeneral.readtagvalue(self.oncmdtag)
            runfbvalue = self.gen.readgeneral.readtagvalue(self.runingFBtag)
            if oncommandvalue == True and runfbvalue == False:
                # sleep(self.delaytimetag)
                print('run')

                self.gen.writegeneral.writenodevalue(self.runingFBtag, 1)
                self.runFB = 1

                level2 = logging.WARNING
                messege2 = self.devicename + ":" + self.oncmdtag + " value is 1"
                logger.log(level2, messege2)

                level1 = logging.INFO
                messege1 = self.devicename + ":" + self.runingFBtag + " is trigger by 1"
                logger.log(level1, messege1)

            if runfbvalue == True and oncommandvalue == False:
                print('stop')
                self.gen.writegeneral.writenodevalue(self.runingFBtag, 0)
                self.runFB = 0

            if runfbvalue == True and self.offcmdvalue == True and len(self.offcmdtag) > 3:
                self.gen.writegeneral.writenodevalue(self.runingFBtag, 0)
                self.runFB = 0


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
    def OnCmd(self):
        return self._oncmdvalue

    @OnCmd.setter
    def OnCmd(self, value):
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
        print(col)
        while n < col:
            data = self.df.iloc[self._idxNo, n]
            yield data, n
            n = n + 1
