from logger import *
from event_V2 import *
from time import sleep
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import logging
import  general

logger = logging.getLogger("main.log")

__all__ = ['Fn_RailSwitch4']


class Fn_RailSwitch4(Eventmanager):



    def __init__(self,filename):
        self.filename = filename
        self.count = 0
        self._fwdlimitswtvalue = False
        self._revlimitswtvalue = False
        # self._fwdrunFBvalue = False
        # self._revrunFBvalue = False
        self.setup()
        self.initilizedigitalinput()
        super().__init__(lambda: self.process())

    def setup(self):
        try:

            self.speedSP = str(2212)
            self.pitcleaningend = str(600.2)
            self.pitcleaningslow = str(600.5)
            self.tubayend = str(600.0)
            self.tubayslow =str(600.3)
            self.treatment = str(600.1)
            self.pittreatmentslow= str(606.5)
            self.tutreatmentslow = str(600.4)

        except Exception as e:
            level = logging.ERROR
            messege = "FN_MOTOR2D" + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)

    def initilizedigitalinput(self):
       pass
    def process(self):
        print("iwas here in fyction2")

        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)
            self.speedSPvalue = readgeneral.readsymbolvalue(self.speedSP, 'S7WLWord', "PA")
            self.pitcleaningendvalue = readgeneral.readsymbolvalue(self.pitcleaningend, 'S7WLBit', "PE")
            self.pitcleaningslowvalue = readgeneral.readsymbolvalue(self.pitcleaningslow, 'S7WLBit', "PE")
            self.tubayendvalue = readgeneral.readsymbolvalue(self.tubayend, 'S7WLBit', "PE")
            self.tubayslowvalue = readgeneral.readsymbolvalue(self.tubayslow, 'S7WLBit', "PE")
            self.treatmentvalue = readgeneral.readsymbolvalue(self.treatment, 'S7WLBit', "PE")
            self.pittreatmentslowvalue = readgeneral.readsymbolvalue(self.pittreatmentslow, 'S7WLBit', "PE")
            self.tutreatmentslowvalue = readgeneral.readsymbolvalue(self.tutreatmentslow, 'S7WLBit', "PE")

            if self.speedSPvalue > 0:
                if not self.pitcleaningendvalue and not self.pitcleaningslowvalue and not self.pittreatmentslowvalue and not self.tubayendvalue and not self.tubayslowvalue and  not self.tutreatmentslowvalue and not self.treatmentvalue:
                    sleep(10)
                    writegeneral.writesymbolvalue(self.tubayend, 1, 'S7WLBit')

                if self.tubayendvalue:
                    sleep(10)
                    writegeneral.writesymbolvalue(self.tubayend, 0, 'S7WLBit')
                    writegeneral.writesymbolvalue(self.tubayslow, 1, 'S7WLBit')

                if self.tubayslowvalue:
                    sleep(10)
                    writegeneral.writesymbolvalue(self.tubayslow, 0, 'S7WLBit')
                    writegeneral.writesymbolvalue(self.tutreatmentslow, 1, 'S7WLBit')

                if self.tutreatmentslowvalue:
                    sleep(10)
                    writegeneral.writesymbolvalue(self.tutreatmentslow, 0, 'S7WLBit')
                    writegeneral.writesymbolvalue(self.treatment, 1, 'S7WLBit')

                if self.treatmentvalue:
                    sleep(10)
                    writegeneral.writesymbolvalue(self.treatment, 0, 'S7WLBit')
                    writegeneral.writesymbolvalue(self.pittreatmentslow, 1, 'S7WLBit')

                if self.pittreatmentslowvalue:
                    sleep(10)
                    writegeneral.writesymbolvalue(self.pittreatmentslow, 0, 'S7WLBit')
                    writegeneral.writesymbolvalue(self.pitcleaningslow, 1, 'S7WLBit')


                if self.pitcleaningslowvalue:
                    sleep(10)
                    writegeneral.writesymbolvalue(self.pitcleaningslow, 0, 'S7WLBit')
                    writegeneral.writesymbolvalue(self.pitcleaningend, 1, 'S7WLBit')

            if self.speedSPvalue < 0 :

                if not self.pitcleaningendvalue and not self.pitcleaningslowvalue and not self.pittreatmentslowvalue and not self.tubayendvalue and not self.tubayslowvalue and  not self.tutreatmentslowvalue and not self.treatmentvalue:
                    print("teh setpoint is negative")
                    sleep(10)
                    writegeneral.writesymbolvalue(self.pitcleaningend, 1, 'S7WLBit')

                if self.pitcleaningendvalue:
                    sleep(10)
                    writegeneral.writesymbolvalue(self.pitcleaningend, 0, 'S7WLBit')
                    writegeneral.writesymbolvalue(self.pitcleaningslow, 1, 'S7WLBit')

                if self.pitcleaningslowvalue:
                    sleep(10)
                    writegeneral.writesymbolvalue(self.pitcleaningslow, 0, 'S7WLBit')
                    writegeneral.writesymbolvalue(self.pittreatmentslow, 1, 'S7WLBit')

                if self.pittreatmentslowvalue:
                    sleep(10)
                    writegeneral.writesymbolvalue(self.pittreatmentslow, 0, 'S7WLBit')
                    writegeneral.writesymbolvalue(self.treatment, 1, 'S7WLBit')

                if self.treatmentvalue:
                    sleep(10)
                    writegeneral.writesymbolvalue(self.treatment, 0, 'S7WLBit')
                    writegeneral.writesymbolvalue(self.tutreatmentslow, 1, 'S7WLBit')


                if self.tutreatmentslowvalue:
                    sleep(10)
                    writegeneral.writesymbolvalue(self.tutreatmentslow, 0, 'S7WLBit')
                    writegeneral.writesymbolvalue(self.tubayslow, 1, 'S7WLBit')

                if self.tubayslowvalue:
                    sleep(10)
                    writegeneral.writesymbolvalue(self.tubayslow, 0, 'S7WLBit')
                    writegeneral.writesymbolvalue(self.tubayend, 1, 'S7WLBit')

            sta_con_plc.disconnect()

        except Exception as e:
            log_exception(e)
            level = logging.INFO
            messege = "Strand2" + ":" + " Exception rasied(process): " + str(e.args) + str(e)
            logger.log(level, messege)








