from logger import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
from clientcomm_v1 import *
import logging
logger = logging.getLogger("main.log")

__all__ = ['Fn_Shear_Angel_Encoder']

class BreakOpenCmdObserver:
    def __init__(self, observable):
        observable.register_observer(self)



class Fn_Shear_Angel_Encoder():

    def __init__(self,filename):
        self.devicename = 'Shear Angel_Encoder'
        self.filename = filename
        self._breakopencmd = False
        self._breakonFB = False
        self._speedsetpoint = False
        self._encodervalue = 0
        self.speedSP_val = 0
        self.encoderoutputtag = ''
        self.setup()
        self.initilizedigitalinput()




    def setup(self):
        try:

            self.areatag = str(621.5)
            self.speedFB = str('db22.dbd0')
            self.encoderoutputtag = str(3214)
            self.mtrnominalSpd = int(1)
            self.plcscancycle = float(1)
            self.driveEngg = int(1)
            self.kval = int(27648)
            self.encodertype = str('absolute')
            self.resolution = int(60)

        except Exception as e:
            level = logging.ERROR
            messege = "Shear Angel_Encoder" + self.devicename + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)



    def initilizedigitalinput(self):

        client = Communication()
        sta_con_plc = client.opc_client_connect(self.filename)
        readgeneral = ReadGeneral(sta_con_plc)
        writegeneral = WriteGeneral(sta_con_plc)

        if len(self.encoderoutputtag) > 3:
            writegeneral.writesymbolvalue(self.encoderoutputtag, 0, 'S7WLWord')
            level = logging.INFO
            messege = self.devicename + ":" + self.encoderoutputtag + " is trigger by 0"
            logger.log(level, messege)


        sta_con_plc.disconnect()


    def encoderprocess(self):


        try:

            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)

            if self.encodertype == "incremental":

                self.drivespeedfbvalue = readgeneral.readDBvalue(self.speedFB, 'S7WLReal')

                currentencodervalue = readgeneral.readsymbolvalue(self.encoderoutputtag, 'S7WLWord', 'PE')

                self._encodervaluerate = int(
                    (self.drivespeedfbvalue * self.mtrnominalSpd * self.plcscancycle * self.resolution) / (
                            self.driveEngg * 60)) * self.kval

                if self.drivespeedfbvalue != 0.0:

                    nextencodervalue = currentencodervalue + self._encodervaluerate

                    print("next value is ", nextencodervalue)

                    if nextencodervalue > 15000:
                        writegeneral.writesymbolvalue(self.encoderoutputtag, 32000, 'S7WLWord')
                    else:
                        writegeneral.writesymbolvalue(self.encoderoutputtag, nextencodervalue, 'S7WLWord')

                    if nextencodervalue <= -15000.00:
                        writegeneral.writesymbolvalue(self.encoderoutputtag, 32000, 'S7WLWord')
                    else:
                        writegeneral.writesymbolvalue(self.encoderoutputtag, nextencodervalue, 'S7WLWord')

            if self.encodertype == "absolute":

                currentencodervalue = readgeneral.readsymbolvalue(self.encoderoutputtag, 'S7WLWord', 'PE')

                self.drivespeedfbvalue = readgeneral.readDBvalue(self.speedFB, 'S7WLReal')

                self._encodervaluerate = int(
                    (self.drivespeedfbvalue * self.mtrnominalSpd * self.plcscancycle * self.resolution) / (
                            self.driveEngg * 60)) * self.kval

                if currentencodervalue > 27648:
                    writegeneral.writesymbolvalue(self.encoderoutputtag, 27648, 'S7WLWord')

                if currentencodervalue < 0:
                    writegeneral.writesymbolvalue(self.encoderoutputtag, 0, 'S7WLWord')

                if self.drivespeedfbvalue > 0.0:

                    if currentencodervalue < 27648:
                        nextencodervalue = currentencodervalue + self._encodervaluerate
                        writegeneral.writesymbolvalue(self.encoderoutputtag, nextencodervalue, 'S7WLWord')

                if self.drivespeedfbvalue < 0.0:

                    if currentencodervalue > 0:
                        nextencodervalue = currentencodervalue + self._encodervaluerate
                        writegeneral.writesymbolvalue(self.encoderoutputtag, nextencodervalue, 'S7WLWord')

            sta_con_plc.disconnect()





        except Exception as e:
            log_exception(e)
            level = logging.INFO
            messege = self.devicename + ":" + " Exception rasied(Encoderprocess): " + str(e.args) + str(e)
            logger.log(level, messege)



    @property
    def areaname(self):
        return self.areatag











