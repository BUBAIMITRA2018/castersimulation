from logger import *
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import logging
import time
from event_V2 import *
logger = logging.getLogger("main.log")
__all__ = ['Fn_LTC1signal']


class Fn_LTC1signal(Eventmanager):

    def __init__(self,filename ):

        self.filename = filename
        self.devicename = "LTC1"
        self.setup()
        self.initilizedigitalinput()
        super().__init__(lambda: self.process())

    def setup(self):

        try:



            self.Ltc1OvrtrPosFb = str(25569)
            self.Ltc1ParkPosFb = str(25570)
            self.Ltc1ParkSlowPosFb = str(25571)
            self.Ltc1RhLoadPosFb = str(25572)
            self.Ltc1VslExgPosFb = str(25573)
            self.Ltc1DekurPosFb = str(25574)
            self.Ltc1TreatPosFb = str(25575)
            self.Ltc1TreatSlowPosFb = str(25576)
            self.Ltc1WireFBPosFb = str(25577)
            self.Ltc1WireOvrtrFBPosFb = str(25578)
            self.maindrivespeedfb = str(25321)
            self.standbydrivespeedfb = str(25331)
            self.positivecount = 0



        except Exception as e:
            level = logging.ERROR
            messege = "FN_LTC1" + self.devicename + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)

    def initilizedigitalinput(self):
        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)
            self.positivecount = 0
            writegeneral.writesymbolvalue(self.Ltc1OvrtrPosFb, 'digital', 0)
            writegeneral.writesymbolvalue(self.Ltc1ParkPosFb, 'digital', 0)
            writegeneral.writesymbolvalue(self.Ltc1ParkSlowPosFb, 'digital', 0)
            writegeneral.writesymbolvalue(self.Ltc1VslExgPosFb, 'digital', 0)
            writegeneral.writesymbolvalue(self.Ltc1DekurPosFb, 'digital', 0)
            writegeneral.writesymbolvalue(self.Ltc1TreatPosFb, 'digital', 0)
            writegeneral.writesymbolvalue(self.Ltc1TreatSlowPosFb, 'digital', 0)
            writegeneral.writesymbolvalue(self.Ltc1WireFBPosFb, 'digital', 0)
            writegeneral.writesymbolvalue(self.Ltc1WireOvrtrFBPosFb, 'digital', 0)






            # writegeneral.writesymbolvalue(self.MainPowerSupplyMccbFault, 'digital', 0)
            # writegeneral.writesymbolvalue(self.Motor1MpcbFault, 'digital', 0)
            # writegeneral.writesymbolvalue(self.Motor2MpcbFault, 'digital', 0)
            # writegeneral.writesymbolvalue(self.Mtr1MccbOn, 'digital', 1)
            # writegeneral.writesymbolvalue(self.Mtr2MccbOn, 'digital', 1)
            # writegeneral.writesymbolvalue(self.ControlSupplyForContactorsMpcb110VAcFault, 'digital', 0)
            # writegeneral.writesymbolvalue(self.ControlSupplyMpcb415VAcFault, 'digital', 0)
            # writegeneral.writesymbolvalue(self.UpsSupplyFault, 'digital', 0)
            # writegeneral.writesymbolvalue(self.Motor1MpcbFault, 'digital', 0)
            # writegeneral.writesymbolvalue(self.Motor2MpcbFault, 'digital', 0)
            # writegeneral.writesymbolvalue(self.MCBPOWERSUPPLYON, 'digital', 1)
            # writegeneral.writesymbolvalue(self.LTC1breakmpccbon, 'digital', 1)

            sta_con_plc.close()


        except Exception as e:
            level = logging.ERROR
            messege = "FN_LTC1" + self.devicename + " Error messege(initilization)" + str(e.args)
            logger.log(level, messege)



    def process(self):
        client = Communication()
        sta_con_plc = client.opc_client_connect(self.filename)
        readgeneral = ReadGeneral(sta_con_plc)
        writegeneral = WriteGeneral(sta_con_plc)

        self.maindrivespeedfbvalue = readgeneral.readsymbolvalue(self.maindrivespeedfb,"analog")
        self.standbydrivespeedfbvalue = readgeneral.readsymbolvalue(self.standbydrivespeedfb,"analog")
        # self.Ltc1OvrtrPosFbvalue = readgeneral.readsymbolvalue(self.Ltc1OvrtrPosFb,"digital")
        # self.Ltc1ParkPosFbvalue = readgeneral.readsymbolvalue(self.Ltc1ParkPosFb, "digital")
        # self.Ltc1ParkSlowPosFbvalue = readgeneral.readsymbolvalue(self.Ltc1ParkSlowPosFb, "digital")
        # self.Ltc1RhLoadPosFbvalue = readgeneral.readsymbolvalue(self.Ltc1RhLoadPosFb, "digital")
        # self.Ltc1VslExgPosFbvalue = readgeneral.readsymbolvalue(self.Ltc1VslExgPosFb, "digital")
        # self.Ltc1DekurPosFbvalue = readgeneral.readsymbolvalue(self.Ltc1DekurPosFb, "digital")
        # self.Ltc1DekurPosFbvalue = readgeneral.readsymbolvalue(self.Ltc1DekurPosFb, "digital")
        # self.Ltc1TreatPosFbvalue = readgeneral.readsymbolvalue(self.Ltc1TreatPosFb, "digital")
        # self.Ltc1TreatSlowPosFbvalue = readgeneral.readsymbolvalue(self.Ltc1TreatSlowPosFb, "digital")
        # self.Ltc1WireFBPosFbvalue = readgeneral.readsymbolvalue(self.Ltc1WireFBPosFb, "digital")
        # self.Ltc1WireOvrtrFBPosFbvalue = readgeneral.readsymbolvalue(self.Ltc1WireOvrtrFBPosFb, "digital")
        # self.Ltc1WireOvrtrFBPosFbvalue = readgeneral.readsymbolvalue(self.Ltc1WireOvrtrFBPosFb, "digital")

        cond1 = self.maindrivespeedfbvalue > 0 or self.standbydrivespeedfbvalue > 0


        if cond1 > 0:

            if self.positivecount == 0:

                writegeneral.writesymbolvalue(self.Ltc1OvrtrPosFb, 'digital', 1)
                self.positivecount = self.positivecount + 1

            if self.positivecount == 1 :
                writegeneral.writesymbolvalue(self.Ltc1OvrtrPosFb, 'digital', 0)
                time.sleep(5)
                writegeneral.writesymbolvalue(self.Ltc1ParkPosFb, 'digital', 1)

                self.positivecount = self.positivecount + 1

            if self.positivecount == 2 :
                time.sleep(5)
                writegeneral.writesymbolvalue(self.Ltc1ParkPosFb, 'digital', 0)
                writegeneral.writesymbolvalue(self.Ltc1ParkSlowPosFb, 'digital', 1)
                self.positivecount = self.positivecount + 1

            if self.positivecount == 3 :
                writegeneral.writesymbolvalue(self.Ltc1ParkSlowPosFb, 'digital', 0)
                time.sleep(8)
                writegeneral.writesymbolvalue(self.Ltc1RhLoadPosFb, 'digital', 1)
                self.positivecount = self.positivecount + 1

            if self.positivecount == 4:
                writegeneral.writesymbolvalue(self.Ltc1RhLoadPosFb, 'digital', 0)
                time.sleep(10)
                writegeneral.writesymbolvalue(self.Ltc1TreatSlowPosFb, 'digital', 1)
                self.positivecount = self.positivecount + 1

            if self.positivecount == 5:
                writegeneral.writesymbolvalue(self.Ltc1TreatSlowPosFb, 'digital', 0)
                time.sleep(5)
                writegeneral.writesymbolvalue(self.Ltc1TreatPosFb, 'digital', 1)
                self.positivecount = self.positivecount + 1

            if self.positivecount == 6:
                writegeneral.writesymbolvalue(self.Ltc1TreatPosFb, 'digital', 0)
                time.sleep(5)
                writegeneral.writesymbolvalue(self.Ltc1VslExgPosFb, 'digital', 1)
                self.positivecount = self.positivecount + 1

            if self.positivecount == 6:
                writegeneral.writesymbolvalue(self.Ltc1VslExgPosFb, 'digital', 0)
                time.sleep(10)
                writegeneral.writesymbolvalue(self.Ltc1DekurPosFb, 'digital', 1)
                self.positivecount = self.positivecount + 1

            if self.positivecount == 7:
                writegeneral.writesymbolvalue(self.Ltc1DekurPosFb, 'digital', 0)
                time.sleep(5)
                writegeneral.writesymbolvalue(self.Ltc1WireFBPosFb, 'digital', 1)
                self.positivecount = self.positivecount + 1

            if self.positivecount == 8:
                writegeneral.writesymbolvalue(self.Ltc1WireFBPosFb, 'digital', 0)
                time.sleep(5)
                writegeneral.writesymbolvalue(self.Ltc1WireOvrtrFBPosFb, 'digital', 1)

        cond2 = self.maindrivespeedfbvalue < 0 or self.standbydrivespeedfbvalue < 0


        if cond2 :

            if self.positivecount == 0:
                writegeneral.writesymbolvalue(self.Ltc1ParkPosFb, 'digital', 0)
                time.sleep(5)
                writegeneral.writesymbolvalue(self.Ltc1OvrtrPosFb, 'digital', 1)


            if self.positivecount == 1:
                writegeneral.writesymbolvalue(self.Ltc1ParkSlowPosFb, 'digital', 0)
                time.sleep(5)
                writegeneral.writesymbolvalue(self.Ltc1ParkPosFb, 'digital', 1)
                self.positivecount = self.positivecount - 1

            if self.positivecount == 2:
                writegeneral.writesymbolvalue(self.Ltc1RhLoadPosFb, 'digital', 0)
                time.sleep(5)
                writegeneral.writesymbolvalue(self.Ltc1ParkSlowPosFb, 'digital', 1)
                self.positivecount = self.positivecount - 1

            if self.positivecount == 3:
                writegeneral.writesymbolvalue(self.Ltc1TreatSlowPosFb, 'digital', 0)
                time.sleep(8)
                writegeneral.writesymbolvalue(self.Ltc1RhLoadPosFb, 'digital', 1)
                self.positivecount = self.positivecount - 1

            if self.positivecount == 4:
                writegeneral.writesymbolvalue(self.Ltc1TreatPosFb, 'digital', 0)
                time.sleep(10)
                writegeneral.writesymbolvalue(self.Ltc1TreatSlowPosFb, 'digital', 1)
                self.positivecount = self.positivecount - 1

            if self.positivecount == 5:
                writegeneral.writesymbolvalue(self.Ltc1VslExgPosFb, 'digital', 0)
                time.sleep(5)
                writegeneral.writesymbolvalue(self.Ltc1TreatPosFb, 'digital', 1)
                self.positivecount = self.positivecount - 1

            if self.positivecount == 6:
                writegeneral.writesymbolvalue(self.Ltc1DekurPosFb, 'digital', 0)
                time.sleep(5)
                writegeneral.writesymbolvalue(self.Ltc1VslExgPosFb, 'digital', 1)
                self.positivecount = self.positivecount - 1

            if self.positivecount == 6:
                writegeneral.writesymbolvalue(self.Ltc1WireFBPosFb, 'digital', 0)
                time.sleep(10)
                writegeneral.writesymbolvalue(self.Ltc1DekurPosFb, 'digital', 1)
                self.positivecount = self.positivecount - 1

            if self.positivecount == 7:
                writegeneral.writesymbolvalue(self.Ltc1WireOvrtrFBPosFb, 'digital', 0)
                time.sleep(5)
                writegeneral.writesymbolvalue(self.Ltc1WireFBPosFb, 'digital', 1)
                self.positivecount = self.positivecount - 1

            if self.positivecount == 8:
                writegeneral.writesymbolvalue(self.Ltc1WireOvrtrFBPosFb, 'digital', 1)
                self.positivecount = self.positivecount - 1

        sta_con_plc.close()



