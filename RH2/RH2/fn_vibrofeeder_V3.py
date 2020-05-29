from logger import *
from event_V2 import *
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *

logger = logging.getLogger("main.log")

__all__ = ['Fn_VibroFeeder']




class Fn_VibroFeeder(Eventmanager):

    def __init__(self,com,df,idxNo,filename):
        self._idxNo =idxNo
        self.devicename = df.iloc[self._idxNo, 0]
        self.filename = filename
        self.gen = com
        self._speedpv = 0.0
        self.df = df
        self.devicename = df.iloc[self._idxNo, 0]
        self.setup()
        self.initilizedigitalinput()
        super().__init__(lambda: self.Viborfeederprocess())


    def setup(self):
        try:

            for tag,col in self.readalltags():

                if col==3:
                    self.areatag = str(tag)

                if col==4:
                    self.cmdtag = str(tag)

                if col == 5:
                    self.speedsetpointtag = str(tag)


                if col == 6:
                    self.speedprocessvaluetag = str(tag)


                if col == 7:
                    self.emergencyFBtag = str(tag)


                if col == 8:
                    self.remoteFBtag = str(tag)


                if col == 9:
                    self.modulefaulttag = str(tag)


                if col == 10:
                    self.feedertriptag = str(tag)


                if col == 11:
                    self.pshealthytag =str(tag)



                if col == 12:
                    self.thyinoprtag =str(tag)



        except Exception as e:
            level = logging.ERROR
            messege = "FN_Vibrofeeder" + self.devicename + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)

    def initilizedigitalinput(self):

        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)
            self._oncmdvalue = readgeneral.readsymbolvalue(self.cmdtag,"digital")

            if len(self.remoteFBtag) > 3:
                writegeneral.writesymbolvalue(self.remoteFBtag, 'digital', 1)
                level = logging.INFO
                messege = self.devicename + ":" + self.remoteFBtag + " is trigger by 1"
                logger.log(level, messege)


            if len(self.modulefaulttag) > 3:
                writegeneral.writesymbolvalue(self.modulefaulttag, 'digital', 0)
                level = logging.INFO
                messege = self.devicename + ":" + self.modulefaulttag + " is trigger by 0"
                logger.log(level, messege)


            if len(self.feedertriptag) > 3:
                writegeneral.writesymbolvalue(self.feedertriptag, 'digital', 0)
                level = logging.INFO
                messege = self.devicename + ":" + self.feedertriptag + " is trigger by 0"
                logger.log(level, messege)


            if len(self.pshealthytag) > 3:
                writegeneral.writesymbolvalue(self.pshealthytag, 'digital', 1)
                level = logging.INFO
                messege = self.devicename + ":" + self.pshealthytag + " is trigger by 1"
                logger.log(level, messege)


            if len(self.thyinoprtag) > 3:
                writegeneral.writesymbolvalue(self.thyinoprtag, 'digital', 1)
                level = logging.INFO
                messege = self.devicename + ":" + self.thyinoprtag + " is trigger by 1"
                logger.log(level, messege)

            sta_con_plc.close()



        except Exception as e:
            level = logging.ERROR
            messege = "FN_Vibrofeeder" + self.devicename + " Error messege(initilization)" + str(e.args)
            logger.log(level, messege)





    def Viborfeederprocess(self):

        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)

            self.tagvalue = readgeneral.readsymbolvalue(self.cmdtag,'digital')

            if self.tagvalue == True:
                setvalue = readgeneral.readsymbolvalue(self.speedsetpointtag,"analog")
                writegeneral.writesymbolvalue(self.speedprocessvaluetag, "analog", setvalue)
                level = logging.WARNING
                messege = self.devicename + ":" + self.speedprocessvaluetag + " value is" + str(setvalue)
                logger.log(level, messege)
                self.speedPV = setvalue
            else:
                writegeneral.writesymbolvalue(self.speedprocessvaluetag,"analog", 0)

            sta_con_plc.close()

        except Exception as e:
            level = logging.ERROR
            messege = "FN_Vibrofeeder" + self.devicename + " Error messege(process)" + str(e.args)
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
    def speedPV(self):
        return self._speedpv

    @speedPV.setter
    def speedPV(self,value):
        self._speedpv = value

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






