from logger import *
from event_V2 import *
from time import sleep
import logging


setup_logging_to_file("sov2S.log")
logger = logging.getLogger("main.log")

__all__ = ['Fn_Sov2S']




class Fn_Sov2S(Eventmanager):

    def __init__(self,com,df,idxNo):
        self._idxNo =idxNo
        self.gen = com
        self.df = df
        self.devicename = df.iloc[self._idxNo, 0]
        self._opncmdvalue = False
        self._clscmdvalue = False
        self._opnFBvalue = False
        self._clsFBvalue = False
        self._opntorqueFBvalue = False
        self._clstorqueFBvalue = False
        self.setup()
        self.initilizedigitalinput()
        super().__init__(lambda: self.sov2sprocess())


    def setup(self):
        try:
            for tag,col in self.readalltags():

                if col==3:
                    self.areatag = str(tag)


                if col==4:
                    self.opencmdtag = str(tag)


                if col == 5:
                    self.closecmdtag = str(tag)


                if col == 6:
                    self.openFBtag = str(tag)


                if col == 7:
                    self.closeFBtag = str(tag)


                if col == 8:
                    self.delaytimetag = tag


                if col == 9:
                    self.torqueOpenFBtag = str(tag)


                if col == 10:
                    self.torquecloseFBtag = str(tag)


                if col == 11:
                    self.torquedelaytimetag = tag

        except Exception as e:
            level = logging.ERROR
            messege = "FN_SOV2S" + self.devicename + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)


    def initilizedigitalinput(self):

        try:
            pass

        except Exception as e:
            level = logging.ERROR
            messege = "FN_SOV2S" + self.devicename + " Error messege(initilization)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)

    def sov2sprocess(self):

        try:
            print("Hello I am fire")
            self.opncmdvalue = self.gen.readgeneral.readtagvalue(self.opencmdtag)
            self.clscmdvalue = self.gen.readgeneral.readtagvalue(self.closecmdtag)

            if self.opncmdvalue == True and self.clscmdvalue == False:
                self.gen.writegeneral.writenodevalue(self.closeFBtag, 0)
                if len(self.torquecloseFBtag) > 3:
                    self.gen.writegeneral.writenodevalue(self.torquecloseFBtag, 0)
                sleep(self.delaytimetag)
                self.gen.writegeneral.writenodevalue(self.openFBtag, 1)
                if len(self.torqueOpenFBtag) > 3:
                    self.gen.writegeneral.writenodevalue(self.torqueOpenFBtag, 1)

                self.opnFB = True
                self.clsFB = False
                self.torqueclsFB = False
                self.torqueopnFB = True


                level = logging.WARNING
                messege = self.devicename + ":" + self.torquecloseFBtag + " is trigger by 0" \
                + self.closeFBtag + " is trigger by 0" + self.openFBtag + " is trigger by 1 " \
                + self.torqueOpenFBtag + "is trigger by 1"
                logger.log(level, messege)

            if self.opncmdvalue == False and self.clscmdvalue == True:
                self.gen.writegeneral.writenodevalue(self.openFBtag, 0)
                if len(self.torqueOpenFBtag) > 3:
                    self.gen.writegeneral.writenodevalue(self.torqueOpenFBtag, 0)
                sleep(self.delaytimetag)
                self.gen.writegeneral.writenodevalue(self.closeFBtag, 1)
                if len(self.torquecloseFBtag) > 3:
                    self.gen.writegeneral.writenodevalue(self.torquecloseFBtag, 1)
                level = logging.WARNING
                messege = self.devicename + ":" + self.torquecloseFBtag + " is trigger by 1" \
                          + self.closeFBtag + " is trigger by 1" + self.openFBtag + " is trigger by 0 " \
                          + self.torqueOpenFBtag + "is trigger by 0"
                logger.log(level, messege)

                self.opnFB = False
                self.clsFB = True
                self.torqueclsFB = True
                self.torqueopnFB = False




        except Exception as e:
            log_exception(e)
            level = logging.ERROR
            messege = self.devicename + ":" + " Exception rasied(process): " + str(e.args) + str(e)
            logger.log(level, messege)


    @property
    def opncomd(self):
        return self._opncmdvalue

    @opncomd.setter
    def opncomd(self,value):
        if value != self._opncmdvalue:
            super().fire()
            self._opncmdvalue = value

    @property
    def clscomd(self):
        return self._clscmdvalue

    @clscomd.setter
    def clscomd(self, value):
        if value != self._clscmdvalue:
            super().fire()
            self._clscmdvalue = value


    @property
    def opnFB(self):
        return self._opnFBvalue

    @opnFB.setter
    def opnFB(self,value):
        self._opnFBvalue = value

    @property
    def clsFB(self):
        return self._clsFBvalue

    @clsFB.setter
    def clsFB(self, value):
        self._clsFBvalue = value

    @property
    def torqueclsFB(self):
        return self._clstorqueFBvalue

    @torqueclsFB.setter
    def torqueclsFB(self, value):
        self._clstorqueFBvalue = value

    @property
    def torqueopnFB(self):
        return self._opntorqueFBvalue

    @torqueopnFB.setter
    def torqueopnFB(self, value):
        self._opntorqueFBvalue = value

    @property
    def areaname(self):
        return self.areatag


    def readalltags(self):
        n = 3
        row, col = self.df.shape
        while n < col:
            data = self.df.iloc[self._idxNo, n]
            yield data,n
            n = n + 1









