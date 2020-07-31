from logger import *
from event_V2 import *
from time import sleep
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import logging
import  general

logger = logging.getLogger("main.log")

__all__ = ['Fn_RailSwitch']


class Fn_RailSwitch(Eventmanager):



    def __init__(self,filename):
        self.filename = filename
        # self.count = 0
        self._fwdlimitswtvalue = False
        self._revlimitswtvalue = False

        self.setup()
        self.initilizedigitalinput()
        super().__init__(lambda: self.process())

    def setup(self):
        try:


                    self.drivecmdtag = str("db27.dbw380")
                    self.trackposition = str(210.5)
                    self.forwardendpoint = str(210.6)
                    self.reverseendpoint = str(210.7)
                    self.trackposition1 = str(211.2)
                    self.forwardendpoint1 = str(211.3)
                    self.reverseendpoint1 = str(211.4)
                    self.trackposition2 = str(211.7)
                    self.forwardendpoint2 = str(212.0)
                    self.reverseendpoint2 = str(212.1)
                    self.trackposition3 = str(212.4)
                    self.forwardendpoint3 = str(212.5)
                    self.reverseendpoint3 = str(212.6)
                    self.counter = str("db65.dbw16")
                    self.rdolcmd = str(211.1)
                    self.allhigh = str(13.2)
                    self.pos1 = str(209.3)
                    self.pos2 = str(209.5)
                    self.pos3 = str(209.7)
                    self.pos4 = str(210.1)
                    self.pos5 = str(210.3)
                    self.pos10 = str(209.4)
                    self.pos20 = str(209.6)
                    self.pos30 = str(210.0)
                    self.pos40 = str(210.2)
                    self.pos50 = str(210.4)
                    self.reset = str(59.7)

        except Exception as e:
            level = logging.ERROR
            messege = "FN_MOTOR2D" + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)



    def initilizedigitalinput(self):
        pass
        # client = Communication()
        # sta_con_plc = client.opc_client_connect(self.filename)
        # readgeneral = ReadGeneral(sta_con_plc)
        # writegeneral = WriteGeneral(sta_con_plc)
        # writegeneral.writesymbolvalue(self.trackposition, 0, 'S7WLBit')
        # writegeneral.writesymbolvalue(self.trackposition1, 0, 'S7WLBit')
        # writegeneral.writesymbolvalue(self.trackposition2, 0, 'S7WLBit')
        # writegeneral.writesymbolvalue(self.trackposition3, 0, 'S7WLBit')
        # writegeneral.writesymbolvalue(self.reverseendpoint, 0, 'S7WLBit')
        # writegeneral.writesymbolvalue(self.reverseendpoint1, 0, 'S7WLBit')
        # writegeneral.writesymbolvalue(self.reverseendpoint2, 0, 'S7WLBit')
        # writegeneral.writesymbolvalue(self.reverseendpoint3, 0, 'S7WLBit')
        # writegeneral.writesymbolvalue(self.forwardendpoint, 0, 'S7WLBit')
        # writegeneral.writesymbolvalue(self.forwardendpoint1, 0, 'S7WLBit')
        # writegeneral.writesymbolvalue(self.forwardendpoint2, 0, 'S7WLBit')
        # writegeneral.writesymbolvalue(self.forwardendpoint3, 0, 'S7WLBit')
        #
        # sta_con_plc.disconnect()



    def process(self):

        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)
            self.count = readgeneral.readDBvalue(self.counter, 'S7WLWord')

            self.drivecmdtagvalue = readgeneral.readDBvalue(self.drivecmdtag, 'S7WLWord')

            if self.drivecmdtagvalue == 15 and self.count != 5:
                sleep(5)
                writegeneral.writesymbolvalue(self.trackposition, 1, 'S7WLBit')
                writegeneral.writesymbolvalue(self.trackposition1, 1, 'S7WLBit')
                writegeneral.writesymbolvalue(self.trackposition2, 1, 'S7WLBit')
                writegeneral.writesymbolvalue(self.trackposition3, 1, 'S7WLBit')
                sleep(5)
                writegeneral.writesymbolvalue(self.trackposition, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.trackposition1, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.trackposition2, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.trackposition3, 0, 'S7WLBit')
                # self.count = self.count + 1

            if self.drivecmdtagvalue == 2063 and self.count != 0:
                sleep(5)
                writegeneral.writesymbolvalue(self.trackposition, 1, 'S7WLBit')
                writegeneral.writesymbolvalue(self.trackposition1, 1, 'S7WLBit')
                writegeneral.writesymbolvalue(self.trackposition2, 1, 'S7WLBit')
                writegeneral.writesymbolvalue(self.trackposition3, 1, 'S7WLBit')
                sleep(5)
                writegeneral.writesymbolvalue(self.trackposition, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.trackposition1, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.trackposition2, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.trackposition3, 0, 'S7WLBit')
                # self.count = self.count - 1

            if self.drivecmdtagvalue == 2063:
                writegeneral.writesymbolvalue(self.forwardendpoint, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.forwardendpoint1, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.forwardendpoint2, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.forwardendpoint3, 0, 'S7WLBit')

            if self.drivecmdtagvalue == 15:
                writegeneral.writesymbolvalue(self.reverseendpoint, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.reverseendpoint1, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.reverseendpoint2, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.reverseendpoint3, 0, 'S7WLBit')

            if self.count == 5:
                sleep(2)
                writegeneral.writesymbolvalue(self.forwardendpoint, 1, 'S7WLBit')
                writegeneral.writesymbolvalue(self.forwardendpoint1, 1, 'S7WLBit')
                writegeneral.writesymbolvalue(self.forwardendpoint2, 1, 'S7WLBit')
                writegeneral.writesymbolvalue(self.forwardendpoint3, 1, 'S7WLBit')

            if self.count == 1:
                sleep(2)
                writegeneral.writesymbolvalue(self.reverseendpoint, 1, 'S7WLBit')
                writegeneral.writesymbolvalue(self.reverseendpoint1, 1, 'S7WLBit')
                writegeneral.writesymbolvalue(self.reverseendpoint2, 1, 'S7WLBit')
                writegeneral.writesymbolvalue(self.reverseendpoint3, 1, 'S7WLBit')

            self.rdolcmdvalue = readgeneral.readsymbolvalue(self.rdolcmd, 'S7WLBit', "PE")

            if self.count == 1 and self.rdolcmdvalue == 1:
                writegeneral.writesymbolvalue(self.pos1, 1, 'S7WLBit')
                writegeneral.writesymbolvalue(self.pos10, 1, 'S7WLBit')

            if self.count == 2 and self.rdolcmdvalue == 1:
                writegeneral.writesymbolvalue(self.pos2, 1, 'S7WLBit')
                writegeneral.writesymbolvalue(self.pos20, 1, 'S7WLBit')

            if self.count == 3 and self.rdolcmdvalue == 1:
                writegeneral.writesymbolvalue(self.pos3, 1, 'S7WLBit')
                writegeneral.writesymbolvalue(self.pos30, 1, 'S7WLBit')

            if self.count == 4 and self.rdolcmdvalue == 1:
                writegeneral.writesymbolvalue(self.pos4, 1, 'S7WLBit')
                writegeneral.writesymbolvalue(self.pos40, 1, 'S7WLBit')

            if self.count == 5 and self.rdolcmdvalue == 1:
                writegeneral.writesymbolvalue(self.pos5, 1, 'S7WLBit')
                writegeneral.writesymbolvalue(self.pos50, 1, 'S7WLBit')

            self.resetval = readgeneral.readsymbolvalue(self.reset, 'S7WLBit', "PA")
            if self.resetval == 1:
                writegeneral.writesymbolvalue(self.pos1, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.pos2, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.pos3, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.pos4, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.pos5, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.pos10, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.pos20, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.pos30, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.pos40, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.pos50, 0, 'S7WLBit')




            sleep(1)

            sta_con_plc.disconnect()

        except Exception as e:
            log_exception(e)
            level = logging.INFO
            messege = "FN_RailSwitch1" + ":" + " Exception rasied(process): " + str(e.args) + str(e)
            logger.log(level, messege)








