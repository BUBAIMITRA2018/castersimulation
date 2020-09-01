from logger import *
from event_V2 import *
from time import sleep
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import logging
import  general

logger = logging.getLogger("main.log")

__all__ = ['Fn_RailSwitch1']


class Fn_RailSwitch1(Eventmanager):



    def __init__(self,filename):
        self.filename = filename
        # self.count = 0
        self._fwdlimitswtvalue = False
        self._revlimitswtvalue = False
        # self._fwdrunFBvalue = False
        # self._revrunFBvalue = False
        self.setup()
        self.initilizedigitalinput()
        super().__init__(lambda: self.process())

    def setup(self):
        try:
            self.lengthsp = str("db300.dbw8")
            self.speedsp = str("db300.dbw14")
            self.start = str("db300.dbw36.0")
            self.stop = str("db300.dbw36.4")
            self.lengthpv = str("db301.dbw8")
            self.speedpv = str("db301.dbw14")
            self.fb = str("db301.dbw46.0")
            self.reset = str("db300.dbw36.7")
            self.runfb = str("db301.dbw45.6")

        except Exception as e:
            level = logging.ERROR
            messege = "FN_MOTOR2D" + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)

    def initilizedigitalinput(self):
        pass



    def process(self):
        print("iwas here in fyction1")

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
            self.speedpvvalue = readgeneral.readDBvalue(self.speedpv, "S7WLWord")
            print("the lenghth setpon",self.lengthspvalue)
            print("the kean pv ",self.lengthpvvalue)
            self.resetvalue = readgeneral.readDBvalue(self.reset, "S7WLBit")

            if self.speedspvalue > self.speedpvvalue and self.startvalue == True and self.stopvalue == False :
                diff = self.speedspvalue - self.speedpvvalue

                count = .2 * diff

                self.speedpvvalue = self.speedpvvalue + count
                writegeneral.writeDBvalue(self.speedpv, self.speedpvvalue, 'S7WLWord')

            if self.speedspvalue <= self.speedpvvalue and self.startvalue == True and self.stopvalue == False :
                diff = self.speedpvvalue - self.speedspvalue

                count = .2 * diff
                self.speedpvvalue = self.speedpvvalue - count
                writegeneral.writeDBvalue(self.speedpv, self.speedpvvalue, 'S7WLWord')


            if self.lengthspvalue > (self.lengthpvvalue +10) and self.startvalue == True and self.stopvalue == False and self.resetvalue == False:
                diff = self.lengthspvalue - self.lengthpvvalue

                count = .005 * diff * self.speedspvalue
                print("the counts are ",count)
                print("the counts are ", self.speedspvalue)
                self.lengthpvvalue = self.lengthpvvalue + count
                writegeneral.writeDBvalue(self.lengthpv, self.lengthpvvalue, 'S7WLWord')

            if self.startvalue == True and self.stopvalue == False:
                writegeneral.writeDBvalue(self.runfb, 1, 'S7WLBit')
            else:
                writegeneral.writeDBvalue(self.runfb, 0, 'S7WLBit')


            if self.lengthspvalue <= (self.lengthpvvalue +10) and self.startvalue == True and self.stopvalue == False :
                print("heheheehheheehheehehehehehehehehehehehehehehe")
                writegeneral.writeDBvalue(self.fb, 1, 'S7WLBit')

            if  self.resetvalue == True:
                writegeneral.writeDBvalue(self.fb, 0, 'S7WLBit')
                writegeneral.writeDBvalue(self.lengthpv, 0, 'S7WLWord')
                writegeneral.writeDBvalue(self.speedpv, 0, 'S7WLWord')

            if self.lengthspvalue == 0:
                writegeneral.writeDBvalue(self.lengthpv, 0, 'S7WLWord')

            sta_con_plc.disconnect()

        except Exception as e:
            log_exception(e)
            level = logging.INFO
            messege = "Strand1" + ":" + " Exception rasied(process): " + str(e.args) + str(e)
            logger.log(level, messege)

