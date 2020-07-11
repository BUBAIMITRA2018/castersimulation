from logger import *
from event_V2 import *
from time import sleep
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import logging
import  general

logger = logging.getLogger("main.log")

__all__ = ['Fn_RailSwitch6']


class Fn_RailSwitch6(Eventmanager):



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

            self.drivecmdtag = str("db27.dbw200")
            self.trackposition = str(81.0)
            self.forwardendpoint = str(81.1)
            self.reverseendpoint = str(81.2)
            self.trackposition1 = str(81.5)
            self.forwardendpoint1 = str(81.6)
            self.reverseendpoint1 = str(81.7)
            self.trackposition2 = str(82.2)
            self.forwardendpoint2 = str(82.3)
            self.reverseendpoint2 = str(82.4)
            self.trackposition3 = str(82.7)
            self.forwardendpoint3 = str(83.0)
            self.reverseendpoint3 = str(83.1)
            self.rdolcmd = str(81.3)
            self.allhigh = str(13.2)
            self.pos1 = str(79.0)
            self.pos2 = str(79.2)
            self.pos3 = str(79.4)
            self.pos4 = str(79.6)
            self.pos5 = str(80.0)
            self.pos6 = str(80.2)
            self.pos7 = str(80.4)
            self.counter = str("db65.dbw12")
            self.rdollowcmd = str(81.4)
            self.rollertable1 = str(80.6)


        except Exception as e:
            level = logging.ERROR
            messege = "FN_MOTOR2D" + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)

    def initilizedigitalinput(self):
        client = Communication()
        sta_con_plc = client.opc_client_connect(self.filename)
        readgeneral = ReadGeneral(sta_con_plc)
        writegeneral = WriteGeneral(sta_con_plc)
        writegeneral.writesymbolvalue(self.trackposition, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.trackposition1, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.trackposition2, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.trackposition3, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.reverseendpoint, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.reverseendpoint1, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.reverseendpoint2, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.reverseendpoint3, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.forwardendpoint, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.forwardendpoint1, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.forwardendpoint2, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.forwardendpoint3, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.pos1, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.pos2, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.pos3, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.pos4, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.pos5, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.pos6, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.pos7, 0, 'S7WLBit')
        sta_con_plc.disconnect()
        print("intiliased")
        pass

    def process(self):

        try:

            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)
            self.allhighvalue = readgeneral.readsymbolvalue(self.allhigh, 'S7WLBit', "PA")
            self.count = readgeneral.readDBvalue(self.counter, 'S7WLWord')

            self.drivecmdtagvalue = readgeneral.readDBvalue(self.drivecmdtag, 'S7WLWord')
            if self.allhighvalue == 1:
                writegeneral.writesymbolvalue(self.pos1, 1, 'S7WLBit')
                writegeneral.writesymbolvalue(self.pos2, 1, 'S7WLBit')
                writegeneral.writesymbolvalue(self.pos3, 1, 'S7WLBit')
                writegeneral.writesymbolvalue(self.pos4, 1, 'S7WLBit')
                writegeneral.writesymbolvalue(self.pos5, 1, 'S7WLBit')
                writegeneral.writesymbolvalue(self.pos6, 1, 'S7WLBit')
                writegeneral.writesymbolvalue(self.pos7, 1, 'S7WLBit')

            if self.drivecmdtagvalue == 15 and self.count != 8:
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

            if self.count == 8:
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

            if self.count == 2 and self.rdolcmdvalue == 1:
                writegeneral.writesymbolvalue(self.pos1, 0, 'S7WLBit')

            if self.count == 3 and self.rdolcmdvalue == 1:
                writegeneral.writesymbolvalue(self.pos2, 0, 'S7WLBit')

            if self.count == 4 and self.rdolcmdvalue == 1:
                writegeneral.writesymbolvalue(self.pos3, 0, 'S7WLBit')

            if self.count == 5 and self.rdolcmdvalue == 1:
                writegeneral.writesymbolvalue(self.pos4, 0, 'S7WLBit')

            if self.count == 6 and self.rdolcmdvalue == 1:
                writegeneral.writesymbolvalue(self.pos5, 0, 'S7WLBit')

            if self.count == 7 and self.rdolcmdvalue == 1:
                writegeneral.writesymbolvalue(self.pos6, 0, 'S7WLBit')

            if self.count == 8 and self.rdolcmdvalue == 1:
                writegeneral.writesymbolvalue(self.pos7, 0, 'S7WLBit')

            self.rdollowcmdvalue = readgeneral.readsymbolvalue(self.rdollowcmd, 'S7WLBit', "PE")

            if self.rdollowcmdvalue == 1 and self.count == 8:
                writegeneral.writesymbolvalue(self.rollertable1, 1, 'S7WLBit')

            sta_con_plc.disconnect()



        except Exception as e:
            log_exception(e)
            level = logging.INFO
            messege = "FN_RailSwitch7" + ":" + " Exception rasied(process): " + str(e.args) + str(e)
            logger.log(level, messege)

