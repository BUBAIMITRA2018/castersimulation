from logger import *
from event_V2 import *
from time import sleep
import logging
logger = logging.getLogger("main.log")

__all__ = ['Fn_VibroFeeder']




class Fn_VibroFeeder(Eventmanager):

    def __init__(self,com,df,idxNo):
        self._idxNo =idxNo
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
            self._oncmdvalue = self.gen.readgeneral.readtagvalue(self.cmdtag)
            if len(self.remoteFBtag) > 3:
                self.gen.writegeneral.writenodevalue(self.remoteFBtag, 1)
                level = logging.INFO
                messege = self.devicename + ":" + self.remoteFBtag + " is trigger by 1"
                logger.log(level, messege)


            if len(self.modulefaulttag) > 3:
                self.gen.writegeneral.writenodevalue(self.modulefaulttag, 0)
                level = logging.INFO
                messege = self.devicename + ":" + self.modulefaulttag + " is trigger by 0"
                logger.log(level, messege)


            if len(self.feedertriptag) > 3:
                self.gen.writegeneral.writenodevalue(self.feedertriptag, 0)
                level = logging.INFO
                messege = self.devicename + ":" + self.feedertriptag + " is trigger by 0"
                logger.log(level, messege)


            if len(self.pshealthytag) > 3:
                self.gen.writegeneral.writenodevalue(self.pshealthytag, 1)
                level = logging.INFO
                messege = self.devicename + ":" + self.pshealthytag + " is trigger by 1"
                logger.log(level, messege)


            if len(self.thyinoprtag) > 3:
                self.gen.writegeneral.writenodevalue(self.thyinoprtag, 1)
                level = logging.INFO
                messege = self.devicename + ":" + self.thyinoprtag + " is trigger by 1"
                logger.log(level, messege)
                
            self.Viborfeederprocess()



        except Exception as e:
            level = logging.ERROR
            messege = "FN_Vibrofeeder" + self.devicename + " Error messege(initilization)" + str(e.args)
            logger.log(level, messege)





    def Viborfeederprocess(self):

        try:

            self.tagvalue = self.gen.readgeneral.readtagvalue(self.cmdtag)

            if self.tagvalue == True:
                setvalue = self.gen.readgeneral.readtagvalue(self.speedsetpointtag)
                self.gen.writegeneral.writenodevalue(self.speedprocessvaluetag, setvalue)
                level = logging.WARNING
                messege = self.devicename + ":" + self.speedprocessvaluetag + " value is" + str(setvalue)
                logger.log(level, messege)
                self.speedPV = setvalue

            else:
                self.gen.writegeneral.writenodevalue(self.speedprocessvaluetag, 0)

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






