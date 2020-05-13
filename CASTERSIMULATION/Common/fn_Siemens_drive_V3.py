from logger import *
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
from event_V3 import *
from time import sleep
import logging
import threading
logger = logging.getLogger("main.log")

__all__ = ['Fn_Siemens_Drive']

class BreakOpenCmdObserver:
    def __init__(self, observable):
        observable.register_observer(self)



class Fn_Siemens_Drive(Eventmanager):

    def __init__(self, com, df, idxNo,filename):

        self._idxNo = idxNo
        self.devicename = df.iloc[self._idxNo, 0]
        self.com = com
        self.df = df
        self._cw = 0
        self.filename = filename
        self._breakopencmd = False
        self._sw = 0
        self._breakonFB = False
        self._speedsetpoint  = False
        self._startcmdvalue = False
        self._stopcmdvalue = False
        self._encodervalue = 0
        self.speedSP_val  = 0
        self.setup()
        self.initilizedigitalinput()
        super().__init__(lambda: self.driveprocess(),lambda : self.encoderprocess())



    def setup(self):
        try:


            for tag,col in self.readalltags():
                
                if col==3:
                    self.areatag = str(tag)

                if col==4:
                    self.cw = str(tag)

                if col==5:
                    self.sw = str(tag)

                if col==6:
                    self.speedFB = str(tag)
                    
                if col ==7:
                    self.speedSP = str(tag)

                if col == 8:
                    self.torque= str(tag)

                if col == 9:
                    self.current = str(tag)

                if col == 10:
                    self.drvreadytag = str(tag)

                if col == 11:
                    self.runningtag = str(tag)

                if col == 12:
                    self.faultfbtag = str(tag)

                if col == 13:
                    self.onfbtag = str(tag)

                if col == 14:
                    self.startcmdtag = str(tag)

                if col == 15:
                    self.stopcmdtag = str(tag)

                if col == 16:
                    self.connectiontype = str(tag)

                if col == 17:
                    self.breakopencmdtag = str(tag)

                if col == 18:
                    self.fastcount = int(tag)

                if col == 19:
                    self.encoderoutputtag = str(tag)

                if col == 20:
                    self.mtrnominalSpd = int(tag)

                if col == 21:
                    self.plcscancycle = str(tag)

                if col == 22:
                    self.driveEngg = int(tag)

                if col == 22:
                    self.kval = int(tag)





        except Exception as e:
            level = logging.ERROR
            messege = "SIEMENS DRIVES" + self.devicename + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)



    def initilizedigitalinput(self):

        client = Communication()
        sta_con_plc = client.opc_client_connect(self.filename)
        readgeneral = ReadGeneral(sta_con_plc)
        writegeneral = WriteGeneral(sta_con_plc)


        if self.connectiontype == "HARDWARE":

            if len(self.drvreadytag) > 3:
                writegeneral.writesymbolvalue(self.drvreadytag, 1, 'S7WLBit')
                level = logging.INFO
                messege = self.devicename + ":" + self.drvreadytag + " is trigger by 1"
                logger.log(level, messege)
            else:
                pass

            if len(self.faultfbtag) > 3:
                writegeneral.writesymbolvalue(self.faultfbtag, 1, 'S7WLBit')
                level = logging.INFO
                messege = self.devicename + ":" + self.faultfbtag + " is trigger by 1"
                logger.log(level, messege)
            else:
                pass

            sta_con_plc.disconnect()

    def driveprocess(self):

        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)

            if self.connectiontype == "PROFIBUS":

                if len(self.cw) > 3 and len(self.sw) > 3 and len(self.speedSP):
                    self.cw_val = int(readgeneral.readsymbolvalue(self.cw, 'S7WLWord', 'PA'))
                    if self.cw_val == 1087:
                        writegeneral.writesymbolvalue(self.sw, 13111, 'S7WLWord')
                        writegeneral.writesymbolvalue(self.current, 0, 'S7WLWord')
                        writegeneral.writesymbolvalue(self.torque, 0, 'S7WLWord')
                        writegeneral.writesymbolvalue(self.speedFB, 0, 'S7WLWord')

                    if self.cw_val == 1151:
                        self.speedSP_val = int(readgeneral.readsymbolvalue(self.speedSP, 'S7WLWord', 'PA'))
                        writegeneral.writesymbolvalue(self.current, 13824, 'S7WLWord')
                        writegeneral.writesymbolvalue(self.torque, 13824, 'S7WLWord')
                    writegeneral.writesymbolvalue(self.speedFB, self.speedSP_val, 'S7WLWord')

                    messege1 = self.devicename + ":" + self.sw + " tag value is " + "13111" \
                               + self.speedFB + " tag value is " + str(self.speedSP_val)
                    level = logging.WARNING
                    logger.log(level, messege1)

            if self.connectiontype == "HARDWARE":

                if len(self.stopcmdtag) > 3:
                    self.stopcmdvalue = readgeneral.readsymbolvalue(self.stopcmdtag, 'S7WLBit', 'PA')

                oncommandvalue = readgeneral.readsymbolvalue(self.startcmdtag, 'S7WLBit', 'PA')
                runfbvalue = readgeneral.readsymbolvalue(self.onfbtag, 'S7WLBit', 'PE')

                if oncommandvalue == True and runfbvalue == False:
                    writegeneral.writesymbolvalue(self.onfbtag, 1, 'S7WLBit')
                    self.speedSP_val = int(readgeneral.readsymbolvalue(self.speedSP, 'S7WLWord', 'PA'))
                    writegeneral.writesymbolvalue(self.current, 13824, 'S7WLWord')
                    writegeneral.writesymbolvalue(self.torque, 13824, 'S7WLWord')
                    writegeneral.writesymbolvalue(self.speedFB, self.speedSP_val, 'S7WLWord')

                    self.runFB = 1
                    level2 = logging.WARNING
                    messege2 = self.devicename + ":" + self.startcmdtag + " value is 1"
                    logger.log(level2, messege2)

                    level1 = logging.INFO
                    messege1 = self.devicename + ":" + self.onfbtag + " is trigger by 1"
                    logger.log(level1, messege1)

                if runfbvalue == True and oncommandvalue == False:
                    self.speedSP_val = int(readgeneral.readsymbolvalue(self.speedSP, 'S7WLWord', 'PA'))
                    writegeneral.writesymbolvalue(self.current, 0, 'S7WLWord')
                    writegeneral.writesymbolvalue(self.torque, 0, 'S7WLWord')
                    writegeneral.writesymbolvalue(self.speedFB, self.speedSP_val, 'S7WLWord')
                    writegeneral.writesymbolvalue(self.onfbtag, 0, 'S7WLBit')
                    self.runFB = 0

                    level2 = logging.WARNING
                    messege2 = self.devicename + ":" + self.startcmdtag + " value is 0"
                    logger.log(level2, messege2)

                    level1 = logging.INFO
                    messege1 = self.devicename + ":" + self.onfbtag + " is trigger by 0"
                    logger.log(level1, messege1)

                if len(self.stopcmdtag) > 3:
                    if runfbvalue == True and self.stopcmdvalue == True:
                        self.speedSP_val = int(readgeneral.readsymbolvalue(self.speedSP, 'S7WLWord', 'PA'))
                        writegeneral.writesymbolvalue(self.current, 0, 'S7WLWord')
                        writegeneral.writesymbolvalue(self.torque, 0, 'S7WLWord')
                        writegeneral.writesymbolvalue(self.speedFB, self.speedSP_val, 'S7WLWord')
                        writegeneral.writesymbolvalue(self.onfbtag, 0, 'S7WLBit')
                        self.runFB = 0

                    level2 = logging.WARNING
                    messege2 = self.devicename + ":" + self.stopcmdtag + " value is 0"
                    logger.log(level2, messege2)

                    level1 = logging.INFO
                    messege1 = self.devicename + ":" + self.onfbtag + " is trigger by 0"
                    logger.log(level1, messege1)

                sta_con_plc.disconnect()



        except Exception as e :

            log_exception(e)
            level = logging.ERROR
            messege = "SIEMENS DRIVES" + self.devicename + " Error messege(driveprocess)" + str(e.args)
            logger.log(level, messege)

    def encoderprocess(self):


        try:

            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)

            self.drivespeedfbvalue = readgeneral.readsymbolvalue(self.speedFB,'S7WLWord','PA')
            self._fastcountvalue = self.fastcount

            self_encodervalue = self.drivespeedfbvalue * self.mtrnominalSpd * self.plcscancycle * self.driveEngg * self.kval

            writegeneral.writesymbolvalue(self.encoderoutputtag, self._encodervalue, 'S7WLWord')




            # self.drivespvalue = readgeneral.readsymbolvalue(self.speedSP, 'S7WLWord', 'PA')
            # self._fastcountvalue = self.fastcount
            # self._encodervalue = readgeneral.readsymbolvalue(self.encoderoutputtag, 'S7WLWord', 'PE')
            # if (self.drivespvalue > 45000):
            #     self._encodervalue = self._encodervalue + self._fastcountvalue
            # if (self.drivespvalue < 45000):
            #     self._encodervalue = self._encodervalue - self._fastcountvalue
            # writegeneral.writesymbolvalue(self.encoderoutputtag, self._encodervalue, 'S7WLWord')

            sta_con_plc.disconnect()


        except Exception as e:
            log_exception(e)
            level = logging.INFO
            messege = self.devicename + ":" + " Exception rasied(Encoderprocess): " + str(e.args) + str(e)
            logger.log(level, messege)





    @property
    def controlword(self):
        return self._cw

    @controlword.setter
    def controlword(self, value):
        if value != self._cw:
            print("drive is fire")
            super().fire1()
            self._cw = value

    @property
    def statusword(self):
        return self._sw

    @statusword.setter
    def statusword(self, value):
        if value != self._sw:
            self._sw = value


    @property
    def speedsetpoint(self):
        return self._speedsetpoint

    @speedsetpoint.setter
    def speedsetpoint(self, value):
        if value != self._speedsetpoint:
            super().fire1()
            self._speedsetpoint = value


    @property
    def StartCmd(self):
        return self._startcmdvalue

    @StartCmd.setter
    def StartCmd(self, value):
        if value != self._startcmdvalue:
            super().fire1()
            self._startcmdvalue = value

    @property
    def BreakOpenCmd(self):
        return self._breakopencmd

    @BreakOpenCmd.setter
    def BreakOpenCmd(self, value):
        if value != self._breakopencmd:
            super().fire2()
            print("Fire encoder process")


    @property
    def StopCmd(self):
        return self._stopcmdvalue

    @StopCmd.setter
    def StopCmd(self, value):
        if value != self._stopcmdvalue:
            super().fire1()
            self._stopcmdvalue = value

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











