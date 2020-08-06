from logger import *
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import logging
from event_V2 import *
import gc
logger = logging.getLogger("main.log")
__all__ = ['Fn_LTC2Standbysignal']


class Fn_LTC2Standbysignal(Eventmanager):

    def __init__(self,filename ):

        self.filename = filename
        self.devicename = "LTC2"
        self.setup()
        self.initilizedigitalinput()
        super().__init__(lambda: self.process())

    def setup(self):

        try:

            self.DrivePowerSupplyMCCBOn = str(25868)
            self.InputContactorSwitchedOn = str(25869)
            self.OutputContactorSwitchedOn = str(25870)
            self.MotorBrakeMccbOn = str(25875)
            self.MotorBrakeContactorSwitchedOn = str(25876)
            self.DriveZeroSpeedFb = str(25877)

            self.InputContactorcmd = str(26248)
            self.OutputContactorcmd = str(26249)
            self.BrakeControlcmd = str(26250)
            self.standbydrivespeedfb = str(25351)






        except Exception as e:
            level = logging.ERROR
            messege = "FN_LTC2_Standby" + self.devicename + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)

    def initilizedigitalinput(self):
        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)

            writegeneral.writesymbolvalue(self.DrivePowerSupplyMCCBOn, 'digital', 1)

            writegeneral.writesymbolvalue(self.MotorBrakeMccbOn, 'digital', 1)



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

        InputContactorcmdValue = readgeneral.readsymbolvalue(self.InputContactorcmd, "digital")
        OutputContactorcmdValue = readgeneral.readsymbolvalue(self.OutputContactorcmd, "digital")
        BrakeControlcmdValue = readgeneral.readsymbolvalue(self.BrakeControlcmd, "digital")

        writegeneral.writesymbolvalue(self.InputContactorSwitchedOn, 'digital', InputContactorcmdValue)
        writegeneral.writesymbolvalue(self.OutputContactorSwitchedOn, 'digital', OutputContactorcmdValue)
        writegeneral.writesymbolvalue(self.MotorBrakeContactorSwitchedOn, 'digital', BrakeControlcmdValue)

        self.standbydrivespeedfbvalue = readgeneral.readsymbolvalue(self.standbydrivespeedfb, "analog")

        if self.standbydrivespeedfbvalue != 0:
            writegeneral.writesymbolvalue(self.DriveZeroSpeedFb, 'digital', 1)

        else:
            writegeneral.writesymbolvalue(self.DriveZeroSpeedFb, 'digital', 0)


        sta_con_plc.close()
        gc.collect()



