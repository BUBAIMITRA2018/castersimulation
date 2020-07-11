from logger import *
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import logging
from event_V2 import *
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

            self.MainPowerSupplyMccbFault = str(25864)
            self.AuxPowerMpcb415VAcFault = str(25865)
            self.ControlSupplyMpcb415VAcFault = str(25866)
            self.ControlSupplyForContactorsMpcb110VAcFault = str(25867)
            self.UpsSupplyFault = str(25868)
            self.InputContactorSwitchedOn = str(25869)
            self.OutputContactorSwitchedOn = str(25870)
            self.BypassForwardContactorOn = str(25871)
            self.BypassReverseContactorOn = str(25872)
            self.Motor1ContactorSwitchedOn = str(25873)
            self.Motor2ContactorSwitchedOn = str(25874)
            self.Motor1BrakeMpcbFault = str(25875)
            self.Motor1BrakeContactorSwitchedOn = str(25876)
            self.Motor2BrakeContactorSwitchedOn = str(25877)
            self.Motor1MpcbFault = str(25878)
            self.Motor2MpcbFault = str(25879)


            self.InputContactorcmd = str(26248)
            self.OutputContactorcmd = str(26249)
            self.BypassForwardcmd = str(26250)
            self.BypassReversecmd = str(26251)
            self.BrakeControlcmd = str(26252)
            self.Motor1Contactorcmd = str(26253)
            self.Motor2Contactorcmd = str(26254)

            self.encoderreading = str(25000)



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
            writegeneral.writesymbolvalue(self.Motor1MpcbFault, 'digital', 0)
            writegeneral.writesymbolvalue(self.Motor2MpcbFault, 'digital', 0)
            writegeneral.writesymbolvalue(self.Motor1BrakeMpcbFault, 'digital', 0)
            writegeneral.writesymbolvalue(self.AuxPowerMpcb415VAcFault, 'digital', 0)
            writegeneral.writesymbolvalue(self.ControlSupplyForContactorsMpcb110VAcFault, 'digital', 0)
            writegeneral.writesymbolvalue(self.ControlSupplyMpcb415VAcFault, 'digital', 0)
            writegeneral.writesymbolvalue(self.UpsSupplyFault, 'digital', 0)
            writegeneral.writesymbolvalue(self.Motor1MpcbFault, 'digital', 0)
            writegeneral.writesymbolvalue(self.Motor2MpcbFault, 'digital', 0)

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
        BypassForwardcmd =readgeneral.readsymbolvalue(self.BypassForwardcmd,"digital")
        BypassReversecmd = readgeneral.readsymbolvalue(self.BypassReversecmd, "digital")
        BrakeControlcmd = readgeneral.readsymbolvalue(self.BrakeControlcmd, "digital")
        Motor1Contactorcmd = readgeneral.readsymbolvalue(self.Motor1Contactorcmd, "digital")
        Motor2Contactorcmd = readgeneral.readsymbolvalue(self.Motor1Contactorcmd, "digital")
        encodervalue = readgeneral.readsymbolvalue(self.encoderreading, "analog")

        if(InputContactorcmd):
            writegeneral.writesymbolvalue(self.InputContactorSwitchedOn, 'digital', 1)

        if (OutputContactorcmd):
            writegeneral.writesymbolvalue(self.OutputContactorSwitchedOn, 'digital', 1)

        if (BypassForwardcmd):
            writegeneral.writesymbolvalue(self.BypassForwardContactorOn, 'digital', 1)

        if (BypassReversecmd):
            writegeneral.writesymbolvalue(self.BypassReverseContactorOn, 'digital', 1)

        if (BrakeControlcmd):
            writegeneral.writesymbolvalue(self.Motor1BrakeContactorSwitchedOn, 'digital', 1)
            writegeneral.writesymbolvalue(self.Motor2BrakeContactorSwitchedOn, 'digital', 1)

        if (Motor1Contactorcmd):
            writegeneral.writesymbolvalue(self.Motor1ContactorSwitchedOn, 'digital', 1)

        if (Motor2Contactorcmd):
            writegeneral.writesymbolvalue(self.Motor2ContactorSwitchedOn, 'digital', 1)



        sta_con_plc.close()



