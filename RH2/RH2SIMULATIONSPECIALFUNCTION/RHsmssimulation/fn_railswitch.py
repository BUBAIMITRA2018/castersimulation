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
        self.count = 0
        self._fwdlimitswtvalue = False
        self._revlimitswtvalue = False
        # self._fwdrunFBvalue = False
        # self._revrunFBvalue = False
        self.setup()
        self.initilizedigitalinput()
        super().__init__(lambda: self.railswitch())

    def setup(self):
        try:


                    self.drivecmdtag = str(88)
                    self.trackposition = str(16.3)
                    self.forwardendpoint = str(16.4)
                    self.reverseendpoint = str(16.5)


        except Exception as e:
            level = logging.ERROR
            messege = "FN_MOTOR2D" + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)



    def initilizedigitalinput(self):
        pass

    def railswitch(self):
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)
            self.drivecmdtagvalue = readgeneral.readsymbolvalue(self.drivecmdtag,'S7WLWord','PA')


            if self.drivecmdtagvalue == 15 and self.count != 8:
                sleep(2)
                writegeneral.writesymbolvalue(self.trackposition, 1, 'S7WLBit')
                sleep(5)
                writegeneral.writesymbolvalue(self.trackposition, 0, 'S7WLBit')
                self.count = self.count+1


            if self.drivecmdtagvalue == 2063 and self.count != 0:
                sleep(2)
                writegeneral.writesymbolvalue(self.trackposition, 1, 'S7WLBit')
                sleep(5)
                writegeneral.writesymbolvalue(self.trackposition, 0, 'S7WLBit')
                self.count = self.count-1

            if self.count == 8:
                sleep(2)
                writegeneral.writesymbolvalue(self.forwardendpoint, 1, 'S7WLBit')

            if self.count == 0:
                sleep(2)
                writegeneral.writesymbolvalue(self.reverseendpoint, 1, 'S7WLBit')

            sta_con_plc.disconnect()





