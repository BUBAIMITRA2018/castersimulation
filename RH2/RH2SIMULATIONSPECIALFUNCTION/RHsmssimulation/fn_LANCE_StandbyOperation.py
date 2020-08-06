from logger import *
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import logging
from event_V2 import *
import gc
logger = logging.getLogger("main.log")
__all__ = ['Fn_LanceStandbysignal']


class Fn_LanceStandbysignal():

    def __init__(self,filename ):

        self.filename = filename
        self.devicename = "Lance Standby"
        self.setup()
        self.initilizedigitalinput()


    def setup(self):

        try:

            self.MainPowerSupplyMccbFault = str(25904)
            self.ControlSupplyMpcb415VAcFault = str(25905)
            self.ControlSupplyForContactorsMpcb110VAcFault = str(25906)
            self.IncommerMccb = str(25907)
            self.InputContactorSwitchedOn = str(25908)
            self.OutputContactorSwitchedOn = str(25909)
            self.BrakeMbcbOn = str(25911)
            self.BrakeContactorSwitchedOn = str(25912)
            self.Motor1TemparatureAlarm = str(25913)
            self.Motor1TemparatureFault = str(25914)
            self.DriveZeroSpeed = str(25910)
            self.maindrivespeedfb = str(25301)
            self.standbydrivespeedfb = str(25311)
            self.Ltc1CrdHlyFb = str()

            self.Ltc1InputCommand = str(26260)
            self.Ltc1OutputCommand = str(26261)
            self.Ltc1BreakOnCommand = str(26262)




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
            writegeneral.writesymbolvalue(self.ControlSupplyMpcb415VAcFault, 'digital', 1)
            writegeneral.writesymbolvalue(self.ControlSupplyForContactorsMpcb110VAcFault, 'digital', 1)
            writegeneral.writesymbolvalue(self.IncommerMccb, 'digital', 1)
            writegeneral.writesymbolvalue(self.BrakeMbcbOn, 'digital', 1)


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

        InputContactorcmdvalue = readgeneral.readsymbolvalue(self.Ltc1InputCommand, "digital")
        OutputContactorcmdvalue = readgeneral.readsymbolvalue(self.Ltc1OutputCommand, "digital")
        BrakeControlcmdvalue = readgeneral.readsymbolvalue(self.Ltc1BreakOnCommand, "digital")

        writegeneral.writesymbolvalue(self.InputContactorSwitchedOn, 'digital', InputContactorcmdvalue)
        writegeneral.writesymbolvalue(self.OutputContactorSwitchedOn, 'digital', OutputContactorcmdvalue)
        writegeneral.writesymbolvalue(self.BrakeContactorSwitchedOn, 'digital', BrakeControlcmdvalue)

        self.maindrivespeedfbvalue = readgeneral.readsymbolvalue(self.maindrivespeedfb, "analog")
        self.standbydrivespeedfbvalue = readgeneral.readsymbolvalue(self.standbydrivespeedfb, "analog")

        if self.maindrivespeedfbvalue != 0:
            writegeneral.writesymbolvalue(self.DriveZeroSpeed, 'digital', 1)

        else:
            writegeneral.writesymbolvalue(self.DriveZeroSpeed, 'digital', 0)


        sta_con_plc.close()
        gc.collect()




