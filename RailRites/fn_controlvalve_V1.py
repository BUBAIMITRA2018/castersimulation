from logger import *
import logging

__all__ = ['Fn_ControlValves']

class Fn_ControlValves:


    def __init__(self,com,df,idxNo,logger):
        self._idxNo =idxNo
        self.gen = com
        self.devicename = df.iloc[self._idxNo, 0]
        self.logger = logger
        self.df = df
        self.setup()
        self.controlvalveinitilization()


    def setup(self):
        try:
            self.sp = self.df.iloc[self._idxNo, 3]
            self.pv = str(self.df.iloc[self._idxNo, 4])
            self.gen.writegeneral.writenodevalue(self.pv, 0)
            self.delaytime = self.df.iloc[self._idxNo, 5]
            self.highpvvalue = self.df.iloc[self._idxNo,6]
            self.lowpvvalue = self.df.iloc[self._idxNo, 7]


        except Exception as e:
            print("exception raise", e.args)
            log_exception(e)

    def controlvalveinitilization(self):
        pass

    def process(self):

        try:

            rawspvalue = self.gen.readgeneral.readnodevalue(self.sp)
            self.currentvalue = self.gen.readgeneral.readtagvalue(self.pv)
            if rawspvalue > 0.0:
                  if rawspvalue > self.currentvalue:
                         diff = rawspvalue - self.currentvalue
                         self.currentvalue = self.currentvalue + (diff / self.delaytime)

                  if rawspvalue < self.currentvalue:
                        diff = self.currentvalue - rawspvalue
                        self.currentvalue = self.currentvalue - (diff / self.delaytime)
            else:
                  self.currentvalue = self.gen.readgeneral.readnodevalue(self.pv)

            self.gen.writegeneral.writenodevalue(self.pv, self.currentvalue)

            level1 = logging.WARNING
            messege1 = self.devicename + ":" + self.pv + " value is " + str(self.currentvalue)
            self.logger.log(level1, messege1)

        except Exception as e:
            log_exception(e)

    def scalingconvtoraw(self, val, highlimit, lowlimit):
        rawvalue = int((val * 27648) / (highlimit - lowlimit))

        return rawvalue

    @property
    def processval(self):
        pv = float((self.currentvalue/27648)*(self.highpvvalue - self.lowpvvalue))
        return  pv

    @property
    def setpoint(self):
        return self.sp


    def readalltags(self):
        n = 3
        row, col = self.df.shape
        print(col)
        while n < col:
            data = self.df.iloc[self._idxNo, n]
            yield data,n
            n = n + 1
