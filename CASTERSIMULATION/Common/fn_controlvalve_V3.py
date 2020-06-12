
from event_V2 import *

from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *

__all__ = ['Fn_ControlValves']

class Fn_ControlValves(Eventmanager):
    def __init__(self,com,df,idxNo,filename ):
        self._idxNo =idxNo
        self.devicename = df.iloc[self._idxNo, 0]
        self.filename = filename
        self.com = com
        self.df = df
        self._sp = 0
        self.setup()
        self.mylock = threading.Lock()
        self.initilizedigitalinput()
        super().__init__(lambda: self.controlvalveprocess())


    def setup(self):
        try:
            self.area = self.df.iloc[self._idxNo,3]

            self.sp = str(self.df.iloc[self._idxNo, 4])

            self.pv = str(self.df.iloc[self._idxNo, 5])

            self.delaytime = self.df.iloc[self._idxNo, 6]

            self.highpvvalue = int (self.df.iloc[self._idxNo, 7])

            self.lowpvvalue = int(self.df.iloc[self._idxNo, 8])


        except Exception as e:

            log_exception(e)

    def initilizedigitalinput(self):
      pass

    def controlvalveprocess(self):
        client = Communication()
        sta_con_plc = client.opc_client_connect(self.filename)
        readgeneral = ReadGeneral(sta_con_plc)
        writegeneral = WriteGeneral(sta_con_plc)

        try:
            if len(self.sp) > 0 :


                
                self.currentvalue = readgeneral.readsymbolvalue(self.pv,'S7WLWord','PE')
                self.spvalue = readgeneral.readsymbolvalue(self.sp, 'S7WLWord', 'PA')

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

                readgeneral.readsymbolvalue(self.pv,'S7WLWord','PE')

            writegeneral.writesymbolvalue(self.pv, self.currentvalue,'S7WLWord')
            sta_con_plc.disconnect()


        except Exception as e:
            log_exception(e)
            level = logging.ERROR
            messege = 'Event:' + "ControlValve" + str(e.args)
            logger.log(level, messege)





    def scalingconvtoraw(self, val, highlimit, lowlimit):
        rawvalue = int((val * 1) / (highlimit - lowlimit))
        # print(rawvalue)
        return rawvalue

    @property
    def processval(self):
        pv = float((self.currentvalue/27648)*(self.highpvvalue - self.lowpvvalue))
        print(pv)
        return  pv



    @property
    def setpoint(self):
        return self._sp

    @setpoint.setter
    def setpoint(self, value):

        if value != self._sp:
            print("setpointvalue is", value)
            print("current value is", self._sp)
            super().fire()
            self._sp = value

    @property
    def areaname(self):
        return self.area


    def readalltags(self):
        n = 3
        row, col = self.df.shape
        print(col)
        while n < col:
            data = self.df.iloc[self._idxNo, n]
            yield data,n
            n = n + 1
