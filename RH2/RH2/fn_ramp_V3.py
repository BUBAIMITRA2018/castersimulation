from event_V3 import *
from clientcomm_v1 import *
import random
from readgeneral_v2 import *
from  writegeneral_v2 import *

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
        super().__init__(lambda: self.increaserampprocess(),lambda : self.decreaserampprocess())




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

        writegeneral.writesymbolvalue(self.outputtag, 'analog', 0)

        sta_con_plc.close()


    def increaserampprocess(self):

        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            writegeneral = WriteGeneral(sta_con_plc)
            readgeneral = ReadGeneral(sta_con_plc)
            self.negativepluse = False
            self.currentrawvalue = readgeneral.readsymbolvalue(self.outputtag, 'analog')
            print("current raw value",self.currentrawvalue)
            self.currentpv = ((self.highlimit - self.lowerlimit) * (self.currentrawvalue / 10000)) + + self.lowerlimit
            self.processrawvalue =  int(((self.val-self.lowerlimit) * 10000) / (self.highlimit - self.lowerlimit))

            print("increase  command executed" + str(self.devicename))

            self.comparevalue = self.val - 0.2

            if not self.postivepluse and (self.val > self.currentpv):
                self.positiverate = (self.val - self.currentpv) / self.samplingvaluerate
                print("rate of increase", self.positiverate)
                self.postivepluse = True

            if self.comparevalue > self.currentpv:
                t1 = threading.Thread(target=self.increasefunction,
                                      args=(self.currentpv, self.comparevalue, self.processrawvalue,self.positiverate))
                t1.start()
              


            if self.currentpv >= self.val:
                self.postivepluse = False

            sta_con_plc.close()


        except Exception as e:
            level = logging.ERROR
            print(e.args)
            messege = "Ramp" + self.devicename + " Error messege(Increase process)" + str(e.args)
            logger.log(level, messege)

    def decreaserampprocess(self):
        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            writegeneral = WriteGeneral(sta_con_plc)
            readgeneral = ReadGeneral(sta_con_plc)
            self.postivepluse = False

            print("decrease command executed")

            self.currentrawvalue = readgeneral.readsymbolvalue(self.outputtag, 'analog')
            print("current raw value", self.currentrawvalue)
            self.currentpv = ( (self.highlimit - self.lowerlimit) * (self.currentrawvalue / 10000)) + self.lowerlimit
            print("current pv is ",  self.currentpv)


            if not self.negativepluse and (self.currentpv > self.lowerlimit):
                self.negativerate = (self.currentpv - self.lowerlimit) / self.samplingvaluerate
                self.negativepluse = True

            if self.lowerlimit < self.currentpv:
                print("t3 is executed")
                t3 = threading.Thread(target=self.decreasefunction, args=(
                    self.currentpv, self.lowerlimit, self.negativerate))
                t3.start()


            if self.currentpv <= self.lowerlimit:
                self.negativepluse = False

            sta_con_plc.close()

        except Exception as e:
            level = logging.ERROR
            print(e.args)
            messege = "Ramp" + self.devicename + " Error messege(Decrease process)" + str(e.args)
            logger.log(level, messege)


    def scaling(self, val, highlimit, lowlimit):
        rawvalue = int((val* 10000) / (highlimit - lowlimit))
        return rawvalue

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
        if value == True:
            print(self.devicename + "It is executed")
            super().fire1()
        self._increasecmdvalue = value





    @property
    def DecreaseCmd(self):
        return self._decreasecmdvalue

    @DecreaseCmd.setter
    def DecreaseCmd(self, value):
        if value == True:
            super().fire2()
        self._decreasecmdvalue = value




    def readalltags(self):
        n = 3
        row, col = self.df.shape
        while n < col:
            data = self.df.iloc[self._idxNo, n]
            yield data,n
            n = n + 1

    def increasefunction(self,currentpv, targetsp,processrawvalue, rate):
        client = Communication()
        sta_con_plc = client.opc_client_connect(self.filename)
        writegeneral = WriteGeneral(sta_con_plc)
        readgeneral = ReadGeneral(sta_con_plc)
        while (currentpv < targetsp):
            currentpv = currentpv + rate
            outrawvalue = self.scaling(currentpv, self.highlimit, self.lowerlimit)

            if outrawvalue > processrawvalue:
                writegeneral.writesymbolvalue(self.outputtag, 'analog', processrawvalue)
            else:
                writegeneral.writesymbolvalue(self.outputtag, 'analog', outrawvalue)
            break

        if (currentpv >= targetsp ):
            self._increasecmdvalue = True
        sta_con_plc.close()



    def decreasefunction(self, currentpv, targetsp, rate):
        client = Communication()
        sta_con_plc = client.opc_client_connect(self.filename)
        writegeneral = WriteGeneral(sta_con_plc)
        readgeneral = ReadGeneral(sta_con_plc)
        while (currentpv > targetsp):
            print("negative rate is ", rate)
            print("cureent pv is " , currentpv)
            currentpv = currentpv - rate
            print("cureent pv is ", currentpv)
            outrawvalue = int(((currentpv-self.lowerlimit)* 10000) / (self.highlimit - self.lowerlimit))
            print("outrawvalue is ", outrawvalue)
            if outrawvalue < 0:
                writegeneral.writesymbolvalue(self.outputtag, 'analog',0)

            else:
                writegeneral.writesymbolvalue(self.outputtag, 'analog', outrawvalue)

            break
        sta_con_plc.close()






