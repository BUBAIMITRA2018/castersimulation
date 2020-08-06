
from event_V2 import *

from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
from time import *

__all__ = ['Fn_ControlValves']

class Fn_ControlValves(Eventmanager):
    def __init__(self,com,df,idxNo,filename ):
        self._idxNo =idxNo
        self.devicename = df.iloc[self._idxNo, 0]
        self.filename = filename
        self.com = com
        self.df = df
        self._sp = 0
        self.setup()
        self.mylock = threading.Lock()
        self.initilizedigitalinput()
        super().__init__(lambda: self.controlvalveprocess())


    def setup(self):
        try:
            self.area = self.df.iloc[self._idxNo,3]

            self.sp = str(self.df.iloc[self._idxNo, 4])

            self.pv = str(self.df.iloc[self._idxNo, 5])

            self.delaytime = self.df.iloc[self._idxNo, 6]

            self.highpvvalue = int(self.df.iloc[self._idxNo, 7])

            self.lowpvvalue = int(self.df.iloc[self._idxNo, 8])

            self.type = str(self.df.iloc[self._idxNo, 9])

            self.con1 = str(self.df.iloc[self._idxNo, 10])

            self.con2 = str(self.df.iloc[self._idxNo, 11])

            self.postion1 = str(self.df.iloc[self._idxNo, 12])

            self.postion2 = str(self.df.iloc[self._idxNo, 13])
            




        except Exception as e:

            log_exception(e)

    def initilizedigitalinput(self):
        client = Communication()
        sta_con_plc = client.opc_client_connect(self.filename)
        readgeneral = ReadGeneral(sta_con_plc)
        writegeneral = WriteGeneral(sta_con_plc)

        writegeneral.writesymbolvalue(self.pv, 0, 'S7WLWord')

        sta_con_plc.disconnect()

    def controlvalveprocess(self):

        try:


            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)


            if len(self.sp) > 0 :


                if(self.type == 'Positive'):

                    self.currentvalue = readgeneral.readsymbolvalue(self.pv, 'S7WLWord', 'PE')
                    self.spvalue = (readgeneral.readsymbolvalue(self.sp, 'S7WLWord', 'PA'))
                    self.con1value = (readgeneral.readsymbolvalue(self.con1, 'S7WLBit', 'PA'))
                    self.con2value = (readgeneral.readsymbolvalue(self.con2, 'S7WLBit', 'PA'))


                    # rawspvalue = self.scalingconvtoraw(self.spvalue, self.highpvvalue, self.lowpvvalue)
                    rawspvalue = self.spvalue

                    if rawspvalue > self.currentvalue and (self.con1value or self.con2value) :
                        diff = rawspvalue - self.currentvalue
                        count = .3 * diff
                        self.currentvalue = self.currentvalue + count
                        writegeneral.writesymbolvalue(self.pv, self.currentvalue, 'S7WLWord')

                    if rawspvalue < self.currentvalue:
                        diff = self.currentvalue - rawspvalue
                        count1 = .3 * diff
                        self.currentvalue = self.currentvalue - count1
                        writegeneral.writesymbolvalue(self.pv, self.currentvalue, 'S7WLWord')

                if(self.type == 'newfuction'):


                    self.currentvalue = readgeneral.readsymbolvalue(self.pv, 'S7WLWord', 'PE')
                    self.spvalue = (readgeneral.readsymbolvalue(self.sp, 'S7WLWord', 'PA'))
                    self.con1value = (readgeneral.readsymbolvalue(self.con1, 'S7WLBit', 'PA'))
                    self.con2value = (readgeneral.readsymbolvalue(self.con2, 'S7WLBit', 'PA'))
                    if len(self.postion1)>3:
                          self.positionvalue1 = (readgeneral.readsymbolvalue(self.postion1, 'S7WLDWord', 'PE'))

                    if len(self.postion2)>3:
                          self.positionvalue2 = (readgeneral.readsymbolvalue(self.postion2, 'S7WLDWord', 'PE'))


                    rawspvalue = self.spvalue


                    if rawspvalue > self.currentvalue and self.con1value:


                        diff = rawspvalue - self.currentvalue
                        count = .3 * diff
                        self.currentvalue1 = self.currentvalue + count

                        writegeneral.writesymbolvalue(self.pv, self.currentvalue1, 'S7WLWord')

                    if rawspvalue < self.currentvalue  and self.con1value:
                        diff = self.currentvalue - rawspvalue
                        count1 = .3 * diff
                        self.currentvalue = self.currentvalue - count1
                        writegeneral.writesymbolvalue(self.pv, self.currentvalue, 'S7WLWord')

                    if not self.con1value:
                        writegeneral.writesymbolvalue(self.pv, 0, 'S7WLWord')

                    if len(self.postion1)>3:
                        if self.con1value == 1 and self.con2value == 0 and self.positionvalue1 >= 0 and self.positionvalue1 < 60000:
                            self.currentposvalue1 = self.positionvalue1 + 5000
                            writegeneral.writesymbolvalue(self.postion1, self.currentposvalue1, 'S7WLDWord')

                        if self.con1value == 0 and self.con2value == 1 and self.positionvalue1> 0 and self.positionvalue1 <= 60000:
                            self.currentposvalue1 = self.positionvalue1 - 5000
                            writegeneral.writesymbolvalue(self.postion1, self.currentposvalue1 , 'S7WLDWord')

                        if self.con1value==0 and self.con2value ==0 and rawspvalue <=0:
                            writegeneral.writesymbolvalue(self.postion1, 0, 'S7WLDWord')


                    else:
                        pass

                    if len(self.postion2)>3:
                        print("heheheheheheheheheheheheh")
                        if self.con1value == 1 and self.con2value == 0 and self.positionvalue2 >= 0 and self.positionvalue2 < 60000:
                            print('ther postion is ',self.positionvalue2)
                            self.currentposvalue2 = self.positionvalue2 + 5000
                            print('ther postion is ', self.currentposvalue2)
                            writegeneral.writesymbolvalue(self.postion2, self.currentposvalue2, 'S7WLDWord')

                        if self.con1value == 0 and self.con2value == 1 and self.positionvalue2> 0 and self.positionvalue2 <= 60000:
                            self.currentposvalue2 = self.positionvalue2 - 5000
                            writegeneral.writesymbolvalue(self.postion2, self.currentposvalue2 , 'S7WLDWord')

                        if self.con1value==0 and self.con2value ==0 and rawspvalue <=0:
                            writegeneral.writesymbolvalue(self.postion2, 0, 'S7WLDWord')

                    else:
                        pass






            sta_con_plc.disconnect()


        except Exception as e:
            log_exception(e)
            level = logging.ERROR
            messege = 'Event:' + "ControlValve" + str(e.args)
            logger.log(level, messege)





    def scalingconvtoraw(self, val, highlimit, lowlimit):
        rawvalue = int((val * 27648) / (highlimit - lowlimit))
        # print(rawvalue)
        return rawvalue

    @property
    def processval(self):
        pv = float((self.currentvalue/27648)*(self.highpvvalue - self.lowpvvalue))
        print(pv)
        return  pv



    @property
    def setpoint(self):
        return self._sp

    @setpoint.setter
    def setpoint(self, value):

        if value != self._sp:
            print("setpointvalue is", value)
            print("current value is", self._sp)
            super().fire()
            self._sp = value

    @property
    def areaname(self):
        return self.area


    def readalltags(self):
        n = 3
        row, col = self.df.shape
        print(col)
        while n < col:
            data = self.df.iloc[self._idxNo, n]
            yield data,n
            n = n + 1
