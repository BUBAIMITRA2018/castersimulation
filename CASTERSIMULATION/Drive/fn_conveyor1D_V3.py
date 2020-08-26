from logger import *
from event_V2 import *
from time import sleep
import logging
import threading
logger = logging.getLogger("main.log")

__all__ = ['Fn_Conveyor1D']




class Fn_Conveyor1D(Eventmanager):

    def __init__(self,com,df,idxNo):
        self._idxNo =idxNo
        self.gen = com
        self.df = df
        self.devicename = df.iloc[self._idxNo, 0]
        self._oncmdvalue = False
        self._runFBvalue = False
        self.setup()
        self.initilizedigitalinput()
        super().__init__(lambda: self.conveyorprocess())


    def setup(self):
        try:

            for tag,col in self.readalltags():

                if col==3:
                    self.areatag = str(tag)

                if col==4:
                    self.cmdtag = str(tag)

                if col == 5:
                    self.remoteFBtag = str(tag)

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
                    self.faultFBtag =str(tag)


                if col == 12:
                    self.delaytimetag = str(tag)

                if col == 13:
                    self.pullchordlefttag = str( tag)

                if col == 14:
                    self.pullchordrighttag = str(tag)


        except Exception as e:
            level = logging.ERROR
            messege = "FN_Conveyor" + self.devicename + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)

    def initilizedigitalinput(self):
        try:
            if len(self.healthyFBtag) > 3:
                self.gen.writegeneral.writenodevalue(self.healthyFBtag, 1)
                level = logging.INFO
                messege = self.devicename + ":" + self.healthyFBtag + " is trigger by 1"
                logger.log(level, messege)

            if len(self.remoteFBtag) > 3:
                self.gen.writegeneral.writenodevalue(self.remoteFBtag, 1)
                level = logging.INFO
                messege = self.devicename + ":" + self.remoteFBtag + " is trigger by 1"
                logger.log(level, messege)


            if len(self.readyFBtag) > 3:
                self.gen.writegeneral.writenodevalue(self.readyFBtag, 1)
                level = logging.INFO
                messege = self.devicename + ":" + self.readyFBtag + " is trigger by 1"
                logger.log(level, messege)


            if len(self.mccbonFeedBacktag) > 3:
                self.gen.writegeneral.writenodevalue(self.mccbonFeedBacktag, 1)
                level = logging.INFO
                messege = self.devicename + ":" + self.mccbonFeedBacktag + " is trigger by 1"
                logger.log(level, messege)


            if len(self.overloadFeedBacktag) > 3:
                self.gen.writegeneral.writenodevalue(self.overloadFeedBacktag, 0)
                level = logging.INFO
                messege = self.devicename + ":" + self.overloadFeedBacktag + " is trigger by 1"
                logger.log(level, messege)


            if len(self.faultFBtag) > 3:
                self.gen.writegeneral.writenodevalue(self.faultFBtag, 0)
                level = logging.INFO
                messege = self.devicename + ":" + self.faultFBtag + " is trigger by 0"
                logger.log(level, messege)


            if len(self.pullchordlefttag) > 3:
                self.gen.writegeneral.writenodevalue(self.pullchordlefttag, 0)
                level = logging.INFO
                messege = self.devicename + ":" + self.pullchordlefttag + " is trigger by 0"
                logger.log(level, messege)


            if len(self.pullchordrighttag) > 3:
                self.gen.writegeneral.writenodevalue(self.pullchordrighttag, 0)
                level = logging.INFO
                messege = self.devicename + ":" + self.pullchordlefttag + " is trigger by 0"
                logger.log(level, messege)
            self.conveyorprocess()


        except Exception as e :
            log_exception(e)
            level = logging.ERROR
            messege = "FN_Conveyor" + self.devicename + " Error messege(initilization)" + str(e.args)
            logger.log(level, messege)


    def conveyorprocess(self):

        try:

            oncommandvalue = self.gen.readgeneral.readtagvalue(self.cmdtag)
            if oncommandvalue:
                self.gen.writegeneral.writenodevalue(self.runingFBtag, 1)
                level = logging.WARNING
                messege = self.devicename + ":" + self.runingFBtag + " is trigger by 1"
                logger.log(level, messege)
                self.runFB = 1
            else:
                self.gen.writegeneral.writenodevalue(self.runingFBtag, 0)
                self.runFB = 0

        except Exception as e:
            level = logging.ERROR
            messege = "FN_Conveyor" + self.devicename + " Error messege(process)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)

    @property
    def OnCmd(self):
        return self._oncmdvalue

    @OnCmd.setter
    def OnCmd(self, value):
        if value != self._oncmdvalue:
            super().fire()
            self._oncmdvalue = value

    @property
    def runFB(self):
        return self._runFBvalue

    @runFB.setter
    def runFB(self, value):
        self._runFBvalue = value

    @property
    def areaname(self):
        return self.areatag


    def readalltags(self):
        n = 3
        row, col = self.df.shape
        print(col)
        while n < col:
            data = self.df.iloc[self._idxNo, n]
            yield data,n
            n = n + 1






