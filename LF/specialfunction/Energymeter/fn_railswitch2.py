from logger import *
from event_V2 import *
from time import sleep
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import logging
import  general

logger = logging.getLogger("main.log")

__all__ = ['Fn_RailSwitch2']


class Fn_RailSwitch2(Eventmanager):



    def __init__(self,filename):
        self.filename = filename
        self.count = 0
        self._fwdlimitswtvalue = False
        self._revlimitswtvalue = False
        # self._fwdrunFBvalue = False
        # self._revrunFBvalue = False
        self.setup()
        self.initilizedigitalinput()
        super().__init__(lambda: self.process())

    def setup(self):
        try:

            self.lengthsp = str("db300.dbw10")
            self.speedsp = str("db300.dbw16")
            self.start = str("db300.dbw36.0")
            self.stop = str("db300.dbw36.4")
            self.lengthpv = str("db301.dbw10")
            self.speedpv = str("db301.dbw16")
            self.fbstrand1 = str("db301.dbw46.0")
            self.fb = str("db301.dbw46.1")
            self.reset = str("db300.dbw36.7")
            self.runfb = str("db301.dbw45.7")


        except Exception as e:
            level = logging.ERROR
            messege = "FN_MOTOR2D" + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)

    def initilizedigitalinput(self):
       pass
    def process(self):
        print("iwas here in fyction2")


        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)
            self.lengthspvalue = readgeneral.readDBvalue(self.lengthsp, "S7WLWord")
            self.speedspvalue = readgeneral.readDBvalue(self.speedsp, "S7WLWord")
            self.startvalue = readgeneral.readDBvalue(self.start, "S7WLBit")
            self.stopvalue = readgeneral.readDBvalue(self.stop, "S7WLBit")
            self.lengthpvvalue = readgeneral.readDBvalue(self.lengthpv, "S7WLWord")
            self.fbstrand1value = readgeneral.readDBvalue(self.fbstrand1, "S7WLBit")
            self.resetvalue = readgeneral.readDBvalue(self.reset, "S7WLBit")
            self.speedpvvalue = readgeneral.readDBvalue(self.speedpv, "S7WLWord")

            if self.speedspvalue > self.speedpvvalue and self.startvalue == True and self.stopvalue == False and self.fbstrand1value == True:
                diff = self.speedspvalue - self.speedpvvalue

                count = .2 * diff

                self.speedpvvalue = self.speedpvvalue + count
                writegeneral.writeDBvalue(self.speedpv, self.speedpvvalue, 'S7WLWord')

            if self.speedspvalue <= self.speedpvvalue and self.startvalue == True and self.stopvalue == False and self.fbstrand1value == True:
                diff = self.speedpvvalue - self.speedspvalue

                count = .2 * diff
                self.speedpvvalue = self.speedpvvalue - count
                writegeneral.writeDBvalue(self.speedpv, self.speedpvvalue, 'S7WLWord')

            if self.lengthspvalue > (self.lengthpvvalue+10) and self.startvalue == True and self.stopvalue == False and self.fbstrand1value == True and self.resetvalue == False:
                diff = self.lengthspvalue - self.lengthpvvalue
                count = .005 * diff * self.speedspvalue
                self.lengthpvvalue= self.lengthpvvalue+ count
                writegeneral.writeDBvalue(self.lengthpv,self.lengthpvvalue, 'S7WLWord')

            if self.startvalue == True and self.stopvalue == False and self.fbstrand1value == True:
                writegeneral.writeDBvalue(self.runfb, 1, 'S7WLBit')
            else:
                writegeneral.writeDBvalue(self.runfb, 0, 'S7WLBit')

            if self.lengthspvalue <= (self.lengthpvvalue + 10) and self.startvalue == True and self.stopvalue == False and self.fbstrand1value == True and self.resetvalue == False:
                writegeneral.writeDBvalue(self.fb, 1, 'S7WLBit')

            if self.resetvalue == True:
                writegeneral.writeDBvalue(self.fb, 0, 'S7WLBit')
                writegeneral.writeDBvalue(self.lengthpv, 0, 'S7WLWord')
                writegeneral.writeDBvalue(self.speedpv, 0, 'S7WLWord')

            if self.lengthspvalue == 0:
                writegeneral.writeDBvalue(self.lengthpv, 0, 'S7WLWord')
            sta_con_plc.disconnect()

        except Exception as e:
            log_exception(e)
            level = logging.INFO
            messege = "Strand2" + ":" + " Exception rasied(process): " + str(e.args) + str(e)
            logger.log(level, messege)








