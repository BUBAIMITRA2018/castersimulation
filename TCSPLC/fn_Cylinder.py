from event_V2 import *
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
from numpy import *
import logging
from time import sleep

logger = logging.getLogger("main.log")

__all__ = ['Fn_Cylinder']


class Fn_Cylinder(Eventmanager):

    def __init__(self,df,idxNo,filename):
        self._idxNo = idxNo
        self.filename = filename
        self.df = df
        self.devicename = df.iloc[self._idxNo, 0]
        self.setup()
        self.initilizedigitalinput()
        self._speedsetpoint = 0.0
        self.simrodsidepressoutrawvalue = 0
        self.simpistonsidepressoutrawvalue = 0
        self.simSSIPosFbvalueoutlongrawvalue = 0
        self.positionrawvalue = 0
        self.mylock = threading.Lock()
        super().__init__(lambda: self.cylinderprocess())

    def setup(self):
        try:


                for tag, col in self.readalltags():

                    if col == 3:
                        self.areatag = str(tag)

                    if col == 4:
                        self.Sptag = str(tag)

                    if col == 5:
                        self.RodSidePresstag = str(tag)

                    if col == 6:
                        self.PistonSidePresstag =str(tag)

                    if col == 7:
                        self.SSIPosFbtag = str(tag)

                    if col == 8:
                        self.Digitalcondition = str(tag)

                    if col == 9 :
                        self.punchrollvalveact = str(tag)

                    if col == 10 :
                        self.CylStokeHighLim = float(tag)

                    if col == 11 :
                        self.CylStokeLowLim = float(tag)

                    if col == 12 :
                        self.SysPressHighLim = float(tag)

                    if col == 13:
                        self.SysPressLowLim = float(tag)

                    if col == 14:
                        self.constant= float(tag)

                    if col == 15:
                        self.stokeconstant = float(tag)

                    if col == 16:
                        self.type = str(tag)

                    if col == 17:
                        self.sptype= str(tag)


                    if col == 18:
                        self.positiontag  = str(tag)



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

        self.CylStokeHighLimrawvalue = longlong( self.unscaling(self.CylStokeHighLim, 50000,self.CylStokeHighLim, self.CylStokeLowLim,0))
        self.CylStokeHighLowLimrawvalue = longlong( self.unscaling(self.CylStokeLowLim,50000, self.CylStokeHighLim, self.CylStokeLowLim,0))
        self.SysPressHighLimrawvalue = float(self.unscaling(self.CylStokeHighLim,27648,self.CylStokeHighLim,self.CylStokeLowLim,0))
        self.SysPressLowLimrawvalue = float(self.unscaling(self.SysPressLowLim,27648, self.SysPressHighLim, self.SysPressLowLim,0))
        # self.positionHighLimrawvalue = float(self.unscaling(self.CylStokeHighLim, 27648, self.CylStokeHighLim, self.CylStokeLowLim, -27648))
        # self.positionLowLimrawvalue = float(self.unscaling(self.SysPressLowLim, 27648, self.SysPressHighLim, self.SysPressLowLim, -27648))
        self.positionHighLimrawvalue = float(27648)
        self.positionLowLimrawvalue = float(-27648)




        sta_con_plc.disconnect()

    def unscaling(self, val,engineeringvaluerange, highlimit, lowlimit,engineeringlowlimit):
            processvaluerange = highlimit - lowlimit
            enggunit = (engineeringvaluerange /processvaluerange) * (val-lowlimit) + engineeringlowlimit
            return enggunit



    def cylinderprocess(self):


        try:

            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)
            self.Digitalconditionvalue = readgeneral.readsymbolvalue(self.Digitalcondition, 'S7WLBit', 'PA')
            self.currentspplcrawvalue = float(readgeneral.readsymbolvalue(self.Sptag, 'S7WLWord', 'PA'))
            self.rodsidepressrawvalue = float(readgeneral.readsymbolvalue(self.RodSidePresstag, 'S7WLWord', 'PE'))
            self.positionrawvalue = float(readgeneral.readsymbolvalue(self.positiontag, 'S7WLWord', 'PE'))
            self.SSIPosFbvalue = float(readgeneral.readsymbolvalue(self.SSIPosFbtag, 'S7WLDWord', 'PE'))
            print("the raw posittion va;yue ",self.positionrawvalue)


            if self.sptype == "unipolar":
                self.currentsprawvalue = (55296 /27648) * (self.currentspplcrawvalue -0) + (-27648)
            else:
                self.currentsprawvalue = self.currentspplcrawvalue

            rateofchange = (self.currentsprawvalue / 27648) * 100 * self.constant
            rateofchangecylstoke = (self.currentsprawvalue / 27648) * 100 * self.stokeconstant


            if self.currentsprawvalue > 0 and self.Digitalconditionvalue == 1:
                print("i was here")
                if self.rodsidepressrawvalue < self.SysPressHighLimrawvalue:
                    rodsidepressoutrawvalue = self.rodsidepressrawvalue + rateofchange
                    rodsidepressoutintrawvalue = int(rodsidepressoutrawvalue)
                    if rodsidepressoutintrawvalue < 27648:
                        self.simrodsidepressoutrawvalue = rodsidepressoutintrawvalue
                    else:
                        self.simrodsidepressoutrawvalue = 27648



            if self.currentsprawvalue < 0 and self.Digitalconditionvalue == 1:
                if self.rodsidepressrawvalue > self.SysPressLowLimrawvalue:
                    rodsidepressoutrawvalue = self.rodsidepressrawvalue + rateofchange
                    rodsidepressoutintrawvalue = int(rodsidepressoutrawvalue)
                    if rodsidepressoutintrawvalue > 0:
                        self.simrodsidepressoutrawvalue = rodsidepressoutintrawvalue
                    else:
                        self.simrodsidepressoutrawvalue = 0


            # if self.currentsprawvalue > 0 and self.Digitalconditionvalue == 1:
            #     if self.positionrawvalue < self.positionHighLimrawvalue:
            #         print("the actual position is not working")
            #         postionrawvalue = self.positionrawvalue + rateofchange
            #         positionintrawvalue = int(postionrawvalue)
            #         if  positionintrawvalue < 27648:
            #             self.positionrawvalue1 =  positionintrawvalue
            #         else:
            #             self.positionrawvalue1 = 27648

            self.positionrawvalue1 = self.currentsprawvalue



            # if self.currentsprawvalue < 0 and self.Digitalconditionvalue == 1:
            #
            #     if self.positionrawvalue > self.positionLowLimrawvalue:
            #         print("the actual position is not workingkkefdfkfkfkvfpvkfvmkfdmvkmfdkvmkfdmkvvkvk")
            #         postionrawvalue = self.positionrawvalue + rateofchange
            #         positionintrawvalue = int(postionrawvalue)
            #         if positionintrawvalue > -27648:
            #             self.positionrawvalue1 =  positionintrawvalue
            #         else:
            #             self.positionrawvalue1 = -27648



            if self.type == "twosidecyl":
                pistonsideressoutrawvalue = 27648 - self.rodsidepressrawvalue
                self.simpistonsidepressoutrawvalue = pistonsideressoutrawvalue




            SSIPosFbvalueoutrawvalue = self.SSIPosFbvalue + rateofchangecylstoke

            SSIPosFbvalueoutlongrawvalue = longlong(SSIPosFbvalueoutrawvalue)

            if SSIPosFbvalueoutlongrawvalue > 50000 and self.Digitalconditionvalue == 1:
                self.simSSIPosFbvalueoutlongrawvalue = 50000


            else:
                if SSIPosFbvalueoutlongrawvalue < 0 and self.Digitalconditionvalue == 1:
                    self.simSSIPosFbvalueoutlongrawvalue = 0

                else:
                    if self.Digitalconditionvalue == 1:
                          self.simSSIPosFbvalueoutlongrawvalue = SSIPosFbvalueoutlongrawvalue



            writegeneral.writesymbolvalue(self.RodSidePresstag, self.simrodsidepressoutrawvalue, 'S7WLWord')
            writegeneral.writesymbolvalue(self.PistonSidePresstag, self.simpistonsidepressoutrawvalue, 'S7WLWord')
            writegeneral.writesymbolvalue(self.SSIPosFbtag, self.simSSIPosFbvalueoutlongrawvalue, 'S7WLDWord')
            writegeneral.writesymbolvalue(self.positiontag, self.positionrawvalue1, 'S7WLWord')
            sleep(1)


            sta_con_plc.disconnect()


        except Exception as e:
            log_exception(e)
            level = logging.INFO
            messege = "self.devicename" + ":" + " Exception rasied(Encoderprocess): " + str(e.args) + str(e)
            logger.log(level, messege)



    @property
    def areaname(self):
        return self.areatag

    @property
    def speedsetpoint(self):
        return self._speedsetpoint

    @speedsetpoint.setter
    def speedsetpoint(self, value):
        if value != -1:
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












