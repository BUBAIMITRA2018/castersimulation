import time
from event_V2 import *
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import logging
import gc
logger = logging.getLogger("main.log")

__all__ = ['FN_ProportionalValve']




class FN_ProportionalValve(Eventmanager):

    def __init__(self,com,df,idxNo,filename):
        self._idxNo =idxNo
        self.filename = filename
        self.gen = com
        self._positionsp = 0.0
        self.df = df
        self.devicename = df.iloc[self._idxNo, 0]
        self.setup()
        self.initilizedigitalinput()
        super().__init__(lambda: self.Proportionalprocess())


    def setup(self):
        try:

            for tag,col in self.readalltags():

                if col==3:
                    self.areatag = str(tag)


                if col == 4:
                    self.possetpointtag = str(tag)


                if col == 5:
                    self.upposlimitswtag = str(tag)


                if col == 6:
                    self.downposlimitswtag =str(tag)



        except Exception as e:
            level = logging.ERROR
            messege = "FN_ProportionalValve" + self.devicename + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)

    def initilizedigitalinput(self):

        try:
            self.Proportionalprocess()

        except Exception as e:
            level = logging.ERROR
            messege = "FN_ProportionalValve" + self.devicename + " Error messege(initilization)" + str(e.args)
            logger.log(level, messege)





    def Proportionalprocess(self):

        try:

            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)

            self.currentvalue = readgeneral.readsymbolvalue(self.possetpointtag, 'S7WLWord', 'PA')

            print("proportional valve start")
            print("current value is ", self.currentvalue)



            if self.currentvalue == 8294:
                writegeneral.writesymbolvalue(self.upposlimitswtag, 0, 'S7WLBit')
                time.sleep(1)
                writegeneral.writesymbolvalue(self.downposlimitswtag, 1, 'S7WLBit')

                level = logging.WARNING
                messege = self.devicename + ":" + self.downposlimitswtag + " value is" + "1"
                logger.log(level, messege)

            if self.currentvalue == 19353:
                writegeneral.writesymbolvalue(self.downposlimitswtag, 0, 'S7WLBit')
                time.sleep(5)
                writegeneral.writesymbolvalue(self.upposlimitswtag, 1, 'S7WLBit')

                level = logging.WARNING
                messege = self.devicename + ":" + self.downposlimitswtag + " value is" + "1"
                logger.log(level, messege)


            sta_con_plc.disconnect()
            gc.collect()

        except Exception as e:
            level = logging.ERROR
            messege = "FN_ProportionalValve" + self.devicename + " Error messege(process)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)

    @property
    def PosSetpoint(self):
        return self._positionsp

    @PosSetpoint.setter
    def PosSetpoint(self, value):
        if value != self._positionsp:
            super().fire()
            self._positionsp = value



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






