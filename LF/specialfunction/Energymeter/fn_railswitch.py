from logger import *
from event_V2 import *
from time import sleep
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import logging
import  general

logger = logging.getLogger("main.log")

__all__ = ['Fn_RailSwitch']


class Fn_RailSwitch(Eventmanager):



    def __init__(self,filename):
        self.filename = filename
        # self.count = 0
        self._fwdlimitswtvalue = False
        self._revlimitswtvalue = False
        # self._fwdrunFBvalue = False
        # self._revrunFBvalue = False
        self.setup()
        self.initilizedigitalinput()
        super().__init__(lambda: self.process())

    def setup(self):
        try:

            self.primaryvoltage1 = str(3000)
            self.primaryvoltage2 = str(3004)
            self.primaryvoltage3 = str(3008)
            self.primarycurrent1 = str(3012)
            self.primarycurrent2 = str(3016)
            self.primarycurrent3 = str(3020)
            self.secondaryvoltage1 = str(3040)
            self.secondaryvoltage2 = str(3044)
            self.secondaryvoltage3 = str(3048)
            self.secondarycurrent1 = str(3052)
            self.secondarycurrent2 = str(3056)
            self.secondarycurrent3 = str(3060)
            self.activepower = str(3024)
            self.reactivepower = str(3028)
            self.powerfactor = str(2546)
            self.energy = str(3036)
            self.fcbclose = str(411.6)
            self.electrodetop = str(411.7)
            self.tapnumber = str(2202)
            self.tapnumberpv = str(2382)

        except Exception as e:
            level = logging.ERROR
            messege = "FN_MOTOR2D" + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)



    def initilizedigitalinput(self):
        print("initialied")


    def process(self):
        print("i m working here")

        global active_power
        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)
            self.tapnumbervalue = readgeneral.readsymbolvalue(self.tapnumber, 'S7WLWord', "PA")
            self.tapnumberpvvalue = readgeneral.readsymbolvalue(self.tapnumberpv, 'S7WLWord', "PE")
            self.electrodetopvalue = readgeneral.readsymbolvalue(self.electrodetop, 'S7WLBit', "PA")
            self.fcbclosevalue = readgeneral.readsymbolvalue(self.fcbclose, 'S7WLBit', "PA")
            print("the tap value is ", self.tapnumbervalue)
            print("the top value ", self.electrodetopvalue)
            print("the fcb valuye is ", self.fcbclosevalue)


            if self.fcbclosevalue == True:
                writegeneral.writesymbolvalue(self.primaryvoltage1, 33000, "S7WLDWord")
                writegeneral.writesymbolvalue(self.primaryvoltage2, 33000, "S7WLDWord")
                writegeneral.writesymbolvalue(self.primaryvoltage3, 33000, "S7WLDWord")
                writegeneral.writesymbolvalue(self.primarycurrent1, 5, "S7WLDWord")
                writegeneral.writesymbolvalue(self.primarycurrent2, 5, "S7WLDWord")
                writegeneral.writesymbolvalue(self.primarycurrent3, 5, "S7WLDWord")
                writegeneral.writesymbolvalue(self.powerfactor, 8, "S7WLWord")
            else:
                writegeneral.writesymbolvalue(self.primaryvoltage1, 0, "S7WLDWord")
                writegeneral.writesymbolvalue(self.primaryvoltage2, 0, "S7WLDWord")
                writegeneral.writesymbolvalue(self.primaryvoltage3, 0, "S7WLDWord")
                writegeneral.writesymbolvalue(self.primarycurrent1, 0, "S7WLDWord")
                writegeneral.writesymbolvalue(self.primarycurrent2,0, "S7WLDWord")
                writegeneral.writesymbolvalue(self.primarycurrent3, 0, "S7WLDWord")
                writegeneral.writesymbolvalue(self.powerfactor, 0, "S7WLWord")



            if self.tapnumbervalue > self.tapnumberpvvalue :
                count = 1
                self.tapnumberpvvalue= self.tapnumberpvvalue+ count
                writegeneral.writesymbolvalue(self.tapnumberpv, self.tapnumberpvvalue, 'S7WLWord')

            if self.tapnumbervalue < self.tapnumberpvvalue :
                count = 1
                self.tapnumberpvvalue = self.tapnumberpvvalue - count
                writegeneral.writesymbolvalue(self.tapnumberpv, self.tapnumberpvvalue, 'S7WLWord')


            print("the tap nummveris ",self.tapnumberpvvalue)


            if self.tapnumberpvvalue == 1 and self.fcbclosevalue and self.electrodetopvalue:
                seconday_voltage = 390
                seconday_current = 50810
                active_power = seconday_voltage * seconday_current * .8
                reactive_power = seconday_voltage * seconday_current * .6
                writegeneral.writesymbolvalue(self.secondaryvoltage1, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondaryvoltage2, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondaryvoltage3, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent1, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent2, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent3, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.activepower, active_power, "S7WLDWord")
                writegeneral.writesymbolvalue(self.reactivepower, reactive_power, "S7WLDWord")

            if self.tapnumberpvvalue == 2 and self.fcbclosevalue and self.electrodetopvalue:
                seconday_voltage = 409
                seconday_current = 50810
                active_power = seconday_voltage * seconday_current * .8
                reactive_power = seconday_voltage * seconday_current * .6
                writegeneral.writesymbolvalue(self.secondaryvoltage1, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondaryvoltage2, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondaryvoltage3, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent1, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent2, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent3, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.activepower, active_power, "S7WLDWord")
                writegeneral.writesymbolvalue(self.reactivepower, reactive_power, "S7WLDWord")

            if self.tapnumberpvvalue == 3 and self.fcbclosevalue and self.electrodetopvalue:
                print("heheheheheheheheehehehehehehehehehehhehe")
                seconday_voltage = 423
                seconday_current = 50810
                active_power = seconday_voltage * seconday_current * .8
                reactive_power = seconday_voltage * seconday_current * .6
                writegeneral.writesymbolvalue(self.secondaryvoltage1, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondaryvoltage2, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondaryvoltage3, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent1, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent2, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent3, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.activepower, active_power, "S7WLDWord")
                writegeneral.writesymbolvalue(self.reactivepower, reactive_power, "S7WLDWord")

            if self.tapnumberpvvalue == 4 and self.fcbclosevalue and self.electrodetopvalue:
                seconday_voltage = 439
                seconday_current = 50810
                active_power = seconday_voltage * seconday_current * .8
                reactive_power = seconday_voltage * seconday_current * .6
                writegeneral.writesymbolvalue(self.secondaryvoltage1, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondaryvoltage2, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondaryvoltage3, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent1, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent2, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent3, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.activepower, active_power, "S7WLDWord")
                writegeneral.writesymbolvalue(self.reactivepower, reactive_power, "S7WLDWord")

            if self.tapnumberpvvalue == 5 and self.fcbclosevalue and self.electrodetopvalue:
                seconday_voltage = 456
                seconday_current = 50810
                active_power = seconday_voltage * seconday_current * .8
                reactive_power = seconday_voltage * seconday_current * .6
                writegeneral.writesymbolvalue(self.secondaryvoltage1, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondaryvoltage2, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondaryvoltage3, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent1, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent2, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent3, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.activepower, active_power, "S7WLDWord")
                writegeneral.writesymbolvalue(self.reactivepower, reactive_power, "S7WLDWord")

            if self.tapnumberpvvalue == 6 and self.fcbclosevalue and self.electrodetopvalue:
                seconday_voltage = 474
                seconday_current = 50810
                active_power = seconday_voltage * seconday_current * .8
                reactive_power = seconday_voltage * seconday_current * .6
                writegeneral.writesymbolvalue(self.secondaryvoltage1, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondaryvoltage2, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondaryvoltage3, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent1, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent2, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent3, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.activepower, active_power, "S7WLDWord")
                writegeneral.writesymbolvalue(self.reactivepower, reactive_power, "S7WLDWord")

            if self.tapnumberpvvalue == 7 and self.fcbclosevalue and self.electrodetopvalue:
                seconday_voltage = 494
                seconday_current = 50810
                active_power = seconday_voltage * seconday_current * .8
                reactive_power = seconday_voltage * seconday_current * .6
                writegeneral.writesymbolvalue(self.secondaryvoltage1, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondaryvoltage2, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondaryvoltage3, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent1, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent2, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent3, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.activepower, active_power, "S7WLDWord")
                writegeneral.writesymbolvalue(self.reactivepower, reactive_power, "S7WLDWord")

            if self.tapnumberpvvalue == 8 and self.fcbclosevalue and self.electrodetopvalue:
                seconday_voltage = 515
                seconday_current = 59328
                active_power = seconday_voltage * seconday_current * .8
                reactive_power = seconday_voltage * seconday_current * .6
                writegeneral.writesymbolvalue(self.secondaryvoltage1, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondaryvoltage2, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondaryvoltage3, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent1, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent2, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent3, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.activepower, active_power, "S7WLDWord")
                writegeneral.writesymbolvalue(self.reactivepower, reactive_power, "S7WLDWord")

            if self.tapnumberpvvalue == 9 and self.fcbclosevalue and self.electrodetopvalue:
                seconday_voltage = 538
                seconday_current = 472196
                active_power = seconday_voltage * seconday_current * .8
                reactive_power = seconday_voltage * seconday_current * .6
                writegeneral.writesymbolvalue(self.secondaryvoltage1, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondaryvoltage2, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondaryvoltage3, seconday_voltage, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent1, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent2, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent3, seconday_current, "S7WLDWord")
                writegeneral.writesymbolvalue(self.activepower, active_power, "S7WLDWord")
                writegeneral.writesymbolvalue(self.reactivepower, reactive_power, "S7WLDWord")

            if self.fcbclosevalue and self.electrodetopvalue:
                print("hheheheheehhehehehehehheheheheheheheheheh")

                energyvalue = readgeneral.readsymbolvalue(self.energy, "S7WLDWord", "PE")
                energyvalue = energyvalue + (active_power / 3600000)
                print("the energy is", energyvalue)
                writegeneral.writesymbolvalue(self.energy, energyvalue, "S7WLDWord")

            if not self.fcbclosevalue:
                print("heheheheheeheheh")

                writegeneral.writesymbolvalue(self.energy, 0, "S7WLDWord")

            if not self.electrodetopvalue or not self.fcbclosevalue:
                writegeneral.writesymbolvalue(self.activepower, 0, "S7WLDWord")
                writegeneral.writesymbolvalue(self.reactivepower, 0, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondaryvoltage1, 0, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondaryvoltage2, 0, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondaryvoltage3, 0, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent1, 0, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent2, 0, "S7WLDWord")
                writegeneral.writesymbolvalue(self.secondarycurrent3, 0, "S7WLDWord")

            sta_con_plc.disconnect()

        except Exception as e:
            log_exception(e)
            level = logging.INFO
            messege = "FN_RailSwitch" + ":" + " Exception rasied(process): " + str(e.args) + str(e)
            logger.log(level, messege)




