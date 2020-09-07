from logger import *
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import logging
import time
import gc
from event_V2 import *
logger = logging.getLogger("main.log")
__all__ = ['Fn_LTC1signal']


class Fn_LTC1signal():

    def __init__(self,filename ):
        self.filename = filename
        self.devicename = "LTC1"
        self.setup()
        self.initilizedigitalinput()


    def setup(self):

        try:
            self.MainPowerSupplyMccbFault = str(25800)
            self.DrivePowerSupplyMccbOn= str(25801)
            self.ControlSupplyMpcb415VAcFault = str(25802)
            self.ControlSupplyForContactorsMpcb110VAcFault = str(25803)
            self.UpsSupplyFault = str(25804)
            self.InputContactorSwitchedOn = str(25805)
            self.OutputContactorSwitchedOn = str(25806)
            self.Motor1MpcbOn = str(25807)
            self.Motor2MpcbOn = str(25808)
            self.Motor1ContactorSwitchedOn = str(25809)
            self.Motor2ContactorSwitchedOn = str(25810)
            self.BrakeMbcbOn = str(25811)
            self.BrakeContactorSwitchedOn = str(25812)
            self.Motor1TemparatureAlarm = str(25813)
            self.Motor1TemparatureFault = str(25814)
            self.Motor2TemparatureAlarm = str(25815)
            self.Motor2TemparatureFault = str(25816)
            self.DriveZeroSpeed= str(25817)
            self.Ltc1CrdRunFb = str(25600)
            self.Ltc1CrdHlthyFb = str(25601)
            self.Ltc1CrdCableSlackFb = str(25602)
            self.Ltc1CrdCableOvrTensionFb = str(25603)
            self.Ltc1CrdFwdRunningFb = str(25604)
            self.Ltc1CrdRevRunningFb = str(25605)
            self.Ltc1CrdPoxyRunningFb = str(25606)



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

            self.Ltc1InputCommand = str(26224)
            self.Ltc1OutputCommand = str(26225)
            self.Ltc1BreakOnCommand = str(26226)
            self.Ltc1Motor1ContractorOnCommand = str(26227)
            self.Ltc1Motor2ContractorOnCommand = str(26228)
            self.Ltc1CrdFwdCommand = str(25663)
            self.Ltc1CrdRevCommand = str(25664)









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
            writegeneral.writesymbolvalue(self.MainPowerSupplyMccbFault, 'digital', 0)
            writegeneral.writesymbolvalue(self.Motor1MpcbOn, 'digital', 1)
            writegeneral.writesymbolvalue(self.Motor2MpcbOn, 'digital', 1)
            writegeneral.writesymbolvalue(self.BrakeMbcbOn, 'digital', 1)
            writegeneral.writesymbolvalue(self.Ltc1CrdHlthyFb, 'digital', 1)
            writegeneral.writesymbolvalue(self.Ltc1CrdCableSlackFb, 'digital', 1)
            writegeneral.writesymbolvalue(self.Ltc1CrdCableOvrTensionFb, 'digital', 1)


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

        InputContactorcmdvalue =readgeneral.readsymbolvalue(self.Ltc1InputCommand,"digital")
        OutputContactorcmdvalue = readgeneral.readsymbolvalue(self.Ltc1OutputCommand, "digital")
        BrakeControlcmdvalue = readgeneral.readsymbolvalue(self.Ltc1BreakOnCommand, "digital")
        Motor1Contactorcmdvalue = readgeneral.readsymbolvalue(self.Ltc1Motor1ContractorOnCommand, "digital")
        Motor2Contactorcmdvalue = readgeneral.readsymbolvalue(self.Ltc1Motor2ContractorOnCommand, "digital")
        self.Ltc1CrdCableFwdCmdValue = readgeneral.readsymbolvalue(self.Ltc1CrdFwdCommand, "digital")
        self.Ltc1CrdCableRevCmdValue = readgeneral.readsymbolvalue(self.Ltc1CrdRevCommand, "digital")


        writegeneral.writesymbolvalue(self.InputContactorSwitchedOn, 'digital', InputContactorcmdvalue)
        writegeneral.writesymbolvalue(self.OutputContactorSwitchedOn, 'digital', OutputContactorcmdvalue)
        writegeneral.writesymbolvalue(self.BrakeContactorSwitchedOn, 'digital', BrakeControlcmdvalue)
        writegeneral.writesymbolvalue(self.Motor1ContactorSwitchedOn, 'digital', Motor1Contactorcmdvalue)
        writegeneral.writesymbolvalue(self.Motor2ContactorSwitchedOn, 'digital', Motor2Contactorcmdvalue)
        writegeneral.writesymbolvalue(self.Ltc1CrdFwdRunningFb, 'digital', self.Ltc1CrdCableFwdCmdValue)
        writegeneral.writesymbolvalue(self.Ltc1CrdRevRunningFb, 'digital', self.Ltc1CrdCableRevCmdValue)

        self.Ltc1CrdRunFbvalue = readgeneral.readsymbolvalue(self.Ltc1CrdFwdRunningFb, "digital") or readgeneral.readsymbolvalue(self.Ltc1CrdRevRunningFb, "digital")

        writegeneral.writesymbolvalue(self.Ltc1CrdRunFb, 'digital', self.Ltc1CrdRunFbvalue)
        writegeneral.writesymbolvalue(self.Ltc1CrdPoxyRunningFb, 'digital', self.Ltc1CrdRunFbvalue)

        self.maindrivespeedfbvalue = readgeneral.readsymbolvalue(self.maindrivespeedfb,"analog")
        self.standbydrivespeedfbvalue = readgeneral.readsymbolvalue(self.standbydrivespeedfb,"analog")


        if self.maindrivespeedfbvalue != 0:
            writegeneral.writesymbolvalue(self.DriveZeroSpeed, 'digital', 1)

        else:
            writegeneral.writesymbolvalue(self.DriveZeroSpeed, 'digital', 0)



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
        gc.collect()



