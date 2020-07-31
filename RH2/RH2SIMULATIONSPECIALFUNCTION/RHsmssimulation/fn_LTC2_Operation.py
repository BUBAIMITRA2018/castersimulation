from logger import *
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import time
import logging
from event_V2 import *
logger = logging.getLogger("main.log")
__all__ = ['Fn_LTC2signal']


class Fn_LTC2signal(Eventmanager):

    def __init__(self,filename ):
        self.filename = filename
        self.devicename = "LTC2"
        self.setup()
        self.initilizedigitalinput()
        super().__init__(lambda: self.process())

    def setup(self):

        try:
            self.MainPowerSupplyMccbFault = str(25840)
            self.DrivePowerSupplyMccbOn = str(25841)
            self.ControlSupplyMpcb415VAcFault = str(25842)
            self.ControlSupplyForContactorsMpcb110VAcFault = str(25843)
            self.UpsSupplyFault = str(25844)
            self.InputContactorSwitchedOn = str(25845)
            self.OutputContactorSwitchedOn = str(25846)
            self.Motor1MpcbOn = str(25847)
            self.Motor2MpcbOn = str(25848)
            self.Motor1ContactorSwitchedOn = str(25849)
            self.Motor2ContactorSwitchedOn = str(25850)
            self.BrakeMbcbOn = str(25851)
            self.BrakeContactorSwitchedOn = str(25852)
            self.Motor1TemparatureAlarm = str(25853)
            self.Motor1TemparatureFault = str(25854)
            self.Motor2TemparatureAlarm = str(25855)
            self.Motor2TemparatureFault = str(25856)
            self.DriveZeroSpeed = str(25857)
            self.Ltc2CrdRunFb = str(25672)
            self.Ltc2CrdHlthyFb = str(25673)
            self.Ltc2CrdCableSlackFb = str(25674)
            self.Ltc2CrdCableOvrTensionFb = str(25675)
            self.Ltc2CrdFwdRunningFb = str(25676)
            self.Ltc2CrdRevRunningFb = str(25677)
            self.Ltc2CrdPoxyRunningFb = str(25678)

            self.maindrivespeedfb = str(25341)
            self.standbydrivespeedfb = str(25351)
            self.Ltc2ParkOvrtrPosFb = str(25580)
            self.Ltc2ParkPosFb = str(25581)
            self.Ltc2ParkSlowPosFb = str(25582)
            self.Ltc2CarGunslowPosFb = str(25583)
            self.Ltc2CarGunPosFb= str(25584)
            self.Ltc2CarTreatmentslowPosFb = str(25585)
            self.Ltc2CarTreatmentPosFb = str(25586)
            self.Ltc2CarTreatmentoverPosFb = str(25587)
            self.positivecount = 0


            self.Ltc2InputCommand = str(26240)
            self.Ltc2OutputCommand = str(26241)
            self.Ltc2BreakOnCommand = str(26242)
            self.Ltc2Motor1ContractorOnCommand = str(26243)
            self.Ltc2Motor2ContractorOnCommand = str(26244)
            self.Ltc2CrdFwdCommand = str(25768)
            self.Ltc2CrdRevCommand = str(25769)



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

            writegeneral.writesymbolvalue(self.MainPowerSupplyMccbFault, 'digital', 1)
            writegeneral.writesymbolvalue(self.Motor1MpcbOn, 'digital', 1)
            writegeneral.writesymbolvalue(self.Motor2MpcbOn, 'digital', 1)

            writegeneral.writesymbolvalue(self.Ltc2CrdHlthyFb, 'digital', 1)
            writegeneral.writesymbolvalue(self.Ltc2CrdCableSlackFb, 'digital', 1)
            writegeneral.writesymbolvalue(self.Ltc2CrdCableOvrTensionFb, 'digital', 1)

            self.positivecount = 0

            sta_con_plc.close()


        except Exception as e:
            level = logging.ERROR
            messege = "Fn_Digitalsignal" + self.devicename + " Error messege(initilization)" + str(e.args)
            logger.log(level, messege)



    def process(self):
        client = Communication()
        sta_con_plc = client.opc_client_connect(self.filename)
        readgeneral = ReadGeneral(sta_con_plc)
        writegeneral = WriteGeneral(sta_con_plc)

        self.maindrivespeedfbvalue = readgeneral.readsymbolvalue(self.maindrivespeedfb, "analog")
        self.standbydrivespeedfbvalue = readgeneral.readsymbolvalue(self.standbydrivespeedfb, "analog")

        InputContactorcmdvalue = readgeneral.readsymbolvalue(self.Ltc2InputCommand, "digital")
        OutputContactorcmdvalue = readgeneral.readsymbolvalue(self.Ltc2OutputCommand, "digital")
        BrakeControlcmdvalue = readgeneral.readsymbolvalue(self.Ltc2BreakOnCommand, "digital")
        Motor1Contactorcmdvalue = readgeneral.readsymbolvalue(self.Ltc2Motor1ContractorOnCommand, "digital")
        Motor2Contactorcmdvalue = readgeneral.readsymbolvalue(self.Ltc2Motor2ContractorOnCommand, "digital")
        self.Ltc2CrdCableFwdCmdValue = readgeneral.readsymbolvalue(self.Ltc2CrdFwdCommand, "digital")
        self.Ltc2CrdCableRevCmdValue = readgeneral.readsymbolvalue(self.Ltc2CrdRevCommand, "digital")

        writegeneral.writesymbolvalue(self.InputContactorSwitchedOn, 'digital', InputContactorcmdvalue)
        writegeneral.writesymbolvalue(self.OutputContactorSwitchedOn, 'digital', OutputContactorcmdvalue)
        writegeneral.writesymbolvalue(self.BrakeContactorSwitchedOn, 'digital', BrakeControlcmdvalue)
        writegeneral.writesymbolvalue(self.Motor1ContactorSwitchedOn, 'digital', Motor1Contactorcmdvalue)
        writegeneral.writesymbolvalue(self.Motor2ContactorSwitchedOn, 'digital', Motor2Contactorcmdvalue)
        writegeneral.writesymbolvalue(self.Ltc2CrdFwdRunningFb, 'digital', self.Ltc2CrdCableFwdCmdValue)
        writegeneral.writesymbolvalue(self.Ltc2CrdRevRunningFb, 'digital', self.Ltc2CrdCableRevCmdValue)

        self.maindrivespeedfbvalue = readgeneral.readsymbolvalue(self.maindrivespeedfb, "analog")
        self.standbydrivespeedfbvalue = readgeneral.readsymbolvalue(self.standbydrivespeedfb, "analog")

        self.Ltc2CrdRunFbvalue = readgeneral.readsymbolvalue(self.Ltc2CrdFwdRunningFb,
                                                             "digital") or readgeneral.readsymbolvalue( self.Ltc2CrdRevRunningFb, "digital")

        writegeneral.writesymbolvalue(self.Ltc2CrdRunFb, 'digital', self.Ltc2CrdRunFbvalue)
        writegeneral.writesymbolvalue(self.Ltc2CrdPoxyRunningFb, 'digital', self.Ltc2CrdRunFbvalue)

        if self.maindrivespeedfbvalue != 0:
            writegeneral.writesymbolvalue(self.DriveZeroSpeed, 'digital', 1)

        else:
            writegeneral.writesymbolvalue(self.DriveZeroSpeed, 'digital', 0)

        cond1 = self.maindrivespeedfbvalue > 0 or self.standbydrivespeedfbvalue > 0

        if cond1:

            if self.positivecount == 0:
                writegeneral.writesymbolvalue(self.Ltc2ParkOvrtrPosFb, 'digital', 1)
                self.positivecount = self.positivecount + 1

            if self.positivecount == 1:
                writegeneral.writesymbolvalue(self.Ltc2ParkOvrtrPosFb, 'digital', 0)
                time.sleep(5)
                writegeneral.writesymbolvalue(self.Ltc2ParkPosFb, 'digital', 1)
                self.positivecount = self.positivecount + 1

            if self.positivecount == 2:
                writegeneral.writesymbolvalue(self.Ltc2ParkPosFb, 'digital', 0)
                time.sleep(5)
                writegeneral.writesymbolvalue(self.Ltc2ParkSlowPosFb, 'digital', 1)
                self.positivecount = self.positivecount + 1

            if self.positivecount == 3:
                writegeneral.writesymbolvalue(self.Ltc2ParkSlowPosFb, 'digital', 0)
                time.sleep(10)
                writegeneral.writesymbolvalue(self.Ltc2CarGunslowPosFb, 'digital', 1)
                self.positivecount = self.positivecount + 1

            if self.positivecount == 4:
                writegeneral.writesymbolvalue(self.Ltc2CarGunslowPosFb, 'digital', 0)
                time.sleep(5)
                writegeneral.writesymbolvalue(self.Ltc2CarGunPosFb, 'digital', 1)
                self.positivecount = self.positivecount + 1

            if self.positivecount == 5:
                writegeneral.writesymbolvalue(self.Ltc2CarGunPosFb, 'digital', 0)
                time.sleep(5)
                writegeneral.writesymbolvalue(self.Ltc2CarTreatmentslowPosFb, 'digital', 1)
                self.positivecount = self.positivecount + 1

            if self.positivecount == 6:
                writegeneral.writesymbolvalue(self.Ltc2CarTreatmentslowPosFb, 'digital', 0)
                time.sleep(8)
                writegeneral.writesymbolvalue(self.Ltc2CarTreatmentPosFb, 'digital', 1)
                self.positivecount = self.positivecount + 1

            if self.positivecount == 7:
                writegeneral.writesymbolvalue(self.Ltc2CarTreatmentPosFb, 'digital', 0)
                time.sleep(5)
                writegeneral.writesymbolvalue(self.Ltc2CarTreatmentoverPosFb, 'digital', 1)

        cond2 = self.maindrivespeedfbvalue < 0 or self.standbydrivespeedfbvalue < 0

        if cond2:
            writegeneral.writesymbolvalue(self.Ltc2ParkPosFb, 'digital', 0)
            if self.positivecount == 0:
                time.sleep(5)
                writegeneral.writesymbolvalue(self.Ltc2ParkOvrtrPosFb, 'digital', 1)

            if self.positivecount == 1:
                writegeneral.writesymbolvalue(self.Ltc2ParkSlowPosFb, 'digital', 0)
                time.sleep(5)
                writegeneral.writesymbolvalue(self.Ltc2ParkPosFb, 'digital', 1)
                self.positivecount = self.positivecount - 1

            if self.positivecount == 2:
                writegeneral.writesymbolvalue(self.Ltc2CarGunslowPosFb, 'digital', 0)
                time.sleep(8)
                writegeneral.writesymbolvalue(self.Ltc2ParkSlowPosFb, 'digital', 1)
                self.positivecount = self.positivecount - 1

            if self.positivecount == 3:
                writegeneral.writesymbolvalue(self.Ltc2CarGunPosFb, 'digital', 0)
                time.sleep(5)
                writegeneral.writesymbolvalue(self.Ltc2CarGunslowPosFb, 'digital', 1)
                self.positivecount = self.positivecount - 1

            if self.positivecount == 4:
                writegeneral.writesymbolvalue(self.Ltc2CarTreatmentslowPosFb, 'digital', 0)
                time.sleep(10)
                writegeneral.writesymbolvalue(self.Ltc2CarGunPosFb, 'digital', 1)
                self.positivecount = self.positivecount - 1

            if self.positivecount == 5:
                writegeneral.writesymbolvalue(self.Ltc2CarTreatmentPosFb, 'digital', 0)
                time.sleep(5)
                writegeneral.writesymbolvalue(self.Ltc2CarTreatmentslowPosFb, 'digital', 1)
                self.positivecount = self.positivecount - 1

            if self.positivecount == 6:
                writegeneral.writesymbolvalue(self.Ltc2CarTreatmentoverPosFb, 'digital', 0)
                time.sleep(5)
                writegeneral.writesymbolvalue(self.Ltc2CarTreatmentPosFb, 'digital', 1)
                self.positivecount = self.positivecount - 1

            if self.positivecount == 7:

                writegeneral.writesymbolvalue(self.Ltc2CarTreatmentoverPosFb, 'digital', 1)




        sta_con_plc.close()



