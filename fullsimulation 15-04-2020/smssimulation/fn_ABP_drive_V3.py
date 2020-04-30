from logger import *
from event_V2 import *
from time import sleep
from event_V2 import *
from time import sleep
import logging
import threading

setup_logging_to_file("ABP_DRIVE.log")
logger = logging.getLogger("main.log")

__all__ = ['Fn_ABP_Drive']




class Fn_ABP_Drive(Eventmanager):

    def __init__(self, com, df, idxNo):
        self._idxNo = idxNo
        self.devicename = df.iloc[self._idxNo, 0]
        self.gen = com
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

        if len(self.DriveRdytag) > 3:
            self.gen.writegeneral.writenodevalue(self.DriveRdytag, 1)
            level = logging.INFO
            messege = self.devicename + ":" + self.DriveRdytag + " is trigger by 1"
            logger.log(level, messege)


        if len(self.FaultFBtag) > 3:
            self.gen.writegeneral.writenodevalue(self.FaultFBtag, 1)
            level = logging.INFO
            messege = self.devicename + ":" + self.FaultFBtag + " is trigger by 1"
            logger.log(level, messege)



    def driveprocess(self):

        try:
            if len(self.startcmdtag) > 3:
                self.startcmdvalue  = self.gen.readgeneral.readtagvalue(self.startcmdtag)

            if len(self.stopcmdtag) > 3:
                self.stopcmdvalue  = self.gen.readgeneral.readtagvalue(self.stopcmdtag)



            if len(self.cw)>3 and len(self.sw)>3 and len(self.speedSP):
                self.cw_val = int(self.gen.readgeneral.readtagvalue(self.cw))
                self.sw_val = int(self.gen.readgeneral.readtagvalue(self.sw))
                if  self.cw_val != 0 and self.cw_val == 1150:
                    self.gen.writegeneral.writenodevalue(self.sw,13169)
                    self.gen.writegeneral.writenodevalue(self.current, 0)
                    self.gen.writegeneral.writenodevalue(self.dcvoltage,27648)
                    self.statusword = 13169



                if self.cw_val != 0 and self.cw_val == 1151:
                    self.gen.writegeneral.writenodevalue(self.sw,13171)
                    self.gen.writegeneral.writenodevalue(self.current, 40)
                    self.gen.writegeneral.writenodevalue(self.torque, 40)
                    self.gen.writegeneral.writenodevalue(self.dcvoltage, 27648)
                self.speedSP_val = int(self.gen.readgeneral.readtagvalue(self.speedSP))



                if (self.sw_val>0) and (self.cw_val == 1151) and (self.speedSP_val>0):
                    self.speedSP_val = int(self.gen.readgeneral.readtagvalue(self.speedSP))
                    self.gen.writegeneral.writenodevalue(self.speedFB, self.speedSP_val)
                    self.gen.writegeneral.writenodevalue(self.sw,13175)
                    self.gen.writegeneral.writenodevalue(self.dcvoltage, 27648)



                if(self.speedSP_val == 0):
                    self.gen.writegeneral.writenodevalue(self.speedFB, 0)
                    self.gen.writegeneral.writenodevalue(self.dcvoltage, 27648)


                if self.cw_val != 1151 :
                    self.gen.writegeneral.writenodevalue(self.sw, 13169)
                    self.gen.writegeneral.writenodevalue(self.current, 0)
                    self.gen.writegeneral.writenodevalue(self.dcvoltage, 27648)



                self.sw_val = int(self.gen.readgeneral.readtagvalue(self.sw))
                self.speed_val = int(self.gen.readgeneral.readtagvalue(self.sw))




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
                    self.gen.writegeneral.writenodevalue(self.RunningFBtag, 1)

                if (len(self.ONFBtag) > 3):
                    self.gen.writegeneral.writenodevalue(self.ONFBtag, 1)

            if self.stopcmdvalue:
                if (len(self.RunningFBtag) > 3):
                    self.gen.writegeneral.writenodevalue(self.RunningFBtag, 0)

                if (len(self.ONFBtag) > 3):
                    self.gen.writegeneral.writenodevalue(self.ONFBtag, 0)




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
        if value != self._breakopencmd:
            if len(self.brakeonFB)> 3:
                self.gen.writegeneral.writenodevalue(self.brakeonFB, value)
                self.breakopenfb = value
            self._breakopencmd = value

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











