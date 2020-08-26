
from event_V2 import *
import gc
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import logging
import time


logger = logging.getLogger("main.log")

__all__ = ['Fn_Motor2D']


class Fn_Motor2D(Eventmanager):



    def __init__(self,com,df,idxNo,filename):
        self._idxNo =idxNo
        self.devicename = df.iloc[self._idxNo,0]
        self.filename = filename
        self.gen = com
        self._fwdoncmdvalue = False
        self._revoncmdvalue = False
        self._fwdrunFBvalue = False
        self._revrunFBvalue = False
        self.df = df
        self.setup()
        self.initilizedigitalinput()
        super().__init__(lambda: self.motor2dprocess())




    def setup(self):
        try:


            for tag,col in self.readalltags():

                if col==3:
                    self.areatag = str(tag)


                if col==4:
                    self.fwdcmdtag = str(tag)

                if col==5:
                    self.revcmdtag = str(tag)

                if col==6:
                    self.remFBtag = str(tag)

                if col ==7:
                    self.fwdrunFBtag1 = str(tag)

                if col == 8:
                    self.revrunFBtag1 = str(tag)

                if col ==9:
                    self.fwdrunFBtag2 = str(tag)

                if col == 10:
                    self.revrunFBtag2 = str(tag)

                if col == 11:
                    self.fwdrunFBtag3 = str(tag)

                if col == 12:
                    self.revrunFBtag3 = str(tag)

                if col == 13:
                    self.fwdrunFBtag4 = str(tag)

                if col == 14:
                    self.revrunFBtag4 = str(tag)





        except Exception as e:
            level = logging.ERROR
            messege = "FN_MOTOR2D" + self.devicename + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)



    def initilizedigitalinput(self):

        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)



            self._fwdoncmdvalue = readgeneral.readsymbolvalue(self.fwdcmdtag,'S7WLBit','PA')
            self._revoncmdvalue = readgeneral.readsymbolvalue(self.revcmdtag,'S7WLBit','PA')
            if len(self.fwdrunFBtag1) > 3:
                writegeneral.writesymbolvalue(self.fwdrunFBtag1, 0, 'S7WLBit')
                print(self.fwdrunFBtag1)
            if len(self.fwdrunFBtag2) > 3:
                writegeneral.writesymbolvalue(self.fwdrunFBtag2, 0, 'S7WLBit')
                print(self.fwdrunFBtag2)
            if len(self.fwdrunFBtag3) > 3:
                writegeneral.writesymbolvalue(self.fwdrunFBtag3, 0, 'S7WLBit')
                print(self.fwdrunFBtag3)
            if len(self.fwdrunFBtag4) > 3:
                writegeneral.writesymbolvalue(self.fwdrunFBtag4, 0, 'S7WLBit')
                print(self.fwdrunFBtag4)
            if len(self.revrunFBtag1) > 3:
                writegeneral.writesymbolvalue(self.revrunFBtag1, 0, 'S7WLBit')
                print(self.revrunFBtag1)
            if len(self.revrunFBtag2) > 3:
                writegeneral.writesymbolvalue(self.revrunFBtag2, 0, 'S7WLBit')
                print(self.revrunFBtag2)
            if len(self.revrunFBtag3) > 3:
                writegeneral.writesymbolvalue(self.revrunFBtag3, 0, 'S7WLBit')
                print(self.revrunFBtag3)
            if len(self.revrunFBtag4) > 3:
                writegeneral.writesymbolvalue(self.revrunFBtag4, 0, 'S7WLBit')
                print(self.revrunFBtag4)

            if len(self.remFBtag) > 3:
                writegeneral.writesymbolvalue(self.remFBtag, 1,'S7WLBit')
                level = logging.INFO
                messege = self.devicename + ":" + self.remFBtag + " is trigger by 1"
                logger.log(level, messege)


            sta_con_plc.disconnect()



        except Exception as e:
            level = logging.ERROR
            messege = "FN_MOTOR2D" + self.devicename + " Error messege(initilization)" + str(e.args)
            logger.log(level, messege)



    def motor2dprocess(self):

        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)



            self.fwdcmdvalue = readgeneral.readsymbolvalue(self.fwdcmdtag,'S7WLBit','PA')
            self.revcmdvalue =  readgeneral.readsymbolvalue(self.revcmdtag,'S7WLBit','PA')

            if self.fwdcmdvalue == True and self.revcmdvalue == False:


                if len(self.revrunFBtag1) > 3:
                    writegeneral.writesymbolvalue(self.revrunFBtag1, 0, 'S7WLBit')
                if len(self.revrunFBtag2) > 3:
                    writegeneral.writesymbolvalue(self.revrunFBtag2, 0, 'S7WLBit')
                if len(self.revrunFBtag3) > 3:
                    writegeneral.writesymbolvalue(self.revrunFBtag3, 0, 'S7WLBit')
                if len(self.revrunFBtag4) > 3:
                    writegeneral.writesymbolvalue(self.revrunFBtag4, 0, 'S7WLBit')

                if len(self.fwdrunFBtag1) > 3:
                    writegeneral.writesymbolvalue(self.fwdrunFBtag1, 1,'S7WLBit')
                if len(self.fwdrunFBtag2) > 3:
                    writegeneral.writesymbolvalue(self.fwdrunFBtag2, 1,'S7WLBit')
                if len(self.fwdrunFBtag3) > 3:
                    writegeneral.writesymbolvalue(self.fwdrunFBtag3, 1,'S7WLBit')
                if len(self.fwdrunFBtag4) > 3:
                    writegeneral.writesymbolvalue(self.fwdrunFBtag4, 1,'S7WLBit')


                self.RevRunFB1 = False
                self.RevRunFB2 = False
                self.RevRunFB3 = False
                self.RevRunFB4 = False

                self.FwdRunFB1 = True
                self.FwdRunFB2 = True
                self.FwdRunFB3 = True
                self.FwdRunFB4 = True

                level = logging.WARNING
                messege = self.devicename + ":" + self.fwdrunFBtag1 +" / "+ self.fwdrunFBtag2 +" / "+ self.fwdrunFBtag3 +" / "+ self.fwdrunFBtag4 + " is trigger by 1"
                logger.log(level, messege)

            if self.fwdcmdvalue == False and self.revcmdvalue == True:
                if len(self.fwdrunFBtag1) > 3:
                    writegeneral.writesymbolvalue(self.fwdrunFBtag1, 0,'S7WLBit')
                if len(self.fwdrunFBtag2) > 3:
                    writegeneral.writesymbolvalue(self.fwdrunFBtag2, 0,'S7WLBit')
                if len(self.fwdrunFBtag3) > 3:
                    writegeneral.writesymbolvalue(self.fwdrunFBtag3, 0,'S7WLBit')
                if len(self.fwdrunFBtag4) > 3:
                    writegeneral.writesymbolvalue(self.fwdrunFBtag4, 0,'S7WLBit')

                if len(self.revrunFBtag1) > 3:
                    writegeneral.writesymbolvalue(self.revrunFBtag1, 1, 'S7WLBit')
                if len(self.revrunFBtag2) > 3:
                    writegeneral.writesymbolvalue(self.revrunFBtag2, 1, 'S7WLBit')
                if len(self.revrunFBtag3) > 3:
                    writegeneral.writesymbolvalue(self.revrunFBtag3, 1, 'S7WLBit')
                if len(self.revrunFBtag4) > 3:
                    writegeneral.writesymbolvalue(self.revrunFBtag4, 1, 'S7WLBit')


                self.FwdRunFB1 = False
                self.FwdRunFB2 = False
                self.FwdRunFB3 = False
                self.FwdRunFB3 = False

                self.RevRunFB1 = True
                self.RevRunFB2 = True
                self.RevRunFB3 = True
                self.RevRunFB4 = True

                level = logging.WARNING
                messege = self.devicename + ":" + self.revrunFBtag1 + " / " + self.revrunFBtag2 + " / " + self.revrunFBtag3 + " / " +  self.revrunFBtag4 + " is trigger by 1"
                logger.log(level, messege)



            sta_con_plc.disconnect()

            gc.collect()



        except Exception as e:
            log_exception(e)
            level = logging.INFO
            messege = self.devicename + ":" + " Exception rasied(process): " + str(e.args) + str(e)
            logger.log(level, messege)





    @property
    def FwdOnCmd(self):
        return self._fwdoncmdvalue

    @FwdOnCmd.setter
    def FwdOnCmd(self, value):
        if value != self._fwdoncmdvalue:
            super().fire()
            print("thefuction is fire")
            self._fwdoncmdvalue = value

    @property
    def RevOnCmd(self):
        return self._revoncmdvalue

    @RevOnCmd.setter
    def RevOnCmd(self, value):
        if value != self._revoncmdvalue:
            super().fire()
            print("thefuction is fire")
            self._revoncmdvalue = value


    @property
    def FwdRunFB1(self):
        return self._fwdrunFBvalue1

    @FwdRunFB1.setter
    def FwdRunFB1(self,value):
        self._fwdrunFBvalue1 = value

    @property
    def RevRunFB1(self):
        return self._revrunFBvalue1

    @RevRunFB1.setter
    def RevRunFB1(self, value):
        self._revrunFBvalue1 = value

    @property
    def OpenLSFB(self):
        return self._openLSvalue

    @OpenLSFB.setter
    def OpenLSFB(self, value):
        if value != self._openLSvalue:
            super().fire()
            self._openLSvalue = value

    @property
    def CloseLSFB(self):
        return self._closeLSvalue

    @CloseLSFB.setter
    def CloseLSFB(self, value):
        if value != self._closeLSvalue:
            super().fire()
            self._closeLSvalue = value

    @property
    def FwdRunFB2(self):
        return self._fwdrunFBvalue2

    @FwdRunFB2.setter
    def FwdRunFB2(self, value):
        self._fwdrunFBvalue2 = value

    @property
    def RevRunFB2(self):
        return self._revrunFBvalue2

    @RevRunFB2.setter
    def RevRunFB2(self, value):
        self._revrunFBvalue2 = value

    @property
    def FwdRunFB3(self):
        return self._fwdrunFBvalue3

    @FwdRunFB3.setter
    def FwdRunFB3(self, value):
        self._fwdrunFBvalue3 = value

    @property
    def RevRunFB3(self):
        return self._revrunFBvalue3

    @RevRunFB3.setter
    def RevRunFB3(self, value):
        self._revrunFBvalue3 = value

    @property
    def FwdRunFB4(self):
        return self._fwdrunFBvalue4

    @FwdRunFB4.setter
    def FwdRunFB4(self, value):
        self._fwdrunFBvalue4 = value

    @property
    def RevRunFB4(self):
        return self._revrunFBvalue4

    @RevRunFB4.setter
    def RevRunFB4(self, value):
        self._revrunFBvalue4 = value



    @property
    def areaname(self):
        return self.areatag



    def readalltags(self):
        n = 3
        row, col = self.df.shape
        while n < col:
            data = self.df.iloc[self._idxNo, n]
            print(data)
            yield data,n
            n = n + 1





