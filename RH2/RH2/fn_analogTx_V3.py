from event_V2 import *
from clientcomm_v1 import *
import random
from readgeneral_v2 import *
from  writegeneral_v2 import *
import gc

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
        self.currentpv = 0

        self.cmdtag1 = ""
        self.cmdtag2 = ""
        self.cmdtag3 = ""
        self.cmdtag3 = ""
        self.cmdtag4 = ""
        self.cmdtag5 = ""
        self.cmdtag6 = ""
        self.cmdtag7 = ""
        self.cmdtag8 = ""
        self.positiverate = 0.0
        self.postivepluse = False
        self.negativerate = 0.0
        self.negativepluse = False


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
            level = logging.ERROR
            messege = 'Event:' + "callallanalog" + str(e.args)
            logger.log(level, messege)

    def analoginitialization(self):
        client = Communication()
        sta_con_plc = client.opc_client_connect(self.filename)
        writegeneral = WriteGeneral(sta_con_plc)
        readgeneral = ReadGeneral(sta_con_plc)

        if self.selval == 1 and self.val > self.lowerlimit and self.val < self.highlimit:
            a = abs(self.val - 0.005)
            b = abs(self.val + 0.005)
            self.targetvalue = random.uniform(a, b)
            self.outrawvalue = self.scaling(self.targetvalue, self.highlimit, self.lowerlimit)
            writegeneral.writesymbolvalue(self.outputtag, 'analog', self.outrawvalue)

        if not self.selval and self.val > self.lowerlimit and self.val < self.highlimit and self.val != 0:
            highband = self.highlimit - self.val
            lowerband = self.val - self.lowerlimit
            self.targetvalue = random.uniform(highband, lowerband)
            self.outrawvalue = self.scaling(self.targetvalue, self.highlimit, self.lowerlimit)
            writegeneral.writesymbolvalue(self.outputtag, 'analog', self.outrawvalue)

        if self.val == 0 and self.selval == 1:
            writegeneral.writesymbolvalue(self.outputtag, 'analog', 0)

        sta_con_plc.close()
        gc.collect()






    def analogprocess(self):

                    try:


                        client = Communication()
                        sta_con_plc = client.opc_client_connect(self.filename)
                        writegeneral = WriteGeneral(sta_con_plc)
                        readgeneral = ReadGeneral(sta_con_plc)

                        if self.selval == 1 and self.val > self.lowerlimit and self.val < self.highlimit:
                            a = abs(self.val - 0.005)
                            b = abs(self.val + 0.005)
                            self.targetvalue = random.uniform(a, b)
                            self.outrawvalue = self.unscaling(self.targetvalue,10000,self.highlimit,self.lowerlimit,0)
                            writegeneral.writesymbolvalue(self.outputtag, 'analog', self.outrawvalue)

                        if not self.selval and self.val > self.lowerlimit and self.val < self.highlimit and self.val != 0:
                            highband = self.highlimit - self.val
                            lowerband = self.val - self.lowerlimit
                            self.targetvalue = random.uniform(highband, lowerband)
                            self.outrawvalue = self.unscaling(self.targetvalue, 10000, self.highlimit, self.lowerlimit,
                                                              0)
                            writegeneral.writesymbolvalue(self.outputtag, 'analog', self.outrawvalue)

                        if self.val == 0 and self.selval == 1:
                            writegeneral.writesymbolvalue(self.outputtag, 'analog', 0)

                        sta_con_plc.close()


                    except Exception as e:
                        level = logging.ERROR
                        print(e.args)
                        messege = "Analog" + self.devicename + " Error messege(process)" + str(e.args)
                        logger.log(level, messege)



    def scaling(self, val, highlimit, lowlimit):
        rawvalue = int((val * 10000) / (highlimit - lowlimit))
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




