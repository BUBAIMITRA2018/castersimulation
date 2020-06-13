from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
from event_V2 import *

import logging


logger = logging.getLogger("main.log")

__all__ = ['Fn_ABP_Drive']




class Fn_ABP_Drive(Eventmanager):

    def __init__(self, com, df, idxNo,filename):
        self._idxNo = idxNo
        self.devicename = df.iloc[self._idxNo, 0]
        self.gen = com
        self.filename = filename
        self.df = df
        self._cw = 0
        self._breakopencmd = False
        self._sw = 0
        self._breakonFB = False
        self._speedsetpoint  = False
        self._startcmdvalue = False
        self._stopcmdvalue = False



        self.setup()
        super().__init__(lambda: self.driveprocess())


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
                    self.reqbrakeOpn = str(tag)
                    
                if col ==7:
                    self.brakeopncmd = str(tag)

                if col == 8:
                    self.brakeonFB= str(tag)

                if col == 9:
                    self.torque = str(tag)

                if col == 10:
                    self.current = str(tag)


                if col == 11:
                    self.speedFB = str(tag)

                if col == 12:
                    self.speedSP = str(tag)

                if col == 13:
                    self.dcvoltage = str(tag)

                if col == 14:
                    self.startcmdtag = str(tag)

                if col == 15:
                    self.stopcmdtag = str(tag)

                if col == 16:
                    self.DriveRdytag = str(tag)

                if col == 17:
                    self.RunningFBtag = str(tag)

                if col == 18:
                    self.FaultFBtag = str(tag)

                if col == 19:
                    self.ONFBtag = str(tag)


        except Exception as e:
            level = logging.ERROR
            messege = "ABP DRIVES" + self.devicename + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)

    def initilizedigitalinput(self):

        client = Communication()
        sta_con_plc = client.opc_client_connect(self.filename)
        readgeneral = ReadGeneral(sta_con_plc)
        writegeneral = WriteGeneral(sta_con_plc)

        if len(self.DriveRdytag) > 3:
            writegeneral.writesymbolvalue(self.DriveRdytag, 1, 'S7WLBit')
            level = logging.INFO
            messege = self.devicename + ":" + self.DriveRdytag + " is trigger by 1"
            logger.log(level, messege)


        if len(self.FaultFBtag) > 3:
            writegeneral.writesymbolvalue(self.FaultFBtag, 1, 'S7WLBit')           
            level = logging.INFO
            messege = self.devicename + ":" + self.FaultFBtag + " is trigger by 1"
            logger.log(level, messege)

        sta_con_plc.disconnect()



    def driveprocess(self):

        try:

            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)



            if len(self.startcmdtag) > 3:
                self.startcmdvalue  = readgeneral.readsymbolvalue(self.startcmdtag,'S7WLBit', 'PA')

            if len(self.stopcmdtag) > 3:
                self.stopcmdvalue  = readgeneral.readsymbolvalue(self.stopcmdtag,'S7WLBit', 'PA')



            if len(self.cw)>3 and len(self.sw)>3 and len(self.speedSP):
                self.cw_val = int(readgeneral.readsymbolvalue(self.cw,'S7WLWord', 'PA'))
                self.sw_val = int(readgeneral.readsymbolvalue(self.sw,'S7WLWord', 'PA'))
                if  self.cw_val != 0 and self.cw_val == 1150:
                    writegeneral.writesymbolvalue(self.sw,13169,'S7WLWord')
                    writegeneral.writesymbolvalue(self.current, 0,'S7WLWord')
                    writegeneral.writesymbolvalue(self.dcvoltage,27648,'S7WLWord')
                    self.statusword = 13169



                if self.cw_val != 0 and self.cw_val == 1151:
                    
                    writegeneral.writesymbolvalue(self.sw,13171,'S7WLWord')
                    writegeneral.writesymbolvalue(self.current, 40,'S7WLWord')
                    writegeneral.writesymbolvalue(self.torque, 40,'S7WLWord')
                    writegeneral.writesymbolvalue(self.dcvoltage, 27648,'S7WLWord')
                self.speedSP_val = int(readgeneral.readsymbolvalue(self.speedSP,'S7WLWord', 'PA'))



                if (self.sw_val>0) and (self.cw_val == 1151) and (self.speedSP_val>0):
                    self.speedSP_val = int(readgeneral.readsymbolvalue(self.speedSP,'S7WLWord', 'PA'))
                    writegeneral.writesymbolvalue(self.speedFB, self.speedSP_val,'S7WLWord')
                    writegeneral.writesymbolvalue(self.sw,13175,'S7WLWord')
                    writegeneral.writesymbolvalue(self.dcvoltage, 27648,'S7WLWord')



                if(self.speedSP_val == 0):
                    writegeneral.writesymbolvalue(self.speedFB, 0,'S7WLWord')
                    writegeneral.writesymbolvalue(self.dcvoltage, 27648,'S7WLWord')


                if self.cw_val != 1151 :
                    writegeneral.writesymbolvalue(self.sw, 13169,'S7WLWord')
                    writegeneral.writesymbolvalue(self.current, 0,'S7WLWord')
                    writegeneral.writesymbolvalue(self.dcvoltage, 27648,'S7WLWord')



                self.sw_val = int(readgeneral.readsymbolvalue(self.sw,'S7WLWord', 'PA'))
                self.speed_val = int(readgeneral.readsymbolvalue(self.speedFB,'S7WLWord', 'PA'))




                messege1 = self.devicename + ":" + self.sw + " tag value is " + str(self.sw) \
                + self.speedFB + " tag value is " + str(self.speed_val)
                level = logging.WARNING
                logger.log(level, messege1)

            else:

                if len(self.cw) > 3:
                    pass
                else:
                    messege1 = self.devicename + ":" + self.cw + " tag is missing"
                    level2 = logging.WARNING
                    logger.log(level2, messege1)

                if len(self.sw) > 3:
                    pass
                else:
                    messege2 = self.devicename + ":" + self.sw + " tag is missing"
                    level2 = logging.WARNING
                    logger.log(level2, messege2)

                if len(self.speedSP) > 3:
                    pass
                else:
                    messege3 = self.devicename + ":" + (self.sw) + " tag is missing"
                    level2 = logging.WARNING
                    logger.log(level2, messege3)

            if self.startcmdvalue :
                if(len(self.RunningFBtag) > 3):
                    writegeneral.writesymbolvalue(self.RunningFBtag, 1,'S7WLBit')

                if (len(self.ONFBtag) > 3):
                    writegeneral.writesymbolvalue(self.ONFBtag, 1,'S7WLBit')

            if self.stopcmdvalue:
                if (len(self.RunningFBtag) > 3):
                    writegeneral.writesymbolvalue(self.RunningFBtag, 0,'S7WLBit')

                if (len(self.ONFBtag) > 3):
                    writegeneral.writesymbolvalue(self.ONFBtag, 0,'S7WLBit')

            sta_con_plc.disconnect()



        except Exception as e:
            log_exception(e)
            level = logging.ERROR
            messege = "ABP DRIVES" + self.devicename + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)

    @property
    def controlword(self):
        return self._cw

    @controlword.setter
    def controlword(self, value):
        if value != self._cw:
            print("drive is fire")
            super().fire()
            self._cw = value

    @property
    def statusword(self):
        return self._sw

    @statusword.setter
    def statusword(self, value):
        if value != self._sw:
            self._sw = value

    @property
    def breakopencmd(self):
        return self._breakopencmd

    @breakopencmd.setter
    def breakopencmd(self, value):
        client = Communication()
        sta_con_plc = client.opc_client_connect(self.filename)
        readgeneral = ReadGeneral(sta_con_plc)
        writegeneral = WriteGeneral(sta_con_plc)
        if value != self._breakopencmd:
            if len(self.brakeonFB)> 3:
                writegeneral.writesymbolvalue(self.brakeonFB, value,'S7WLBit')
                self.breakopenfb = value
            self._breakopencmd = value
        sta_con_plc.disconnect()

    @property
    def speedsetpoint(self):
        return self._speedsetpoint

    @speedsetpoint.setter
    def speedsetpoint(self, value):
        if value != self._speedsetpoint:
            super().fire()
            self._speedsetpoint = value


    @property
    def breakopenfb(self):
        return self._breakonFB

    @breakopenfb.setter
    def breakopenfb(self, value):
        if value != self._breakonFB:
            self._breakonFB = value



    @property
    def StartCmd(self):
        return self._startcmdvalue

    @StartCmd.setter
    def StartCmd(self, value):
        if value != self._startcmdvalue:
            print("drive is fire")
            super().fire()
            self._startcmdvalue = value


    @property
    def StopCmd(self):
        return self._stopcmdvalue

    @StopCmd.setter
    def StopCmd(self, value):
        if value != self._stopcmdvalue:
            print("drive is fire")
            super().fire()
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











