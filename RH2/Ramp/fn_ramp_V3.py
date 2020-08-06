from event_V3 import *
from clientcomm_v1 import *
import random
import time
from readgeneral_v2 import *
from  writegeneral_v2 import *
import gc

logger = logging.getLogger("main.log")

__all__ = ['Fn_Ramp']

class Fn_Ramp(Eventmanager):

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
        self._increasecmdvalue =  False
        self._decreasecmdvalue = False
        self.setup()
        self.initialization()
        super().__init__(lambda: self.callincreaserampprocess(),lambda : self.calldecreaserampprocess())




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

                    self.cmdtag1 = self.cmdtag1.split(".")
                    self.cmdtag1 = self.cmdtag1[0]


                if col == 10:
                    self.cmdtag2 = str(item)
                    self.cmdtag2 = self.cmdtag2.split(".")
                    self.cmdtag2 = self.cmdtag2[0]


                if col == 11:
                    self.cmdtag3 = str(item)

                    self.cmdtag3 = self.cmdtag3.split(".")
                    self.cmdtag3 = self.cmdtag3[0]

                if col == 12:
                    self.cmdtag4 =str(item)
                    self.cmdtag4 = self.cmdtag4.split(".")
                    self.cmdtag4 = self.cmdtag4[0]



                if col == 13:
                    self.cmdtag5 = str((item))
                    self.cmdtag5 = self.cmdtag5.split(".")
                    self.cmdtag5 = self.cmdtag5[0]


                if col == 14:
                    self.cmdtag6 =str(item)

                    self.cmdtag6 = self.cmdtag6.split(".")
                    self.cmdtag6 = self.cmdtag6[0]

                if col == 15:
                    self.cmdtag7 = str(item)
                    self.cmdtag7 = self.cmdtag7.split(".")
                    self.cmdtag7 = self.cmdtag7[0]

                if col == 16:
                    self.cmdtag8 = str(item)
                    self.cmdtag8 = self.cmdtag8.split(".")
                    self.cmdtag8 = self.cmdtag8[0]

                if col == 17:
                    self.setholdingvalue = int(item)

                if col == 18:
                    self.samplingvaluerate = float(item)


        except Exception as e:
            level = logging.ERROR
            messege = 'Event:' + "FN_Ramp" + str(e.args)
            logger.log(level, messege)

    def initialization(self):
        client = Communication()
        sta_con_plc = client.opc_client_connect(self.filename)
        writegeneral = WriteGeneral(sta_con_plc)
        readgeneral = ReadGeneral(sta_con_plc)

        self.processrawvalue = self.unscaling(self.val,10000,self.highlimit,self.lowerlimit,0)
        self.lowerlimitrawvalue = self.unscaling(self.lowerlimit,10000,self.highlimit,self.lowerlimit,0)
        self.highlimitrawvalue = self.unscaling(self.highlimit, 10000, self.highlimit, self.lowerlimit, 0)


        sta_con_plc.close()


    def callincreaserampprocess(self):

        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            writegeneral = WriteGeneral(sta_con_plc)
            readgeneral = ReadGeneral(sta_con_plc)
            self.negativepluse = False
            currentrawvalue = readgeneral.readsymbolvalue(self.outputtag, 'analog')

            if  currentrawvalue < self.processrawvalue:
                local_p1 = threading.Thread(target=self.increasingthread,args=(self.filename,currentrawvalue,self.processrawvalue,self.outputtag,self.samplingvaluerate))
                local_p1.start()
            sta_con_plc.close()

        except Exception as e:
            level = logging.ERROR
            print(e.args)
            messege = "Ramp" + self.devicename + " Error messege(Increase process)" + str(e.args)
            logger.log(level, messege)

    def calldecreaserampprocess(self):
        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            writegeneral = WriteGeneral(sta_con_plc)
            readgeneral = ReadGeneral(sta_con_plc)
            self.postivepluse = False
            currentrawvalue = readgeneral.readsymbolvalue(self.outputtag, 'analog')

            if  currentrawvalue > self.lowerlimitrawvalue:
                local_p2 = threading.Thread(target=self.decreasingthread, args=(
                self.filename, currentrawvalue, self.lowerlimitrawvalue, self.outputtag, self.samplingvaluerate))
                local_p2.start()


            sta_con_plc.close()

        except Exception as e:
            level = logging.ERROR
            print(e.args)
            messege = "Ramp" + self.devicename + " Error messege(Decrease process)" + str(e.args)
            logger.log(level, messege)

    def unscaling(self, val, engineeringvaluerange, highlimit, lowlimit, engineeringlowlimit):
        processvaluerange = highlimit - lowlimit
        enggunit = (engineeringvaluerange / processvaluerange) * (val - lowlimit) + engineeringlowlimit
        return enggunit

    @property
    def areaname(self):
        return self.area

    @property
    def processvalue(self):
        client = Communication()
        sta_con_plc = client.opc_client_connect(self.filename)
        readgeneral = ReadGeneral(sta_con_plc)
        currentrawvalue = readgeneral.readsymbolvalue(self.outputtag, 'analog')
        sta_con_plc.close()
        return float(((self.highlimit - self.lowerlimit) * (currentrawvalue / 10000)) + self.lowerlimit)


    @property
    def setpointvalue(self):
        return (self.val - 0.2)

    @property
    def lowerlimitvalue(self):
        return self.lowerlimit


    @property
    def IncreaseCmd(self):
        return self._increasecmdvalue

    @IncreaseCmd.setter
    def IncreaseCmd(self, value):
        if value != self._increasecmdvalue:
            self._increasecmdvalue = value
            super().fire1()


    @property
    def DecreaseCmd(self):
        return self._decreasecmdvalue

    @DecreaseCmd.setter
    def DecreaseCmd(self, value):
        if value != self._decreasecmdvalue:
            self._decreasecmdvalue = value
            super().fire2()


    def readalltags(self):
        n = 3
        row, col = self.df.shape
        while n < col:
            data = self.df.iloc[self._idxNo, n]
            yield data,n
            n = n + 1

    def increasingthread(self, filename,currentrawvalue, targetrawvalue,outputtag, sampleratevalue):
        client = Communication()
        sta_con_plc = client.opc_client_connect(filename)
        writegeneral = WriteGeneral(sta_con_plc)
        readgeneral = ReadGeneral(sta_con_plc)
        rateofchange = (targetrawvalue - currentrawvalue)/sampleratevalue
        try:
            while ((currentrawvalue < targetrawvalue) and self._increasecmdvalue) :
                outrawvalue = currentrawvalue + rateofchange
                if outrawvalue > targetrawvalue:
                    writegeneral.writesymbolvalue(outputtag, 'analog', targetrawvalue)
                else:
                    writegeneral.writesymbolvalue(outputtag, 'analog', outrawvalue)

                currentrawvalue = readgeneral.readsymbolvalue(outputtag, 'analog')
                time.sleep(1)

            sta_con_plc.close()

            gc.collect()


        except Exception as e:
            level = logging.ERROR
            print(e.args)
            messege = "Ramp" + " Error messege(increasingthread)" + str(e.args)
            logger.log(level, messege)



    def decreasingthread(self, filename, currentrawvalue, targetrawvalue, outputtag, sampleratevalue):
        client = Communication()
        sta_con_plc = client.opc_client_connect(filename)
        writegeneral = WriteGeneral(sta_con_plc)
        readgeneral = ReadGeneral(sta_con_plc)
        rateofchange = (targetrawvalue - currentrawvalue) / sampleratevalue
        try:
            while (currentrawvalue > targetrawvalue) and self._decreasecmdvalue:
                outrawvalue = currentrawvalue + rateofchange
                if outrawvalue < targetrawvalue:
                    writegeneral.writesymbolvalue(outputtag, 'analog', targetrawvalue)
                else:
                    writegeneral.writesymbolvalue(outputtag, 'analog', outrawvalue)

                currentrawvalue = readgeneral.readsymbolvalue(outputtag, 'analog')
                time.sleep(1)
            sta_con_plc.close()
            gc.collect()

        except Exception as e:
            level = logging.ERROR
            print(e.args)
            messege = "Ramp" + " Error messege(decreasingthread)" + str(e.args)
            logger.log(level, messege)

















