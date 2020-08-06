from logger import *
from event_V2 import *
from time import sleep
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import logging
import  general
import gc

logger = logging.getLogger("main.log")

__all__ = ['Fn_RailSwitch8']


class Fn_RailSwitch8(Eventmanager):



    def __init__(self,filename):
        self.filename = filename
        self.count = 0
        self._fwdlimitswtvalue = False
        self._revlimitswtvalue = False
        self.setup()
        self.initilizedigitalinput()
        super().__init__(lambda: self.process())

    def setup(self):
        try:

            self.drivecmdentry1 = str("db27.dbw0")
            self.drivecmdentry2 = str("db27.dbw60")
            self.drivecmdentry3 = str("db27.dbw120")
            self.drivecmdentry4 = str("db27.dbw180")
            self.limitswitchentry1A = str(16.1)
            self.limitswitchentry1B = str(16.2)
            self.limitswitchentry2A = str(34.6)
            self.limitswitchentry2B = str(34.7)
            self.limitswitchentry3A = str(62.1)
            self.limitswitchentry3B = str(62.2)
            self.limitswitchentry4A = str(80.6)
            self.limitswitchentry4B = str(80.7)


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
        writegeneral.writesymbolvalue(self.limitswitchentry1A, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.limitswitchentry1B, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.limitswitchentry2A, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.limitswitchentry2B, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.limitswitchentry3A, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.limitswitchentry3B, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.limitswitchentry4A, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.limitswitchentry4B, 0, 'S7WLBit')

        sta_con_plc.disconnect()
        print("intiliased")
        pass

    def process(self):

        try:

            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)
            self.drivecmdentry1value = readgeneral.readDBvalue(self.drivecmdentry1, 'S7WLWord')
            self.drivecmdentry2value = readgeneral.readDBvalue(self.drivecmdentry2, 'S7WLWord')
            self.drivecmdentry3value = readgeneral.readDBvalue(self.drivecmdentry3, 'S7WLWord')
            self.drivecmdentry4value = readgeneral.readDBvalue(self.drivecmdentry4, 'S7WLWord')


            if self.drivecmdentry1value == 15:
                sleep(5)

                writegeneral.writesymbolvalue(self.limitswitchentry1A, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.limitswitchentry2A, 1, 'S7WLBit')
                sleep(5)
                writegeneral.writesymbolvalue(self.limitswitchentry1B, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.limitswitchentry2B, 1, 'S7WLBit')

            if self.drivecmdentry2value == 15:

                sleep(5)
                writegeneral.writesymbolvalue(self.limitswitchentry2A, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.limitswitchentry3A, 1, 'S7WLBit')
                sleep(5)
                writegeneral.writesymbolvalue(self.limitswitchentry2B, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.limitswitchentry3B, 1, 'S7WLBit')

            if self.drivecmdentry3value == 15:

                sleep(5)
                writegeneral.writesymbolvalue(self.limitswitchentry3A, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.limitswitchentry4A, 1, 'S7WLBit')
                sleep(5)
                writegeneral.writesymbolvalue(self.limitswitchentry3B, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.limitswitchentry4B, 1, 'S7WLBit')

            if self.drivecmdentry4value == 15:
                sleep(5)
                writegeneral.writesymbolvalue(self.limitswitchentry4A, 0, 'S7WLBit')
                sleep(5)
                writegeneral.writesymbolvalue(self.limitswitchentry4B, 0, 'S7WLBit')

            if self.drivecmdentry4value == 2063:
                sleep(5)
                writegeneral.writesymbolvalue(self.limitswitchentry4B, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.limitswitchentry3B, 1, 'S7WLBit')
                sleep(5)
                writegeneral.writesymbolvalue(self.limitswitchentry4A, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.limitswitchentry3A, 1, 'S7WLBit')

            if self.drivecmdentry3value == 2063:
                sleep(5)
                writegeneral.writesymbolvalue(self.limitswitchentry3B, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.limitswitchentry2B, 1, 'S7WLBit')
                sleep(5)
                writegeneral.writesymbolvalue(self.limitswitchentry3A, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.limitswitchentry2A, 1, 'S7WLBit')

            if self.drivecmdentry2value == 2063:
                sleep(5)
                writegeneral.writesymbolvalue(self.limitswitchentry2B, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.limitswitchentry1B, 1, 'S7WLBit')
                sleep(5)
                writegeneral.writesymbolvalue(self.limitswitchentry2A, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.limitswitchentry1A, 1, 'S7WLBit')



            sta_con_plc.disconnect()
            gc.collect()

            

        except Exception as e:
            log_exception(e)
            level = logging.INFO
            messege = "FN_RailSwitch8" + ":" + " Exception rasied(process): " + str(e.args) + str(e)
            logger.log(level, messege)


