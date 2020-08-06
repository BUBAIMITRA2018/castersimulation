from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
from event_V2 import *

import logging


logger = logging.getLogger("main.log")

__all__ = ['Fn_Schneider_Drive']




class Fn_Schneider_Drive(Eventmanager):

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
            messege = "Fn_Schneider_Drive" + self.devicename + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)

    def initilizedigitalinput(self):

        client = Communication()
        sta_con_plc = client.opc_client_connect(self.filename)
        readgeneral = ReadGeneral(sta_con_plc)
        writegeneral = WriteGeneral(sta_con_plc)

        if len(self.DriveRdytag) > 3:
            writegeneral.writeDBvalue(self.DriveRdytag, 1, 'S7WLBit')
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



            if len(self.cw)>3 and len(self.sw)>3 and len(self.speedSP)>3:
                print('the CW tag ', self.cw)

                self.cw_val = (readgeneral.readDBvalue(self.cw,'S7WLWord'))

                print('the SW tag ', self.sw)
                self.sw_val = (readgeneral.readDBvalue(self.sw,'S7WLWord'))
                self.speedSP_val = int(readgeneral.readDBvalue(self.speedSP, 'S7WLWord'))

                if self.cw_val != 0 and self.cw_val == 6:
                    writegeneral.writeDBvalue(self.sw,11,'S7WLWord')
                    if len(self.torque) > 3:
                        writegeneral.writeDBvalue(self.torque, 0, 'S7WLWord')

                    if len(self.dcvoltage) > 3:
                        writegeneral.writeDBvalue(self.dcvoltage, 0, 'S7WLWord')

                    if len(self.current) > 3:
                        writegeneral.writeDBvalue(self.current, 0, 'S7WLWord')
                    writegeneral.writeDBvalue(self.speedFB,self.speedSP_val, 'S7WLWord')



                if self.cw_val != 0 and self.cw_val == 15:
                    writegeneral.writeDBvalue(self.sw,527,'S7WLWord')
                    writegeneral.writeDBvalue(self.speedFB, self.speedSP_val, 'S7WLWord')

                    if len(self.torque) > 3:
                        writegeneral.writeDBvalue(self.torque, 130, 'S7WLWord')

                    if len(self.dcvoltage) > 3:
                        writegeneral.writeDBvalue(self.dcvoltage, 13175, 'S7WLWord')

                    if len(self.current) > 3:
                        writegeneral.writeDBvalue(self.current, 13, 'S7WLWord')



                if self.cw_val != 0 and self.cw_val == 2063:
                    writegeneral.writeDBvalue(self.sw, 16911, 'S7WLWord')
                    writegeneral.writeDBvalue(self.speedFB, self.speedSP_val, 'S7WLWord')

                    if len(self.torque) > 3:
                        writegeneral.writeDBvalue(self.torque, 130, 'S7WLWord')

                    if len(self.dcvoltage) > 3:
                        writegeneral.writeDBvalue(self.dcvoltage, 13175, 'S7WLWord')

                    if len(self.current) > 3:
                        writegeneral.writeDBvalue(self.current, 13, 'S7WLWord')


                if self.cw_val != 0 and self.cw_val == 64:
                    writegeneral.writeDBvalue(self.sw, 8719, 'S7WLWord')
                    writegeneral.writeDBvalue(self.speedFB, 0, 'S7WLWord')

                    if len(self.torque) > 3:
                        writegeneral.writeDBvalue(self.torque, 0, 'SS7WLWord')

                    if len(self.dcvoltage) > 3:
                        writegeneral.writeDBvalue(self.dcvoltage, 0, 'S7WLWord')

                    if len(self.current) > 3:
                        writegeneral.writeDBvalue(self.current, 0, 'S7WLWord')



                if self.cw_val != 0 and self.cw_val == 128:
                    writegeneral.writeDBvalue(self.sw, 11, 'SS7WLWord')
                    writegeneral.writeDBvalue(self.speedFB, 0, 'S7WLWord')

                    if len(self.torque) > 3:
                        writegeneral.writeDBvalue(self.torque, 0, 'S7WLWord')

                    if len(self.dcvoltage) > 3:
                        writegeneral.writeDBvalue(self.dcvoltage, 0, 'S7WLWord')

                    if len(self.current) > 3:
                        writegeneral.writeDBvalue(self.current, 0, 'S7WLWord')


            # if self.startcmdvalue :
            #     if(len(self.RunningFBtag) > 3):
            #         writegeneral.writesymbolvalue(self.RunningFBtag, 1,'S7WLBit')
            #
            #     if (len(self.ONFBtag) > 3):
            #         writegeneral.writesymbolvalue(self.ONFBtag, 1,'S7WLBit')
            #
            # if self.stopcmdvalue:
            #     if (len(self.RunningFBtag) > 3):
            #         writegeneral.writesymbolvalue(self.RunningFBtag, 0,'S7WLBit')
            #
            #     if (len(self.ONFBtag) > 3):
            #         writegeneral.writesymbolvalue(self.ONFBtag, 0,'S7WLBit')

            sta_con_plc.disconnect()



        except Exception as e:
            log_exception(e)
            level = logging.ERROR
            messege = "Fn_Schneider_Drive" + self.devicename + " Error messege(process)" + str(e.args)
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











