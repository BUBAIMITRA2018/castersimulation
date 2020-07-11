from logger import *
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import logging
from event_V2 import *
logger = logging.getLogger("main.log")
__all__ = ['Fn_LanceStandbysignal']


class Fn_LanceStandbysignal(Eventmanager):

    def __init__(self,filename ):

        self.filename = filename
        self.devicename = "LTC1 STANDBY"
        self.setup()
        self.initilizedigitalinput()
        super().__init__(lambda: self.process())

    def setup(self):

        try:

            self.MainPowerSupplyMccbFault = str(25904)
            self.AuxPowerMpcb415VAcFault = str(25905)
            self.UpsSupplyFault = str(25906)
            self.DriveInputSupplyMccbFault =str(25907)
            self.HoistOverloadRelayTripped = str(25908)
            self.InputContactorSwitchedOn = str(25909)
            self.OutputContactorSwitchedOn = str(25910)
            self.BypassContactorSwitchedOn = str(25911)
            self.LanceHoistControlSupplyForContactorsMcb110VAcFault = str(25912)
            self.LanceHoistBrakeContactorSwitchedOn = str(25913)
            self.LanceHoistThermisterAlarm = str(25914)
            self.LanceHoistThermisterFault = str(25915)
            self.LanceHoistBrakeMpcbFault = str(25916)
            self.LanceHoistMainSupplyMccb415VAcFault = str(25917)


            self.InputContactorcmd = str(26256)
            self.OutputContactorcmd = str(26257)
            self.LanceHoistBypassContactorCmd = str(26258)
            self.LanceHoistBrakeContactorCmd = str(26259)
            self.LanceHoistBypassInputContactorcmd = str(26260)
            self.LanceHoistBypassOutputContactorcmd = str(26261)
            self.LanceHoistBypassBypassContactorcmd = str(26262)
            self. LanceHoistBypassBrakeContactorcmd = str(26262)





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

            writegeneral.writesymbolvalue(self.MainPowerSupplyMccbFault, 'digital', 0)
            writegeneral.writesymbolvalue(self.AuxPowerMpcb415VAcFault, 'digital', 0)
            writegeneral.writesymbolvalue(self.UpsSupplyFault, 'digital', 0)
            writegeneral.writesymbolvalue(self.HoistOverloadRelayTripped, 'digital', 0)
            writegeneral.writesymbolvalue(self.LanceHoistControlSupplyForContactorsMcb110VAcFault, 'digital', 0)
            writegeneral.writesymbolvalue(self.LanceHoistThermisterAlarm, 'digital', 0)
            writegeneral.writesymbolvalue(self.LanceHoistThermisterFault, 'digital', 0)
            writegeneral.writesymbolvalue(self.LanceHoistBrakeMpcbFault, 'digital', 0)
            writegeneral.writesymbolvalue(self.LanceHoistMainSupplyMccb415VAcFault, 'digital', 0)

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

        InputContactorcmd =readgeneral.readsymbolvalue(self.InputContactorcmd,"digital")
        OutputContactorcmd = readgeneral.readsymbolvalue(self.OutputContactorcmd, "digital")
        LanceHoistBypassContactorCmd =readgeneral.readsymbolvalue(self.LanceHoistBypassContactorCmd,"digital")
        LanceHoistBrakeContactorCmd = readgeneral.readsymbolvalue(self.LanceHoistBrakeContactorCmd, "digital")



        if(InputContactorcmd):
            writegeneral.writesymbolvalue(self.InputContactorSwitchedOn, 'digital', 1)

        if (OutputContactorcmd):
            writegeneral.writesymbolvalue(self.OutputContactorSwitchedOn, 'digital', 1)

        if (LanceHoistBypassContactorCmd):
            writegeneral.writesymbolvalue(self.BypassContactorSwitchedOn, 'digital', 1)

        if (LanceHoistBrakeContactorCmd):
            writegeneral.writesymbolvalue(self.LanceHoistBrakeContactorSwitchedOn, 'digital', 1)

        sta_con_plc.close()




