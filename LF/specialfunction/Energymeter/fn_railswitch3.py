from logger import *
from event_V2 import *
from time import sleep
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import logging
import  general

logger = logging.getLogger("main.log")

__all__ = ['Fn_RailSwitch3']


class Fn_RailSwitch3(Eventmanager):



    def __init__(self,filename):
        self.filename = filename
        self.count = 0
        self._fwdlimitswtvalue = False
        self._revlimitswtvalue = False
        # self._fwdrunFBvalue = False
        # self._revrunFBvalue = False
        self.setup()
        self.initilizedigitalinput()
        super().__init__(lambda: self.process())

    def setup(self):
        try:

            self.ele1lift = str(434.4)
            self.ele2lift = str(434.7)
            self.ele3lift = str(435.2)
            self.ele1auto = str(434.6)
            self.ele2auto = str(435.1)
            self.ele3auto = str(435.4)
            self.ele1down = str(434.5)
            self.ele2down = str(435.0)
            self.ele3down = str(435.3)
            self.ele1liftfb = str(602.0)
            self.ele2liftfb = str(602.3)
            self.ele3liftfb = str(602.6)
            self.ele1downfb = str(602.1)
            self.ele2downfb = str(602.4)
            self.ele3downfb = str(602.7)




        except Exception as e:
            level = logging.ERROR
            messege = "FN_MOTOR2D" + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)

    def initilizedigitalinput(self):
       pass
    def process(self):
        print("iwas here in fyction2")


        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)
            self.ele1liftvalue = readgeneral.readsymbolvalue(self.ele1lift, 'S7WLBit', "PA")
            self.ele2liftvalue = readgeneral.readsymbolvalue(self.ele2lift, 'S7WLBit', "PA")
            self.ele3liftvalue = readgeneral.readsymbolvalue(self.ele3lift, 'S7WLBit', "PA")
            self.ele1autovalue = readgeneral.readsymbolvalue(self.ele1auto, 'S7WLBit', "PA")
            self.ele2autovalue = readgeneral.readsymbolvalue(self.ele2auto, 'S7WLBit', "PA")
            self.ele3autovalue = readgeneral.readsymbolvalue(self.ele3auto, 'S7WLBit', "PA")
            self.ele1downvalue = readgeneral.readsymbolvalue(self.ele1down, 'S7WLBit', "PA")
            self.ele2downvalue = readgeneral.readsymbolvalue(self.ele2down, 'S7WLBit', "PA")
            self.ele3downvalue = readgeneral.readsymbolvalue(self.ele3down, 'S7WLBit', "PA")

            if self.ele1downvalue == True or self.ele1autovalue == True:
                writegeneral.writesymbolvalue(self.ele1liftfb, 0, "S7WLBit")
                writegeneral.writesymbolvalue(self.ele1downfb, 1, "S7WLBit")


            if self.ele1liftvalue == True or self.ele1autovalue == False:
                writegeneral.writesymbolvalue(self.ele1downfb, 0, "S7WLBit")
                writegeneral.writesymbolvalue(self.ele1liftfb, 1, "S7WLBit")

            if self.ele2downvalue == True or self.ele2autovalue == True:
                writegeneral.writesymbolvalue(self.ele2liftfb, 0, "S7WLBit")
                writegeneral.writesymbolvalue(self.ele2downfb, 1, "S7WLBit")

            if self.ele2liftvalue == True or self.ele2autovalue == False:
                writegeneral.writesymbolvalue(self.ele2downfb, 0, "S7WLBit")
                writegeneral.writesymbolvalue(self.ele2liftfb, 1, "S7WLBit")

            if self.ele3downvalue == True or self.ele3autovalue == True:
                writegeneral.writesymbolvalue(self.ele3liftfb, 0, "S7WLBit")
                writegeneral.writesymbolvalue(self.ele3downfb, 1, "S7WLBit")

            if self.ele1liftvalue == True or self.ele1autovalue == False:
                writegeneral.writesymbolvalue(self.ele3downfb, 0, "S7WLBit")
                writegeneral.writesymbolvalue(self.ele3liftfb, 1, "S7WLBit")


            sta_con_plc.disconnect()

        except Exception as e:
            log_exception(e)
            level = logging.INFO
            messege = "Strand2" + ":" + " Exception rasied(process): " + str(e.args) + str(e)
            logger.log(level, messege)








