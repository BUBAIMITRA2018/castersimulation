from logger import *
from event_V2 import *
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *

logger = logging.getLogger("main.log")

__all__ = ['Fn_Conveyor1D']




class Fn_Conveyor1D(Eventmanager):

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
                    self.cmdtag = str(tag)

                if col == 5:
                    self.remoteFBtag = str(tag)

                if col == 6:
                    self.runingFBtag = str(tag)


                if col == 7:
                    self.healthyFBtag = str(tag)


                if col == 8:
                    self.readyFBtag = str(tag)


                if col == 9:
                    self.mccbonFeedBacktag = str(tag)

                if col == 10:
                    self.overloadFeedBacktag = str(tag)


                if col == 11:
                    self.faultFBtag =str(tag)


                if col == 12:
                    self.delaytimetag = str(tag)

                if col == 13:
                    self.pullchordlefttag = str( tag)

                if col == 14:
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
                writegeneral.writesymbolvalue(self.faultFBtag,"digital", 0)
                level = logging.INFO
                messege = self.devicename + ":" + self.faultFBtag + " is trigger by 0"
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

            oncommandvalue = readgeneral.readsymbolvalue(self.cmdtag,"digital")
            if oncommandvalue:
                writegeneral.writesymbolvalue(self.runingFBtag,"digital",1)
                level = logging.WARNING
                messege = self.devicename + ":" + self.runingFBtag + " is trigger by 1"
                logger.log(level, messege)
                self.runFB = 1
            else:
                writegeneral.writesymbolvalue(self.runingFBtag,"digital", 0)
                self.runFB = 0

            sta_con_plc.close()

        except Exception as e:
            level = logging.ERROR
            messege = "FN_Conveyor" + self.devicename + " Error messege(process)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)

    @property
    def OnCmd(self):
        return self._oncmdvalue

    @OnCmd.setter
    def OnCmd(self, value):
        if value != self._oncmdvalue:
            super().fire()
            self._oncmdvalue = value

    @property
    def runFB(self):
        return self._runFBvalue

    @runFB.setter
    def runFB(self, value):
        self._runFBvalue = value

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






