from event_V2 import *
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
from numpy import *
import logging

logger = logging.getLogger("main.log")

__all__ = ['Fn_Cylinder']


class Fn_Cylinder():

    def __init__(self,df,idxNo,filename):
        self._idxNo = idxNo
        self.filename = filename
        self.df = df
        self.devicename = df.iloc[self._idxNo, 0]
        self.setup()
        self.initilizedigitalinput()
        self._speedsetpoint = 0.0
        super().__init__(lambda: self.process())

    def setup(self):
        try:

            self.Sptag = str()
            self.areatag = str()
            self.CylStokeHighLim = float()
            self.CylStokeLowLim = float()
            self.SysPressHighLim = float()
            self.SysPressLowLim = float()
            self.constant = float()
            self.stokeconstant = float()
            self.RodSidePresstag = str()
            self.PistonSidePresstag =str()
            self.SSIPosFbtag = str()
            self.type = str(double)
            self.sptype = str("unipolar")



        except Exception as e:
            level = logging.ERROR
            messege = " Fn_Cylinder" + self.devicename + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)



    def initilizedigitalinput(self):

        client = Communication()
        sta_con_plc = client.opc_client_connect(self.filename)
        readgeneral = ReadGeneral(sta_con_plc)
        writegeneral = WriteGeneral(sta_con_plc)

        self.CylStokeHighLimrawvalue = longlong( self.unscaling(self.CylStokeHighLim, 33554431,self.CylStokeHighLim, self.CylStokeLowLim,0))
        self.CylStokeHighLowLimrawvalue = longlong( self.unscaling(self.CylStokeLowLim,33554431, self.CylStokeHighLim, self.CylStokeLowLim,0))
        self.SysPressHighLimrawvalue = float(self.unscaling(self.CylStokeHighLim,27648,self.CylStokeHighLim,self.CylStokeLowLim,0))
        self.SysPressLowLimrawvalue = float(self.unscaling(self.SysPressLowLim,27648, self.SysPressHighLim, self.SysPressLowLim,0))

        sta_con_plc.disconnect()

    def unscaling(self, val,engineeringvaluerange, highlimit, lowlimit,engineeringlowlimit):
            processvaluerange = highlimit - lowlimit
            enggunit = (engineeringvaluerange /processvaluerange) * (val-lowlimit) + engineeringlowlimit
            return enggunit



    def process(self):

        try:

            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)

            self.currentspplcrawvalue = readgeneral.readsymbolvalue(self.Sptag, 'S7WLWord', 'PA')
            self.rodsidepressrawvalue = readgeneral.readsymbolvalue(self.RodSidePresstag, 'S7WLWord', 'PE')
            self.SSIPosFbvalue = readgeneral.readsymbolvalue(self.SSIPosFbtag, 'S7WLDWord', 'PE')


            if self.sptype == "unipolar":
                self.currentsprawvalue = (55296 /27648) * (self.currentspplcrawvalue -0) + (-27648)
            else:
                self.currentsprawvalue = self.currentspplcrawvalue

            rateofchange = (self.currentsprawvalue / 27648) * 100 * self.constant
            rateofchangecylstoke = (self.currentsprawvalue / 27648) * 100 * self.stokeconstant


            if self.currentsprawvalue > 0:
                if self.rodsidepressrawvalue < self.SysPressHighLimrawvalue:
                    rodsidepressoutrawvalue = self.rodsidepressrawvalue + rateofchange
                    rodsidepressoutintrawvalue = int(rodsidepressoutrawvalue)
                    if rodsidepressoutintrawvalue < 27648:
                        self.simrodsidepressoutrawvalue = rodsidepressoutintrawvalue
                    else:
                        self.simrodsidepressoutrawvalue = 27648



                if self.currentsprawvalue < 0:
                    if self.rodsidepressrawvalue > self.SysPressLowLimrawvalue:
                        rodsidepressoutrawvalue = self.rodsidepressrawvalue + rateofchange
                        rodsidepressoutintrawvalue = int(rodsidepressoutrawvalue)
                        if rodsidepressoutintrawvalue > 0:
                            self.simrodsidepressoutrawvalue = rodsidepressoutintrawvalue
                        else:
                            self.simrodsidepressoutrawvalue = 0



            if type == "twosidecyl":
                pistonsideressoutrawvalue = 27648 - self.rodsidepressrawvalue
                self.simpistonsidepressoutrawvalue = pistonsideressoutrawvalue




            SSIPosFbvalueoutrawvalue = self.SSIPosFbvalue + rateofchangecylstoke

            SSIPosFbvalueoutlongrawvalue = longlong(SSIPosFbvalueoutrawvalue)

            if SSIPosFbvalueoutlongrawvalue > 33554431:
                self.simSSIPosFbvalueoutlongrawvalue = 33554431


            else:
                if SSIPosFbvalueoutlongrawvalue < 0:
                    self.simSSIPosFbvalueoutlongrawvalue = 0

                else:
                    self.simSSIPosFbvalueoutlongrawvalue = SSIPosFbvalueoutlongrawvalue



            writegeneral.writesymbolvalue(self.RodSidePresstag, self.simrodsidepressoutrawvalue, 'S7WLWord')
            writegeneral.writesymbolvalue(self.PistonSidePresstag, self.simpistonsidepressoutrawvalue, 'S7WLWord')
            writegeneral.writesymbolvalue(self.SSIPosFbvalue, self.simSSIPosFbvalueoutlongrawvalue, 'S7WLDWord')


            sta_con_plc.disconnect()


        except Exception as e:
            log_exception(e)
            level = logging.INFO
            messege = self.devicename + ":" + " Exception rasied(Encoderprocess): " + str(e.args) + str(e)
            logger.log(level, messege)



    @property
    def areaname(self):
        return self.areatag

    @property
    def speedsetpoint(self):
        return self._speedsetpoint

    @speedsetpoint.setter
    def speedsetpoint(self, value):
        if value != self._speedsetpoint:
            super().fire()
            self._speedsetpoint = value

    def readalltags(self):
        n = 3
        row, col = self.df.shape
        print(col)
        while n < col:
            data = self.df.iloc[self._idxNo, n]
            yield data,n
            n = n + 1












