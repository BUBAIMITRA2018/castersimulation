from logger import *
from event_V2 import *
from time import sleep
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import logging
import  general

logger = logging.getLogger("main.log")

__all__ = ['Fn_RailSwitch7']


class Fn_RailSwitch7(Eventmanager):



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

            self.drivecmdtag = str("db27.dbw560")
            self.trackposition = str(272.7)
            self.forwardendpoint = str(273.0)
            self.reverseendpoint = str(273.1)
            self.trackposition1 = str(273.4)
            self.forwardendpoint1 = str(273.5)
            self.reverseendpoint1 = str(273.6)
            self.trackposition2 = str(274.1)
            self.forwardendpoint2 = str(274.2)
            self.reverseendpoint2 = str(274.3)
            self.trackposition3 = str(274.6)
            self.forwardendpoint3 = str(274.7)
            self.reverseendpoint3 = str(275.0)
            self.counter = str("db65.dbw30")

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
        sta_con_plc.disconnect()
        print("intiliased")
        pass

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

            if self.count == 4:
                writegeneral.writesymbolvalue(self.forwardendpoint, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.forwardendpoint1, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.forwardendpoint2, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.forwardendpoint3, 0, 'S7WLBit')

            if self.count == 2:
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

            sleep(1)

            sta_con_plc.disconnect()

            

        except Exception as e:
            log_exception(e)
            level = logging.INFO
            messege = "FN_RailSwitch8" + ":" + " Exception rasied(process): " + str(e.args) + str(e)
            logger.log(level, messege)


