from logger import *
from event_V2 import *
import threading

__all__ = ['Fn_ControlValves']

class Fn_ControlValves(Eventmanager):


    def __init__(self,com,df,idxNo):

        self._idxNo =idxNo
        self.gen = com
        self.df = df
        self.setup()
        self.mylock = threading.Lock()
        self.initilizedigitalinput()
        super().__init__(lambda: self.process())


    def setup(self):
        try:
            self.subarea = self.df.iloc[self._idxNo,3]

            self.sp = self.df.iloc[self._idxNo, 4]

            self.pv = str(self.df.iloc[self._idxNo, 5])

            self.delaytime = self.df.iloc[self._idxNo, 6]

            self.highpvvalue = self.df.iloc[self._idxNo, 7]

            self.lowpvvalue = self.df.iloc[self._idxNo, 8]


        except Exception as e:
            print("exception raise", e.args)
            log_exception(e)

    def initilizedigitalinput(self):

        pass

    def process(self):

        try:
            if len(self.sp) > 0 :
                self.currentvalue = self.gen.readgeneral.readsymbolvalue(self.pv,'S7WLWord','PE')
                self.spvalue = self.gen.readgeneral.readsymbolvalue(self.sp, 'S7WLWord', 'PA')

                rawspvalue = self.scalingconvtoraw(self.spvalue,self.highpvvalue,self.lowpvvalue)

                if rawspvalue > self.currentvalue:

                    diff = rawspvalue - self.currentvalue
                    count= .01*diff
                    self.currentvalue = self.currentvalue + count
                if rawspvalue < self.currentvalue:
                    diff = self.currentvalue-rawspvalue
                    count1=.01*diff
                    self.currentvalue = self.currentvalue - count1


            else:

                self.currentvalue = self.gen.readgeneral.readsymbolvalue(self.pv)

            self.gen.writegeneral.writesymbolvalue(self.pv, self.currentvalue,'S7WLWord')

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
