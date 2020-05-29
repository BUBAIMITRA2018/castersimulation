from logger import *
from event_V2 import *
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *

logger = logging.getLogger("main.log")

__all__ = ['Fn_Conveyor2D']




class Fn_Conveyor2D(Eventmanager):

    def __init__(self,com,df,idxNo,filename):
        self._idxNo =idxNo
        self.gen = com
        self.df = df
        self.filename = filename
        self.devicename = df.iloc[self._idxNo, 0]
        self._oncmdvalue = False
        self._runFBvalue = False
        self.setup()
        self.initilizedigitalinput()
        super().__init__(lambda: self.conveyorprocess())


    def setup(self):
        try:

            for tag,col in self.readalltags():

                if col==3:
                    self.areatag = str(tag)

                if col==4:
                    self.fwdcmdtag = str(tag)

                if col == 5:
                    self.revcmdtag = str(tag)


                if col == 6:
                    self.remoteFBtag = str(tag)

                if col == 7:
                    self.fwdruningFBtag = str(tag)

                if col == 8:
                    self.revruningFBtag = str(tag)


                if col == 9:
                    self.healthyFBtag = str(tag)


                if col == 10:
                    self.readyFBtag = str(tag)


                if col == 11:
                    self.mccbonFeedBacktag = str(tag)

                if col == 12:
                    self.overloadFeedBacktag = str(tag)


                if col == 13:
                    self.faultFBtag =str(tag)


                if col == 14:
                    self.delaytimetag = str(tag)

                if col == 15:
                    self.pullchordlefttag = str( tag)

                if col == 16:
                    self.pullchordrighttag = str(tag)


        except Exception as e:
            level = logging.ERROR
            messege = "FN_Conveyor" + self.devicename + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)

    def initilizedigitalinput(self):
        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)

            if len(self.healthyFBtag) > 3:
                writegeneral.writesymbolvalue(self.healthyFBtag,"digital",1)
                level = logging.INFO
                messege = self.devicename + ":" + self.healthyFBtag + " is trigger by 1"
                logger.log(level, messege)

            if len(self.remoteFBtag) > 3:
                writegeneral.writesymbolvalue(self.remoteFBtag,"digital",1)
                level = logging.INFO
                messege = self.devicename + ":" + self.remoteFBtag + " is trigger by 1"
                logger.log(level, messege)


            if len(self.readyFBtag) > 3:
                writegeneral.writesymbolvalue(self.readyFBtag,"digital",1)
                level = logging.INFO
                messege = self.devicename + ":" + self.readyFBtag + " is trigger by 1"
                logger.log(level, messege)


            if len(self.mccbonFeedBacktag) > 3:
                writegeneral.writesymbolvalue(self.mccbonFeedBacktag,"digital", 1)
                level = logging.INFO
                messege = self.devicename + ":" + self.mccbonFeedBacktag + " is trigger by 1"
                logger.log(level, messege)


            if len(self.overloadFeedBacktag) > 3:
                writegeneral.writesymbolvalue(self.overloadFeedBacktag,"digital", 0)
                level = logging.INFO
                messege = self.devicename + ":" + self.overloadFeedBacktag + " is trigger by 1"
                logger.log(level, messege)


            if len(self.faultFBtag) > 3:
                writegeneral.writesymbolvalue(self.faultFBtag,"digital", 1)
                level = logging.INFO
                messege = self.devicename + ":" + self.faultFBtag + " is trigger by 1"
                logger.log(level, messege)


            if len(self.pullchordlefttag) > 3:
                writegeneral.writesymbolvalue(self.pullchordlefttag,"digital", 0)
                level = logging.INFO
                messege = self.devicename + ":" + self.pullchordlefttag + " is trigger by 0"
                logger.log(level, messege)


            if len(self.pullchordrighttag) > 3:
                writegeneral.writesymbolvalue(self.pullchordrighttag,"digital",0)
                level = logging.INFO
                messege = self.devicename + ":" + self.pullchordlefttag + " is trigger by 0"
                logger.log(level, messege)

            sta_con_plc.close()

        except Exception as e :
            log_exception(e)
            level = logging.ERROR
            messege = "FN_Conveyor" + self.devicename + " Error messege(initilization)" + str(e.args)
            logger.log(level, messege)


    def conveyorprocess(self):

        try:

            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)

            self.fwdcmdvalue = readgeneral.readsymbolvalue(self.fwdcmdtag, "digital")
            self.revcmdvalue = readgeneral.readsymbolvalue(self.revcmdtag, "digital")

            #
            if self.fwdcmdvalue == True and self.revcmdvalue == False:
                writegeneral.writesymbolvalue(self.fwdruningFBtag, 'digital', 1)
                writegeneral.writesymbolvalue(self.revruningFBtag, 'digital', 0)



                self.RevRunFB = False
                self.FwdRunFB = True
                level = logging.WARNING
                messege = self.devicename + ":" + self.fwdruningFBtag + " is trigger by 1 "
                logger.log(level, messege)

            if self.fwdcmdvalue == False and self.revcmdvalue == True:
                writegeneral.writesymbolvalue(self.fwdruningFBtag, 'digital', 0)
                writegeneral.writesymbolvalue(self.revruningFBtag, 'digital', 1)


                self.RevRunFB = True
                self.FwdRunFB = False
                level = logging.WARNING
                messege = self.devicename + ":" + self.fwdruningFBtag + self.revruningFBtag + " is trigger by 1"
                logger.log(level, messege)

            if self.fwdcmdvalue == False and self.revcmdvalue == False:
                writegeneral.writesymbolvalue(self.fwdruningFBtag, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.revruningFBtag, 0, 'S7WLBit')
                self.RevRunFB = False
                self.FwdRunFB = False
                level = logging.WARNING

            if self.fwdcmdvalue == True and self.revcmdvalue == True:
                writegeneral.writesymbolvalue(self.fwdruningFBtag, 'digital', 0)
                writegeneral.writesymbolvalue(self.revruningFBtag, 'digital', 0)
                self.RevRunFB = False
                self.FwdRunFB = False
                level = logging.WARNING

            sta_con_plc.close()

        except Exception as e:
            level = logging.ERROR
            messege = "FN_Conveyor" + self.devicename + " Error messege(process)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)

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






