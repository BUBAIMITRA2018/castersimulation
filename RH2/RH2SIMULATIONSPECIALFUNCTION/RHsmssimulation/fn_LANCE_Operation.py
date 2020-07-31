from logger import *
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import logging
logger = logging.getLogger("main.log")
__all__ = ['Fn_LANCEsignal']


class Fn_LANCEsignal():

    def __init__(self, filename ):


        self.filename = filename
        self.devicename = "Lance"
        self.setup()
        self.initilizedigitalinput()


    def setup(self):

        try:
            self.MainPowerSupplyMccbFault = str(25884)
            self.ControlSupplyMpcb415VAcFault = str(25885)
            self.ControlSupplyForContactorsMpcb110VAcFault = str(25887)
            self.UpsSupplyFault = str(25886)
            self.IncommerMccb = str(25888)
            self.InputContactorSwitchedOn = str(25889)
            self.OutputContactorSwitchedOn = str(25890)
            self.BrakeMbcbOn = str(25892)
            self.BrakeContactorSwitchedOn = str(25893)
            self.Motor1TemparatureAlarm = str(25894)
            self.Motor1TemparatureFault = str(25895)
            self.DriveZeroSpeed = str(25891)
            self.maindrivespeedfb = str(25301)
            self.standbydrivespeedfb = str(25311)
            self.encodertag  = str(25280)
            self.SimMFLSlewPos = str()

            self.mflhoistultopposition =str(25588)
            self.mflhoisttopposition = str(25589)
            self.mflhoistambushposition = str(25590)
            self.mflhoistbottomposition = str(25591)
            self.mflhoistulbottomposition = str(25592)
            self.mflparkpositionovertravel = str(25593)
            self.mflparkposition = str(25594)
            self.mflhotofftakeposition = str(25595)
            self.mflhotoffovertakeposition = str(25596)



            self.Ltc1InputCommand = str(26256)
            self.Ltc1OutputCommand = str(26257)
            self.Ltc1BreakOnCommand = str(26258)


        except Exception as e:
                level = logging.ERROR
                messege = "FN_Lance" + self.devicename + " Error messege(setup)" + str(e.args)
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
            writegeneral.writesymbolvalue(self.UpsSupplyFault, 'digital', 1)
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


        self.encodertagvalue =  readgeneral.readsymbolvalue(self.encodertag, "analog")
        # self.slewpositionvalue = readgeneral.readsymbolvalue(self.SimMFLSlewPos, "analog")
        #
        # if(self.slewpositionvalue <= 1000):
        #     writegeneral.writesymbolvalue(self.mflparkpositionovertravel, 'digital', 1)
        # else:
        #     writegeneral.writesymbolvalue(self.mflparkpositionovertravel, 'digital', 0)
        #
        # if (self.slewpositionvalue > 1000) and (self.slewpositionvalue < 2000):
        #
        #     writegeneral.writesymbolvalue(self.mflparkposition, 'digital', 1)
        # else:
        #     writegeneral.writesymbolvalue(self.mflparkposition, 'digital', 0)
        #
        # if (self.slewpositionvalue >= 8000) and (self.slewpositionvalue < 9000):
        #
        #     writegeneral.writesymbolvalue(self.mflhotofftakeposition, 'digital', 1)
        # else:
        #     writegeneral.writesymbolvalue(self.mflhotofftakeposition, 'digital', 0)
        #
        # if (self.slewpositionvalue >= 9000):
        #
        #     writegeneral.writesymbolvalue(self.mflhotoffovertakeposition, 'digital', 1)
        # else:
        #     writegeneral.writesymbolvalue(self.mflhotoffovertakeposition, 'digital', 0)

        if (self.encodertagvalue <= 100):
            writegeneral.writesymbolvalue(self.mflhoistultopposition, 'digital', 1)
        else:
            writegeneral.writesymbolvalue(self.mflhoistultopposition, 'digital', 0)


        if (self.encodertagvalue > 150) and (self.encodertagvalue < 250) :
            writegeneral.writesymbolvalue(self.mflhoisttopposition, 'digital', 1)
        else:
            writegeneral.writesymbolvalue(self.mflhoisttopposition, 'digital', 0)


        if (self.encodertagvalue > 450) and (self.encodertagvalue < 550) :
            writegeneral.writesymbolvalue(self.mflhoistambushposition, 'digital', 1)
        else:
            writegeneral.writesymbolvalue(self.mflhoistambushposition, 'digital', 0)

        if (self.encodertagvalue > 2950) and (self.encodertagvalue < 3050):
            writegeneral.writesymbolvalue(self.mflhoistbottomposition, 'digital', 1)
        else:
            writegeneral.writesymbolvalue(self.mflhoistbottomposition, 'digital', 0)

        if (self.encodertagvalue >= 3100):
            writegeneral.writesymbolvalue(self.mflhoistulbottomposition, 'digital', 1)
        else:
            writegeneral.writesymbolvalue(self.mflhoistulbottomposition, 'digital', 0)



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


