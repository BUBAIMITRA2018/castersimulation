from logger import *
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import logging
from event_V2 import *
logger = logging.getLogger("main.log")
__all__ = ['Fn_LANCEsignal']


class Fn_LANCEsignal(Eventmanager):

    def __init__(self, filename ):


        self.filename = filename
        self.devicename = "Lance"
        self.setup()
        self.initilizedigitalinput()
        super().__init__(lambda: self.digitalprocess())

    def setup(self):

        try:

            self.MainPowerSupplyMccbFault = str(25884)
            self.AuxPowerMpcb415VAcFault = str(25885)
            self.UpsSupplyFault = str(25886)
            self.DriveInputSupplyMccbFault =str(25587)
            self.HoistOverloadRelayTripped = str(25588)
            self.InputContactorSwitchedOn = str(25889)
            self.OutputContactorSwitchedOn = str(25890)
            self.BypassContactorSwitchedOn = str(25891)
            self.LanceHoistControlSupplyForContactorsMcb110VAcFault = str(25892)
            self.LanceHoistBrakeContactorSwitchedOn = str(25893)
            self.LanceHoistThermisterAlarm = str(25894)
            self.LanceHoistThermisterFault = str(25895)
            self.LanceHoistBrakeMpcbFault = str(25896)
            self.LanceHoistMainSupplyMccb415VAcFault = str(25897)


            self.InputContactorcmd = str(26256)
            self.OutputContactorcmd = str(26257)
            self.LanceHoistBypassContactorCmd = str(26258)
            self.LanceHoistBrakeContactorCmd = str(26259)
            self.LanceHoistBypassInputContactorcmd = str(26260)
            self.LanceHoistBypassOutputContactorcmd = str(26261)
            self.LanceHoistBypassBypassContactorcmd = str(26262)
            self. LanceHoistBypassBrakeContactorcmd = str(26262)

            self.encoderreading = str(25000)

            self.MflHoistUltTopPosFb = str(25588)
            self.MflHoistTopPosFb = str(25589)
            self.MflHoistAmbPosFb = str(25590)
            self.MflHoistBtmPosFb= str(25591)
            self.MflHoistUltBtmPosFb = str(25592)
            self.MflSlwParkOvrtrPosFb = str(25593)
            self.MflSlwParkPosFb = str(25594)
            self.MflSlwHotOfPosFb = str(25595)
            self.MflSlwHotOfOvrtrPosFb = str(25596)



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



    def digitalprocess(self):
        client = Communication()
        sta_con_plc = client.opc_client_connect(self.filename)
        readgeneral = ReadGeneral(sta_con_plc)
        writegeneral = WriteGeneral(sta_con_plc)

        InputContactorcmd =readgeneral.readsymbolvalue(self.InputContactorcmd,"digital")
        OutputContactorcmd = readgeneral.readsymbolvalue(self.OutputContactorcmd, "digital")
        LanceHoistBypassContactorCmd =readgeneral.readsymbolvalue(self.LanceHoistBypassContactorCmd,"digital")
        LanceHoistBrakeContactorCmd = readgeneral.readsymbolvalue(self.LanceHoistBrakeContactorCmd, "digital")

        encodervalue = readgeneral.readsymbolvalue(self.encoderreading, "analog")

        if(InputContactorcmd):
            writegeneral.writesymbolvalue(self.InputContactorSwitchedOn, 'digital', 1)

        if (OutputContactorcmd):
            writegeneral.writesymbolvalue(self.OutputContactorSwitchedOn, 'digital', 1)

        if (LanceHoistBypassContactorCmd):
            writegeneral.writesymbolvalue(self.BypassContactorSwitchedOn, 'digital', 1)

        if (LanceHoistBrakeContactorCmd):
            writegeneral.writesymbolvalue(self.LanceHoistBrakeContactorSwitchedOn, 'digital', 1)



        if (encodervalue >= 2000 and encodervalue <= 2005) :
            writegeneral.writesymbolvalue(self.MflHoistUltTopPosFb, 'digital', 1)

        if (encodervalue >= 2000 and encodervalue <= 2005) :
            writegeneral.writesymbolvalue(self.MflHoistTopPosFb, 'digital', 1)

        if (encodervalue >= 2000 and encodervalue <= 2005):
            writegeneral.writesymbolvalue(self.MflHoistAmbPosFb, 'digital', 1)

        if (encodervalue >= 2000 and encodervalue <= 2005):
            writegeneral.writesymbolvalue(self.MflHoistBtmPosFb, 'digital', 1)

        if (encodervalue >= 2000 and encodervalue <= 2005):
            writegeneral.writesymbolvalue(self.MflHoistUltBtmPosFb, 'digital', 1)

        if (encodervalue >= 2000 and encodervalue <= 2005):
            writegeneral.writesymbolvalue(self.MflSlwParkOvrtrPosFb, 'digital', 1)

        if (encodervalue >= 2000 and encodervalue <= 2005):
            writegeneral.writesymbolvalue(self.MflSlwParkPosFb, 'digital', 1)

        if (encodervalue >= 2000 and encodervalue <= 2005):
            writegeneral.writesymbolvalue(self.MflSlwHotOfPosFb, 'digital', 1)

        if (encodervalue >= 2000 and encodervalue <= 2005):
            writegeneral.writesymbolvalue(self.MflSlwHotOfOvrtrPosFb, 'digital', 1)



        sta_con_plc.close()


