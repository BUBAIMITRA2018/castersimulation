
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import logging

logger = logging.getLogger("main.log")

__all__ = ['Fn_PLC_2_PLC_COMMUNICATION']



class Fn_PLC_2_PLC_COMMUNICATION():

    def __init__(self):

        self.devicename = 'PLC_2_PLC_COMMUNICATION'
        self._breakopencmd = False
        self._breakonFB = False
        self._speedsetpoint = False
        self._encodervalue = 0
        self.encoderoutputtag = ''
        self.speedSP_val = 0
        self.setup()
        self.initilizedigitalinput()


    def setup(self):
        try:

            # ........................................TCS....................
            self.IN_MLC_FASTSTOP = str(613.7)
            self.IN_MLC_ECLOSEFRMDRV = str(614.0)
            self.IN_MLC_GENDRVSTOP = str(614.1)

            self.OUT_TCS_ECLOSE = str(616.0)
            self.OUT_TCS_DRVSTART = str(616.1)
            self.OUT_TCS_MLCREADY = str(616.2)
            self.OUT_TCS_TD1PHPOS = str(616.3)
            self.OUT_TCS_TD2PHPOS = str(616.4)
            self.OUT_TCS_ECLOSE2 = str(616.5)
            self.OUT_TCS_HMOFAULT = str(616.6)

            # ........................................DRIVE....................

            self.OUT_MLC_FASTSTOP = str(403.0)
            self.OUT_MLC_ECLOSEFRMDRV = str(403.1)
            self.OUT_MLC_GENDRVSTOP = str(403.2)

            self.IN_TCS_ECLOSE = str(410.0)
            self.IN_TCS_DRVSTART = str(410.1)
            self.IN_TCS_MLCREADY = str(410.2)
            self.IN_TCS_TD1PHPOS = str(410.3)
            self.IN_TCS_TD2PHPOS = str(410.4)
            self.IN_TCS_ECLOSE2 = str(410.5)
            self.IN_TCS_HMOFAULT = str(410.6)




        except Exception as e:
            level = logging.ERROR
            messege = "PLC_2_PLC_COMMUNICATION" + self.devicename + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)



    def initilizedigitalinput(self):
        pass




    def process(self):


        try:
            client = Communication()
            sta_con_drvplc = client.opc_client_connect('10.17.13.235', 0, 3)
            readgeneral_drvplc = ReadGeneral(sta_con_drvplc)
            writegeneral_drvplc = WriteGeneral(sta_con_drvplc)

            sta_con_tcsplc = client.opc_client_connect('10.17.13.237', 0, 3)
            readgeneral_tcsplc = ReadGeneral(sta_con_tcsplc)
            writegeneral_tcsplc = WriteGeneral(sta_con_tcsplc)

            MLC_FASTSTOP =  readgeneral_drvplc.readsymbolvalue(self.OUT_MLC_FASTSTOP, 'S7WLBit', 'PA')
            writegeneral_tcsplc.writesymbolvalue(self.IN_MLC_FASTSTOP, MLC_FASTSTOP , 'S7WLBit')

            MLC_ECLOSEFRMDRV = readgeneral_drvplc.readsymbolvalue(self.OUT_MLC_ECLOSEFRMDRV, 'S7WLBit', 'PA')
            writegeneral_tcsplc.writesymbolvalue(self.IN_MLC_ECLOSEFRMDRV, MLC_ECLOSEFRMDRV, 'S7WLBit')

            MLC_GENDRVSTOP = readgeneral_drvplc.readsymbolvalue(self.OUT_MLC_GENDRVSTOP, 'S7WLBit', 'PA')
            writegeneral_tcsplc.writesymbolvalue(self.OUT_MLC_GENDRVSTOP, MLC_GENDRVSTOP, 'S7WLBit')

            TCS_ECLOSE = readgeneral_tcsplc.readsymbolvalue(self.OUT_TCS_ECLOSE, 'S7WLBit', 'PA')
            writegeneral_drvplc.writesymbolvalue(self.IN_TCS_ECLOSE, TCS_ECLOSE, 'S7WLBit')

            TCS_DRVSTART = readgeneral_tcsplc.readsymbolvalue(self.OUT_TCS_DRVSTART, 'S7WLBit', 'PA')
            writegeneral_drvplc.writesymbolvalue(self.IN_TCS_DRVSTART, TCS_DRVSTART, 'S7WLBit')

            TCS_MLCREADY = readgeneral_tcsplc.readsymbolvalue(self.OUT_TCS_MLCREADY, 'S7WLBit', 'PA')
            writegeneral_drvplc.writesymbolvalue(self.IN_TCS_MLCREADY, TCS_MLCREADY, 'S7WLBit')

            TCS_TD1PHPOS = readgeneral_tcsplc.readsymbolvalue(self.OUT_TCS_TD1PHPOS, 'S7WLBit', 'PA')
            writegeneral_drvplc.writesymbolvalue(self.IN_TCS_TD1PHPOS, TCS_TD1PHPOS, 'S7WLBit')

            TCS_TD2PHPOS = readgeneral_tcsplc.readsymbolvalue(self.OUT_TCS_TD2PHPOS, 'S7WLBit', 'PA')
            writegeneral_drvplc.writesymbolvalue(self.IN_TCS_TD2PHPOS, TCS_TD2PHPOS, 'S7WLBit')

            TCS_ECLOSE2 = readgeneral_tcsplc.readsymbolvalue(self.OUT_TCS_ECLOSE2, 'S7WLBit', 'PA')
            writegeneral_drvplc.writesymbolvalue(self.IN_TCS_ECLOSE2, TCS_ECLOSE2, 'S7WLBit')

            TCS_HMOFAULT = readgeneral_tcsplc.readsymbolvalue(self.OUT_TCS_HMOFAULT, 'S7WLBit', 'PA')
            writegeneral_drvplc.writesymbolvalue(self.IN_TCS_HMOFAULT, TCS_HMOFAULT, 'S7WLBit')



            sta_con_drvplc.disconnect()
            sta_con_tcsplc.disconnect()



        except Exception as e:
            log_exception(e)
            level = logging.INFO
            messege = self.devicename + ":" + " Exception rasied(Encoderprocess): " + str(e.args) + str(e)
            logger.log(level, messege)














