from logger import *
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
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
            self.AuxPowerMpcb415VAcFault = str(25841)
            self.ControlSupplyMpcb415VAcFault = str(25842)
            self.ControlSupplyForContactorsMpcb110VAcFault = str(25843)
            self.UpsSupplyFault = str(25844)
            self.InputContactorSwitchedOn = str(25845)
            self.OutputContactorSwitchedOn = str(25846)
            self.BypassForwardContactorOn = str(25847)
            self.BypassReverseContactorOn = str(25848)
            self.Motor1ContactorSwitchedOn = str(25849)
            self.Motor2ContactorSwitchedOn = str(25850)
            self.Motor1BrakeMpcbFault = str(25851)
            self.Motor1BrakeContactorSwitchedOn = str(25852)
            self.Motor2BrakeContactorSwitchedOn = str(25853)
            self.Motor1MpcbFault = str(25854)
            self.Motor2MpcbFault = str(25855)


            self.InputContactorcmd = str(26240)
            self.OutputContactorcmd = str(26241)
            self.BypassForwardcmd = str(26242)
            self.BypassReversecmd = str(26243)
            self.BrakeControlcmd = str(26244)
            self.Motor1Contactorcmd = str(26245)
            self.Motor2Contactorcmd = str(26246)

            self.encoderreading = str(25000)

            self.Ltc1EastParkOvrtrPosFb = str(25580)
            self.Ltc1EastParkPosFb = str(25581)
            self.Ltc1CarIntlk1PosFb = str(25582)
            self.Ltc1CarIntlk2PosFb= str(25583)
            self.Ltc1RhTreat1PosFb = str(25584)
            self.Ltc1RhTreat2PosFb = str(25585)



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

        if (encodervalue >= 2000 and encodervalue <= 2005) :
            writegeneral.writesymbolvalue(self.Ltc1EastParkOvrtrPosFb, 'digital', 1)

        if (encodervalue >= 2000 and encodervalue <= 2005) :
            writegeneral.writesymbolvalue(self.Ltc1EastParkPosFb, 'digital', 1)



        if (encodervalue >= 2000 and encodervalue <= 2005):
            writegeneral.writesymbolvalue(self.Ltc1CarIntlk1PosFb, 'digital', 1)

        if (encodervalue >= 2000 and encodervalue <= 2005):
            writegeneral.writesymbolvalue(self.Ltc1CarIntlk2PosFb, 'digital', 1)

        if (encodervalue >= 2000 and encodervalue <= 2005):
            writegeneral.writesymbolvalue(self.Ltc1RhTreat1PosFb, 'digital', 1)

        if (encodervalue >= 2000 and encodervalue <= 2005):
            writegeneral.writesymbolvalue(self.Ltc1RhTreat2PosFb, 'digital', 1)

        sta_con_plc.close()



