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



    def __init__(self,com,df,idxNo,filename):
        self._idxNo =idxNo
        self.devicename = df.iloc[self._idxNo,0]
        self.filename = filename
        self.gen = com
        self._fwdlimitswtvalue = False
        self._revlimitswtvalue = False
        # self._fwdrunFBvalue = False
        # self._revrunFBvalue = False
        self.df = df
        self.setup()
        self.initilizedigitalinput()
        super().__init__(lambda: self.railswitch())

    def setup(self):
        try:


            for tag,col in self.readalltags():

                if col==3:
                    self.areatag = str(tag)


                if col==4:
                    self.fwdlimitswttag = str(tag)

                if col==5:
                    self.revlimitswttag = str(tag)

                if col==6:
                    self.positionA = str(tag)

                if col ==7:
                    self.positionB = str(tag)

                if col == 8:
                    self.positionC = str(tag)

                if col == 9:
                    self.positionD = str(tag)
                if col == 10:
                    self.positionE = str(tag)

                if col == 11:
                    self.positionF = str(tag)

                if col == 12:
                    self.positionG = str(tag)

                if col == 13:
                    self.positionH = str(tag)

        except Exception as e:
            level = logging.ERROR
            messege = "FN_MOTOR2D" + self.devicename + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)



    def initilizedigitalinput(self):

            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)

            writegeneral.writesymbolvalue(self.positionA, 0, 'S7WLBit')
            writegeneral.writesymbolvalue(self.positionB, 0, 'S7WLBit')
            writegeneral.writesymbolvalue(self.positionC, 0, 'S7WLBit')
            writegeneral.writesymbolvalue(self.positionD, 0, 'S7WLBit')
            writegeneral.writesymbolvalue(self.positionE, 0, 'S7WLBit')
            writegeneral.writesymbolvalue(self.positionF, 0, 'S7WLBit')
            writegeneral.writesymbolvalue(self.positionG, 0, 'S7WLBit')
            writegeneral.writesymbolvalue(self.positionH, 0, 'S7WLBit')
            sta_con_plc.disconnect()

    def railswitch(self):

        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)
            # print('i m executing motor 2 d')
            self.fwdlimitswtvalue = readgeneral.readsymbolvalue(self.fwdlimitswttag,'S7WLBit','PE')
            self.revlimitswtvalue =  readgeneral.readsymbolvalue(self.revlimitswttag,'S7WLBit','PE')

            if self.fwdlimitswtvalue == True and self.revlimitswtvalue == False:

                writegeneral.writesymbolvalue(self.positionA, 1, 'S7WLBit')
                sleep(5)
                writegeneral.writesymbolvalue(self.positionA, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.positionB, 1, 'S7WLBit')
                sleep(5)
                writegeneral.writesymbolvalue(self.positionB, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.positionC, 1, 'S7WLBit')
                sleep(5)
                writegeneral.writesymbolvalue(self.positionC, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.positionD, 1, 'S7WLBit')
                sleep(5)
                writegeneral.writesymbolvalue(self.positionD, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.positionE, 1, 'S7WLBit')
                sleep(5)
                writegeneral.writesymbolvalue(self.positionE, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.positionF, 1, 'S7WLBit')
                sleep(5)
                writegeneral.writesymbolvalue(self.positionF, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.positionG, 1, 'S7WLBit')
                sleep(5)
                writegeneral.writesymbolvalue(self.positionG, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.positionH, 1, 'S7WLBit')

            if self.fwdlimitswtvalue == False and self.revlimitswtvalue == True:


                writegeneral.writesymbolvalue(self.positionH, 1, 'S7WLBit')
                sleep(5)
                writegeneral.writesymbolvalue(self.positionH, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.positionG, 1, 'S7WLBit')
                sleep(5)
                writegeneral.writesymbolvalue(self.positionG, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.positionF, 1, 'S7WLBit')
                sleep(5)
                writegeneral.writesymbolvalue(self.positionF, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.positionE, 1, 'S7WLBit')
                sleep(5)
                writegeneral.writesymbolvalue(self.positionE, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.positionD, 1, 'S7WLBit')
                sleep(5)
                writegeneral.writesymbolvalue(self.positionD, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.positionC, 1, 'S7WLBit')
                sleep(5)
                writegeneral.writesymbolvalue(self.positionC, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.positionB, 1, 'S7WLBit')
                sleep(5)
                writegeneral.writesymbolvalue(self.positionB, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.positionA, 1, 'S7WLBit')

            sta_con_plc.disconnect()



        except Exception as e:
            log_exception(e)
            level = logging.INFO
            messege = self.devicename + ":" + " Exception rasied(process): " + str(e.args) + str(e)
            logger.log(level, messege)
            print("Motor 2d error:",e.args)


    def __getstate__(self):
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        del state['mylock']
        return state

    @property
    def FwdOnlimit(self):
        return self._fwdlimitswtvalue

    @FwdOnlimit.setter
    def FwdOnlimit(self, value):
        if value != self._fwdlimitswtvalue:
            super().fire()
            self._fwdlimitswtvalue = value

    @property
    def RevOnlimit(self):
        return self._revlimitswtvalue

    @RevOnlimit.setter
    def RevOnlimit(self, value):
        if value != self._revlimitswtvalue:
            super().fire()
            self._revlimitswtvalue = value


    @property
    def areaname(self):
        return self.areatag



    def readalltags(self):
        n = 3
        row, col = self.df.shape
        print(col)
        while n < col:
            data = self.df.iloc[self._idxNo, n]
            yield data,n
            n = n + 1


