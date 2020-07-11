from logger import *
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import logging
from event_V2 import *
logger = logging.getLogger("main.log")
__all__ = ['Fn_LTC1Standysignal']


class Fn_LTC1Standysignal(Eventmanager):

    def __init__(self, filename ):

        self.filename = filename
        self.devicename = "LTC1"
        self.setup()
        self.initilizedigitalinput()
        super().__init__(lambda: self.process())

    def setup(self):

        try:

            self.MainPowerSupplyMccbFault = str(25820)
            self.AuxPowerMpcb415VAcFault = str(25821)
            self.ControlSupplyMpcb415VAcFault = str(25822)
            self.ControlSupplyForContactorsMpcb110VAcFault = str(25823)
            self.UpsSupplyFault = str(25824)
            self.InputContactorSwitchedOn = str(25825)
            self.OutputContactorSwitchedOn = str(25826)
            self.BypassForwardContactorOn = str(25827)
            self.BypassReverseContactorOn = str(25828)
            self.Motor1ContactorSwitchedOn = str(25829)
            self.Motor2ContactorSwitchedOn = str(25830)
            self.Motor1BrakeMpcbFault = str(25831)
            self.Motor1BrakeContactorSwitchedOn = str(25832)
            self.Motor2BrakeContactorSwitchedOn = str(25833)
            self.Motor1MpcbFault = str(25834)
            self.Motor2MpcbFault = str(25835)


            self.InputContactorcmd = str(26232)
            self.OutputContactorcmd = str(26233)
            self.BypassForwardcmd = str(26234)
            self.BypassReversecmd = str(26235)
            self.BrakeControlcmd = str(26236)
            self.Motor1Contactorcmd = str(26237)
            self.Motor2Contactorcmd = str(26238)

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



    def readalltags(self):
        n = 3
        row, col = self.df.shape
        print(col)
        while n < col:
            data = self.df.iloc[self._idxNo, n]
            yield data, n
            n = n + 1

