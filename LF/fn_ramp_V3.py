from event_V3 import *
from clientcomm_v1 import *
import random
from readgeneral_v2 import *
from writegeneral_v2 import *

logger = logging.getLogger("main.log")

__all__ = ['Fn_Ramp']


class Fn_Ramp(Eventmanager):

    def __init__(self, com, df, idxNo, filename):

        self.filename = filename
        self._idxNo = idxNo
        self.gen = com
        self.devicename = df.iloc[self._idxNo, 0]
        self.df = df
        self.outrawvalue = 0
        self.currentpv = 0

        self.cmdtag1 = ""
        self.cmdtag2 = ""
        self.cmdtag3 = ""
        self.cmdtag3 = ""
        self.cmdtag4 = ""
        self.cmdtag5 = ""
        self.cmdtag6 = ""
        self.cmdtag7 = ""
        self.cmdtag8 = ""
        self.positiverate = 0.0
        self.postivepluse = False
        self.negativerate = 0.0
        self.negativepluse = False
        self._increasecmdvalue = False
        self._decreasecmdvalue = False
        self.setup()
        self.initialization()
        super().__init__(lambda: self.increaserampprocess(), lambda: self.decreaserampprocess())

    def setup(self):
        try:

            for item, col in self.readalltags():

                if col == 3:
                    self.area = str(item)

                if col == 4:
                    self.highlimit = float(item)

                if col == 5:
                    self.lowerlimit = float(item)

                if col == 6:
                    self.val = float(item)

                if col == 7:
                    self.selval = int(item)

                if col == 8:
                    self.outputtag = str(item)

                if col == 9:
                    self.cmdtag1 = str(item)



                if col == 10:
                    self.cmdtag2 = str(item)


                if col == 11:
                    self.cmdtag3 = str(item)



                if col == 12:
                    self.cmdtag4 = str(item)


                if col == 13:
                    self.cmdtag5 = str((item))


                if col == 14:
                    self.cmdtag6 = str(item)



                if col == 15:
                    self.cmdtag7 = str(item)


                if col == 16:
                    self.cmdtag8 = str(item)

                if col == 17:
                    self.setholdingvalue = int(item)

                if col == 18:
                    self.samplingvaluerate = float(item)


        except Exception as e:
            level = logging.ERROR
            messege = 'Event:' + "FN_Ramp" + str(e.args)
            logger.log(level, messege)

    def initialization(self):
        client = Communication()
        sta_con_plc = client.opc_client_connect(self.filename)
        writegeneral = WriteGeneral(sta_con_plc)
        readgeneral = ReadGeneral(sta_con_plc)

        writegeneral.writesymbolvalue(self.outputtag, 0, 'S7WLWord')

        sta_con_plc.disconnect()

    def increaserampprocess(self):

        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            writegeneral = WriteGeneral(sta_con_plc)
            readgeneral = ReadGeneral(sta_con_plc)
            self.negativepluse = False
            self.currentrawvalue = readgeneral.readsymbolvalue(self.outputtag, 'S7WLWord', 'PE')
            print("current raw value", self.currentrawvalue)
            self.currentpv = ((self.highlimit - self.lowerlimit) * (self.currentrawvalue / 27648)) + self.lowerlimit
            self.processrawvalue = int(((self.val - self.lowerlimit) * 27648) / (self.highlimit - self.lowerlimit))

            self.comparevalue = self.val - 0.2

            if not self.postivepluse and (self.val > self.currentpv):
                self.positiverate = (self.val - self.currentpv) / self.samplingvaluerate

                self.postivepluse = True

            if self.comparevalue > self.currentpv:

                currentpv = self.currentpv + self.positiverate

                outrawvalue = self.scaling(currentpv, self.highlimit, self.lowerlimit)

                if outrawvalue > self.processrawvalue:

                    writegeneral.writesymbolvalue(self.outputtag, self.processrawvalue, 'S7WLWord')
                else:
                    writegeneral.writesymbolvalue(self.outputtag, outrawvalue, 'S7WLWord')





                # t1 = threading.Thread(target=self.increasefunction,
                #                       args=(self.currentpv, self.comparevalue, self.processrawvalue, self.positiverate))



                # if (currentpv >= targetsp):
                #     self._increasecmdvalue = True

            #     t1.start()
            #
            # if self.currentpv >= self.val:
            #     self.postivepluse = False

            sta_con_plc.disconnect()


        except Exception as e:
            level = logging.ERROR
            print("error is ", e.args)

            messege = "Ramp" + self.devicename + " Error messege(Increase process)" + str(e.args)
            logger.log(level, messege)

    def decreaserampprocess(self):
        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            writegeneral = WriteGeneral(sta_con_plc)
            readgeneral = ReadGeneral(sta_con_plc)
            self.postivepluse = False
            self.currentrawvalue =  readgeneral.readsymbolvalue(self.outputtag, 'S7WLWord', 'PE')

            self.currentpv = ((self.highlimit - self.lowerlimit) * (self.currentrawvalue /27648)) + self.lowerlimit


            if not self.negativepluse and (self.currentpv > self.lowerlimit):
                self.negativerate = (self.currentpv - self.lowerlimit) / self.samplingvaluerate
                self.negativepluse = True

            if self.lowerlimit < self.currentpv:

                currentpv = self.currentpv - self.negativerate

                outrawvalue = int(((currentpv - self.lowerlimit) * 27648) / (self.highlimit - self.lowerlimit))

                if outrawvalue < 0:
                    writegeneral.writesymbolvalue(self.outputtag, 0, 'S7WLWord')
                else:
                    writegeneral.writesymbolvalue(self.outputtag, outrawvalue, 'S7WLWord')



            sta_con_plc.disconnect()

        except Exception as e:
            level = logging.ERROR
            print("error is ",e.args)

            messege = "Ramp" + self.devicename + " Error messege(Decrease process)" + str(e.args)
            logger.log(level, messege)

    def scaling(self, val, highlimit, lowlimit):
        rawvalue = int((val * 27648) / (highlimit - lowlimit))
        return rawvalue

    @property
    def areaname(self):
        return self.area

    @property
    def processvalue(self):
        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            currentrawvalue = readgeneral.readsymbolvalue(self.outputtag, 'S7WLWord', 'PE')
            sta_con_plc.disconnect()
            return float(((self.highlimit - self.lowerlimit) * (currentrawvalue / 27648)) + self.lowerlimit)

        except Exception as e:
            level = logging.ERROR
            print(e.args)
            messege = "Ramp" + self.devicename + " Error messege(processvalue )" + str(e.args)
            logger.log(level, messege)

    @property
    def setpointvalue(self):
        return (self.val - 0.2)

    @property
    def lowerlimitvalue(self):
        return self.lowerlimit

    @property
    def IncreaseCmd(self):
        return self._increasecmdvalue

    @IncreaseCmd.setter
    def IncreaseCmd(self, value):
        if value == True:
            print(self.devicename + "It is increase executed")
            super().fire1()


    @property
    def DecreaseCmd(self):
        return self._decreasecmdvalue

    @DecreaseCmd.setter
    def DecreaseCmd(self, value):
        if value == True:
            print(self.devicename + "It is decrease executed")
            super().fire2()



    def readalltags(self):
        n = 3
        row, col = self.df.shape
        while n < col:
            data = self.df.iloc[self._idxNo, n]
            yield data, n
            n = n + 1

    def increasefunction(self, currentpv, targetsp, processrawvalue, rate):
        client = Communication()
        sta_con_plc = client.opc_client_connect(self.filename)
        writegeneral = WriteGeneral(sta_con_plc)
        readgeneral = ReadGeneral(sta_con_plc)

        try:
            while (currentpv < targetsp):
                currentpv = currentpv + rate
                outrawvalue = self.scaling(currentpv, self.highlimit, self.lowerlimit)

                if outrawvalue > processrawvalue:

                    writegeneral.writesymbolvalue(self.outputtag, processrawvalue, 'S7WLWord')
                else:
                    writegeneral.writesymbolvalue(self.outputtag, outrawvalue, 'S7WLWord')

                break
            if (currentpv >= targetsp):
                self._increasecmdvalue = True


        except:

            level = logging.ERROR
            messege = "Ramp" + self.devicename + " Error messege(processvalue )" + str(e.args)
            logger.log(level, messege)



        sta_con_plc.disconnect()

    def decreasefunction(self, currentpv, targetsp, rate):
        client = Communication()
        sta_con_plc = client.opc_client_connect(self.filename)
        writegeneral = WriteGeneral(sta_con_plc)
        readgeneral = ReadGeneral(sta_con_plc)

        print("decreased command executed")


        try:

            while (currentpv > targetsp):
                currentpv = currentpv - rate

                outrawvalue = int(((currentpv - self.lowerlimit) * 27648) / (self.highlimit - self.lowerlimit))

                if outrawvalue < 0:
                    writegeneral.writesymbolvalue(self.outputtag, 0, 'S7WLWord')

                else:
                    writegeneral.writesymbolvalue(self.outputtag, outrawvalue, 'S7WLWord')

                break

        except:

            level = logging.ERROR
            messege = "Ramp" + self.devicename + " Error messege(processvalue )" + str(e.args)
            logger.log(level, messege)



        sta_con_plc.close()







