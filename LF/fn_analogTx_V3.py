
from event_V2 import *

from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import threading
import random
logger = logging.getLogger("main.log")

__all__ = ['Fn_AnalogTx']

class Fn_AnalogTx(Eventmanager):

    def __init__(self,com,df,idxNo,filename):

        self.filename=filename
        self._idxNo =idxNo
        self.gen = com
        self.devicename = df.iloc[self._idxNo, 0]
        self.df = df
        self.outrawvalue = 0
        self.setup()
        self.analoginitialization()
        super().__init__(lambda: self.analogprocess())



    def setup(self):
        try:


            for item, col in self.readalltags():

                if col == 3:
                    self.area = str(item)

                if col == 4:
                    self.highlimit = float(item)


                if col == 5:
                    self.lowerlimit = float(item)


                if col == 6:
                    self.val = float(item)


                if col == 7:
                    self.selval =int(item)


                if col == 8:
                    self.outputtag = str(item)




        except Exception as e:
            log_exception(e)
            level = logging.ERROR
            messege = 'Event:' + "callallanalog" + str(e.args)
            logger.log(level, messege)

    def analoginitialization(self):
        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)

            if self.selval == 1 and self.val > self.lowerlimit and self.val < self.highlimit:
                a = abs(self.val - 0.005)
                b = abs(self.val + 0.005)
                self.targetvalue = random.uniform(a, b)
                self.outrawvalue = self.unscaling(self.targetvalue, 27648, self.highlimit, self.lowerlimit, 0)
                writegeneral.writesymbolvalue(self.outputtag, self.outrawvalue, 'S7WLWord')

            if not self.selval and self.val > self.lowerlimit and self.val < self.highlimit and self.val != 0:
                highband = self.highlimit - self.val
                lowerband = self.val - self.lowerlimit
                self.targetvalue = random.uniform(highband, lowerband)
                self.outrawvalue = self.unscaling(self.targetvalue, 27648, self.highlimit, self.lowerlimit, 0)
                writegeneral.writesymbolvalue(self.outputtag, self.outrawvalue, 'S7WLWord')

            if self.val == 0 and self.selval == 1:
                writegeneral.writesymbolvalue(self.outputtag, 0, 'S7WLWord')

            sta_con_plc.disconnect()


        except Exception as e:
            print(e.args)
            log_exception(e)
            level = logging.ERROR
            messege = self.devicename + "FN_analog(initilization)" + str(e.args)
            logger.log(level, messege)

            print(messege)



    def analogprocess(self):
                    try:
                        client = Communication()
                        sta_con_plc = client.opc_client_connect(self.filename)
                        readgeneral = ReadGeneral(sta_con_plc)
                        writegeneral = WriteGeneral(sta_con_plc)

                        pass


                        sta_con_plc.disconnect()



                    except Exception as e:
                        level = logging.ERROR
                        messege = "Analog" + self.devicename + " Error messege(process)" + str(e.args)
                        logger.log(level, messege)
                        log_exception(e)
                        print(messege)


    def scaling(self, val, highlimit, lowlimit):
        rawvalue = int((val * 27648) / (highlimit - lowlimit))
        return rawvalue

    def unscaling(self, val, engineeringvaluerange, highlimit, lowlimit, engineeringlowlimit):
        processvaluerange = highlimit - lowlimit
        enggunit = (engineeringvaluerange / processvaluerange) * (val - lowlimit) + engineeringlowlimit
        return enggunit

    @property
    def areaname(self):
        return self.area


    def readalltags(self):
        n = 3
        row, col = self.df.shape
        while n < col:
            data = self.df.iloc[self._idxNo, n]
            yield data,n
            n = n + 1




