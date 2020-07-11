
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
        print("initilization complete")


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

                if col == 9:
                    self.cmdtag1 = str(item)

                if col == 10:
                    self.cmdtag2 = str(item)

                if col == 11:
                    self.cmdtag3 = str(item)

                if col == 12:
                    self.cmdtag4 = str(item)


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

            if(len(self.cmdtag1) > 3):
                self.cmdtag1value = readgeneral.readsymbolvalue(self.cmdtag1,'S7WLBit','PA')
            else:
                self.cmdtag1value = 1

            if (len(self.cmdtag2) > 3):
                self.cmdtag2value = readgeneral.readsymbolvalue(self.cmdtag2,'S7WLBit','PA')
            else:
                self.cmdtag2value = 1

            if (len(self.cmdtag3) > 3):
                self.cmdtag3value = readgeneral.readsymbolvalue(self.cmdtag3,'S7WLBit','PA')
            else:
                self.cmdtag3value = 1

            if (len(self.cmdtag4) > 3):
                self.cmdtag4value = readgeneral.readsymbolvalue(self.cmdtag4,'S7WLBit','PA')
            else:
                self.cmdtag4value = 1

            writegeneral.writesymbolvalue(self.outputtag, 0 , 'S7WLWord')

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

                        if (self.cmdtag1value and self.cmdtag2value and self.cmdtag3value and self.cmdtag4value):

                            if self.selval==1 and self.val > self.lowerlimit and self.val < self.highlimit :

                                a = abs(self.val - 0.005)
                                b = abs(self.val + 0.005)
                                self.targetvalue = random.uniform(a, b)
                                self.outrawvalue = self.scaling(self.targetvalue, self.highlimit, self.lowerlimit)
                                writegeneral.writesymbolvalue(self.outputtag, self.outrawvalue,'S7WLWord')


                            if not self.selval and  self.val > self.lowerlimit and self.val < self.highlimit and  self.val != 0 :
                                highband = self.highlimit - self.val
                                lowerband = self.val - self.lowerlimit
                                self.targetvalue = random.uniform(highband, lowerband)
                                self.outrawvalue = self.scaling(self.targetvalue, self.highlimit, self.lowerlimit)
                                writegeneral.writesymbolvalue(self.outputtag, self.outrawvalue,'S7WLWord')

                            if self.val == 0 and self.selval==1 :
                                writegeneral.writesymbolvalue(self.outputtag, 0, 'S7WLWord')

                            sta_con_plc.disconnect()

                            print('the value of analog is ',self.outrawvalue)


                            level1 = logging.WARNING
                            messege1 = self.devicename + ":" + self.outputtag + " value is " + str(self.outrawvalue)
                            logger.log(level1, messege1)

                    except Exception as e:
                        level = logging.ERROR
                        print(e.args)
                        messege = "Analog" + self.devicename + " Error messege(process)" + str(e.args)
                        logger.log(level, messege)
                        log_exception(e)
                        print(messege)


    def scaling(self, val, highlimit, lowlimit):
        rawvalue = int((val * 27648) / (highlimit - lowlimit))
        return rawvalue

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




