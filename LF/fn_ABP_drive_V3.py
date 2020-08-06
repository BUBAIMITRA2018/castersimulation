from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
from event_V2 import *
import gc

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
        self.initilizedigitalinput()
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

        # if len(self.DriveRdytag) > 3:
        #     writegeneral.writeDBvalue(self.DriveRdytag, 1, 'S7WLBit')
        #     level = logging.INFO
        #     messege = self.devicename + ":" + self.DriveRdytag + " is trigger by 1"
        #     logger.log(level, messege)
        #
        #
        # if len(self.FaultFBtag) > 3:
        #     writegeneral.writeDBvalue(self.FaultFBtag, 1, 'S7WLBit')
        #     level = logging.INFO
        #     messege = self.devicename + ":" + self.FaultFBtag + " is trigger by 1"
        #     logger.log(level, messege)


        writegeneral.writeDBvalue(self.sw, 14129, 'S7WLWord')

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

            self.cw_val = int(readgeneral.readDBvalue(self.cw,'S7WLWord'))
            self.speedSP_val = int((readgeneral.readDBvalue(self.speedSP, 'S7WLWord')))


            print("control word value",self.cw_val)
            print("speed setpoint value", self.speedSP_val)


            if self.cw_val == 0:
                writegeneral.writeDBvalue(self.sw, 14129, 'S7WLWord')
                writegeneral.writeDBvalue(self.current, 0, 'S7WLWord')
                writegeneral.writeDBvalue(self.speedFB, 0, 'S7WLWord')
                writegeneral.writeDBvalue(self.torque, 0, 'S7WLWord')
                if len(self.dcvoltage) > 3:
                    writegeneral.writeDBvalue(self.dcvoltage, 27648, 'S7WLWord')

            if self.cw_val == 1139:
                writegeneral.writeDBvalue(self.sw, 14129, 'S7WLWord')
                writegeneral.writeDBvalue(self.current, 0, 'S7WLWord')
                writegeneral.writeDBvalue(self.speedFB, 0, 'S7WLWord')
                writegeneral.writeDBvalue(self.torque, 0, 'S7WLWord')
                if len(self.dcvoltage) > 3:
                    writegeneral.writeDBvalue(self.dcvoltage, 27648, 'S7WLWord')

            if self.cw_val == 1145:

                writegeneral.writeDBvalue(self.sw, 14131, 'S7WLWord')
                writegeneral.writeDBvalue(self.current, 17000, 'S7WLWord')
                writegeneral.writeDBvalue(self.torque, 17000, 'S7WLWord')
                writegeneral.writeDBvalue(self.speedFB, self.speedSP_val, 'S7WLWord')
                if len(self.dcvoltage) > 3:
                    writegeneral.writeDBvalue(self.dcvoltage, 27648, 'S7WLWord')

            if self.cw_val != 0 and self.cw_val == 1151:
                writegeneral.writeDBvalue(self.sw, 13111, 'S7WLWord')
                writegeneral.writeDBvalue(self.current, 17000, 'S7WLWord')
                writegeneral.writeDBvalue(self.torque, 17000, 'S7WLWord')
                writegeneral.writeDBvalue(self.speedFB, self.speedSP_val, 'S7WLWord')
                if len(self.dcvoltage) > 3:
                    writegeneral.writeDBvalue(self.dcvoltage, 27648, 'S7WLWord')

            sta_con_plc.disconnect()
            gc.collect()



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
                writegeneral.writeDBvalue(self.brakeonFB, value,'S7WLBit')
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











