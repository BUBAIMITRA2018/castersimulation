from logger import *
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import logging
from event_V2 import *
logger = logging.getLogger("main.log")
__all__ = ['Fn_LTC1signal']


class Fn_LTC1signal(Eventmanager):

    def __init__(self,filename ):

        self.filename = filename
        self.devicename = "LTC1"
        self.setup()
        self.initilizedigitalinput()
        super().__init__(lambda: self.digitalprocess())

    def setup(self):

        try:

            self.MainPowerSupplyMccbFault = str(25800)
            self.AuxPowerMpcb415VAcFault = str(25801)
            self.ControlSupplyMpcb415VAcFault = str(25802)
            self.ControlSupplyForContactorsMpcb110VAcFault = str(25803)
            self.UpsSupplyFault = str(25804)
            self.InputContactorSwitchedOn = str(25805)
            self.OutputContactorSwitchedOn = str(25806)
            self.BypassForwardContactorOn = str(25807)
            self.BypassReverseContactorOn = str(25808)
            self.Motor1ContactorSwitchedOn = str(25809)
            self.Motor2ContactorSwitchedOn = str(25810)
            self.Motor1BrakeMpcbFault = str(25811)
            self.Motor1BrakeContactorSwitchedOn = str(25812)
            self.Motor2BrakeContactorSwitchedOn = str(25813)
            self.Motor1MpcbFault = str(25814)
            self.Motor2MpcbFault = str(25815)


            self.InputContactorcmd = str(26224)
            self.OutputContactorcmd = str(26225)
            self.BypassForwardcmd = str(26226)
            self.BypassReversecmd = str(26227)
            self.BrakeControlcmd = str(26228)
            self.Motor1Contactorcmd = str(26229)
            self.Motor2Contactorcmd = str(26230)

            self.encoderreading = str(25000)

            self.Ltc1EastParkOvrtrPosFb = str(25569)
            self.Ltc1EastParkPosFb = str(25570)
            self.Ltc1LdlLoadPosFb = str(25571)
            self.Ltc1RhLoadPosFb = str(25572)
            self.Ltc1CarIntlk1PosFb = str(25573)
            self.Ltc1CarIntlk2PosFb= str(25574)
            self.Ltc1RhTreat1PosFb = str(25575)
            self.Ltc1RhTreat2PosFb = str(25576)
            self.Ltc1WfWestPark1PosFb = str(25575)
            self.Ltc1WfWestPark2PosFb = str(25576)


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

        if (encodervalue >= 2000 and encodervalue <= 2005) :
            writegeneral.writesymbolvalue(self.Ltc1LdlLoadPosFb, 'digital', 1)

        if (encodervalue >= 2000 and encodervalue <= 2005):
            writegeneral.writesymbolvalue(self.Ltc1RhLoadPosFb, 'digital', 1)

        if (encodervalue >= 2000 and encodervalue <= 2005):
            writegeneral.writesymbolvalue(self.Ltc1CarIntlk1PosFb, 'digital', 1)

        if (encodervalue >= 2000 and encodervalue <= 2005):
            writegeneral.writesymbolvalue(self.Ltc1CarIntlk2PosFb, 'digital', 1)

        if (encodervalue >= 2000 and encodervalue <= 2005):
            writegeneral.writesymbolvalue(self.Ltc1RhTreat1PosFb, 'digital', 1)

        if (encodervalue >= 2000 and encodervalue <= 2005):
            writegeneral.writesymbolvalue(self.Ltc1RhTreat2PosFb, 'digital', 1)


        if (encodervalue >= 2000 and encodervalue <= 2005):
            writegeneral.writesymbolvalue(self.Ltc1WfWestPark1PosFb, 'digital', 1)

        if (encodervalue >= 2000 and encodervalue <= 2005):
            writegeneral.writesymbolvalue(self.Ltc1WfWestPark2PosFb, 'digital', 1)



        sta_con_plc.close()



