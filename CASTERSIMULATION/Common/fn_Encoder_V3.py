from logger import *
from event_V2 import *
from time import sleep
import logging
import threading

__all__ = ['Fn_Encoder']

logger = logging.getLogger("main.log")

class Fn_Encoder(Eventmanager):

    def __init__(self,com,df,idxNo):
        self._idxNo =idxNo
        self.gen = com
        self.df = df
        self.devicename = df.iloc[self._idxNo,0]
        self.setup()
        self._encodervalue = 0
        self._fastcountvalue = 0
        self._drivespvalue = 0
        self._breakopencmdvalue = 0
        self.initilizedigitalinput()
        self.mylock = threading.Lock()
        super().__init__(lambda: self.encoderprocess())

    def setup(self):
        try:
            for tag,col in self.readalltags():

                if col == 3:
                    self.area = str(tag)

                if col==4:
                    self.drivesptag = str(tag)

                if col == 5:
                    self.breakopentag = str(tag)

                if col == 6:
                    self.fastcounttag = int(tag)

                if col == 7:
                    self.encoderoutputtag = str(tag)
        except Exception as e:
            level = logging.ERROR
            messege = "FN_Encoder" + self.devicename + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)


    def initilizedigitalinput(self):
        try:
           self._encodervalue = 0
        except Exception as e :
            level = logging.ERROR
            messege = "FN_Encoder" + self.devicename + " Error messege(initilization)" + str(e.args)
            logger.log(level, messege)

    def encoderprocess(self):
        try:
            self.drivespvalue = self.gen.readgeneral.readtagvalue(self.drivesptag)
            self._fastcountvalue = self.fastcounttag
            if(self.drivespvalue>45000):
                self._encodervalue = self._encodervalue + self._fastcountvalue
            if(self.drivespvalue<45000):
                self._encodervalue = self._encodervalue  - self._fastcountvalue
            self.gen.writegeneral.writenodevalue(self.encoderoutputtag, self._encodervalue)
        except Exception as e:
            log_exception(e)
            level = logging.INFO
            messege = self.devicename + ":" + " Exception rasied(process): " + str(e.args) + str(e)
            logger.log(level, messege)


    @property
    def BreakOpenCmd(self):
        return self._breakopencmdvalue

    @BreakOpenCmd.setter
    def BreakOpenCmd(self,value):
        if value != self._breakopencmdvalue:
            super().fire()
            self._breakopencmdvalue = value

    @property
    def areaname(self):
        return self.area

    def readalltags(self):
        n = 3
        row, col = self.df.shape
        print(col)
        while n <col:
            data = self.df.iloc[self._idxNo, n]
            yield data,n
            n = n + 1

