from logger import *
from event_V2 import *
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import logging
import gc



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
                    self.fwdrunFBtag = str(tag)

                if col == 8:
                    self.revrunFBtag = str(tag)

                if col == 9:
                    self.healthyFBtag = str(tag)
                if col == 10:
                    self.readyFBtag = str(tag)

                if col == 11:
                    self.mccbonFeedBacktag = str(tag)

                if col == 12:
                    self.overloadFeedBacktag = str(tag)

                if col == 13:
                    self.faultFBtag = str(tag)

                if col == 14:
                    self.delaytimetag = tag

                if col == 15:
                    self.FwdPlcRlstag = str(tag)

                if col == 16:
                    self.BwdPlcRlstag = str(tag)

                if col == 17:
                    self.openLStag = str(tag)

                if col == 18:
                    self.closeLStag = str(tag)





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

            self._fwdoncmdvalue = readgeneral.readsymbolvalue(self.fwdcmdtag,"digital")
            self._revoncmdvalue = readgeneral.readsymbolvalue(self.revcmdtag,"digital")
            self._fwdrunFBvalue = readgeneral.readsymbolvalue(self.fwdrunFBtag,"digital")
            self._revrunFBvalue = readgeneral.readsymbolvalue(self.revrunFBtag,"digital")


            if len(self.remFBtag) > 3:
                writegeneral.writesymbolvalue(self.remFBtag, 'digital', 1 )
                level = logging.INFO
                messege = self.devicename + ":" + self.remFBtag + " is trigger by 1"
                logger.log(level, messege)




            if len(self.healthyFBtag) > 3:

                writegeneral.writesymbolvalue(self.healthyFBtag,  'digital', 1 )
                level = logging.INFO
                messege = self.devicename + ":" + self.healthyFBtag + " is trigger by 1"
                logger.log(level, messege)



            if len(self.readyFBtag) > 3:
                writegeneral.writesymbolvalue(self.readyFBtag, 'digital', 1)
                level = logging.INFO
                messege = self.devicename + ":" + self.readyFBtag + " is trigger by 1"
                logger.log(level, messege)



            if len(self.mccbonFeedBacktag) > 3:
                writegeneral.writesymbolvalue(self.mccbonFeedBacktag, 'digital', 1)
                level = logging.INFO
                messege = self.devicename + ":" + self.mccbonFeedBacktag + " is trigger by 1"
                logger.log(level, messege)



            if len(self.overloadFeedBacktag) > 3:
                writegeneral.writesymbolvalue(self.overloadFeedBacktag, 'digital', 0)
                level = logging.INFO
                messege = self.devicename + ":" + self.overloadFeedBacktag + " is trigger by 0"
                logger.log(level, messege)



            if len(self.faultFBtag) > 3:
                writegeneral.writesymbolvalue(self.faultFBtag,'digital', 1)
                level = logging.INFO
                messege = self.devicename + ":" + self.faultFBtag + " is trigger by 1"
                logger.log(level, messege)

            sta_con_plc.close()



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

            self.fwdcmdvalue = readgeneral.readsymbolvalue(self.fwdcmdtag,"digital")
            self.revcmdvalue =  readgeneral.readsymbolvalue(self.revcmdtag,"digital")

            #
            if self.fwdcmdvalue == True and self.revcmdvalue == False:

                writegeneral.writesymbolvalue(self.fwdrunFBtag, 'digital', 1)
                writegeneral.writesymbolvalue(self.revrunFBtag, 'digital', 0)

                writegeneral.writesymbolvalue(self.openLStag, 'digital', 1)
                writegeneral.writesymbolvalue(self.closeLStag, 'digital', 0)

                self.RevRunFB = False
                self.FwdRunFB  = True
                level = logging.WARNING
                messege = self.devicename + ":" + self.fwdrunFBtag + " is trigger by 1" + self.openLStag + "is triggered by 1"
                logger.log(level, messege)

            if self.fwdcmdvalue == False and self.revcmdvalue == True:

                writegeneral.writesymbolvalue(self.fwdrunFBtag, 'digital', 0)
                writegeneral.writesymbolvalue(self.revrunFBtag, 'digital', 1)

                writegeneral.writesymbolvalue(self.openLStag, 'digital', 0)
                writegeneral.writesymbolvalue(self.closeLStag, 'digital', 1)
                self.RevRunFB = True
                self.FwdRunFB = False
                level = logging.WARNING
                messege = self.devicename + ":" + self.fwdrunFBtag + self.revrunFBtag + " is trigger by 1" + self.closeLStag + "is triggered by 1"
                logger.log(level, messege)

            if self.fwdcmdvalue == False and self.revcmdvalue == False:

                writegeneral.writesymbolvalue(self.fwdrunFBtag, 0,'S7WLBit')
                writegeneral.writesymbolvalue(self.revrunFBtag, 0,'S7WLBit')
                self.RevRunFB = False
                self.FwdRunFB = False
                level = logging.WARNING

            if self.fwdcmdvalue == True and self.revcmdvalue == True:

                writegeneral.writesymbolvalue(self.fwdrunFBtag, 'digital', 0)
                writegeneral.writesymbolvalue(self.revrunFBtag, 'digital', 0)
                self.RevRunFB = False
                self.FwdRunFB = False
                level = logging.WARNING

            sta_con_plc.close()
            gc.collect()



        except Exception as e:
            log_exception(e)
            level = logging.INFO
            messege = self.devicename + ":" + " Exception rasied(process): " + str(e.args) + str(e)
            logger.log(level, messege)
            print("Motor 2d error:",e.args)




    @property
    def FwdOnCmd(self):
        return self._fwdoncmdvalue

    @FwdOnCmd.setter
    def FwdOnCmd(self, value):
        if value != self._fwdoncmdvalue:
            super().fire()
            self._fwdoncmdvalue = value

    @property
    def RevOnCmd(self):
        return self._revoncmdvalue

    @RevOnCmd.setter
    def RevOnCmd(self, value):
        if value != self._revoncmdvalue:
            super().fire()
            self._revoncmdvalue = value


    @property
    def FwdRunFB(self):
        return self._fwdrunFBvalue

    @FwdRunFB.setter
    def FwdRunFB(self,value):
        self._fwdrunFBvalue = value

    @property
    def RevRunFB(self):
        return self._revrunFBvalue

    @RevRunFB.setter
    def RevRunFB(self, value):
        self._revrunFBvalue = value

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
    def areaname(self):
        return self.areatag



    def readalltags(self):
        n = 3
        row, col = self.df.shape
        print(col)
        while n < col:
            data = self.df.iloc[self._idxNo, n]
            yield data,n
            n = n + 1





