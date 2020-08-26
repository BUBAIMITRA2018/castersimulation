from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import  time
from time import sleep
import logging
import threading
logger = logging.getLogger("main.log")

__all__ = ['Fn_TundishCar2']





class Fn_TundishCar2():

    def __init__(self,filename):
        self.filename = filename
        self.setup()
        self.initilizedigitalinput()




    def setup(self):
        try:

            self.Actualposition = str('db3752.dbd50')


            self.TundishCar2_heatovt_limitsw = str(611.0)

            self.TundishCar2_heatstop_limitsw = str(611.1)
            self.TundishCar2_heatslow_limitsw = str(611.2)

            self.TundishCar2_castovt_limitsw = str(611.5)
            self.TundishCar2_caststop_limitsw = str(611.4)
            self.TundishCar2_castslow_limitsw = str(611.3)





        except Exception as e:
            level = logging.ERROR
            messege = "TundishCar" + "" + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)




    def initilizedigitalinput(self):
        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)

            writegeneral.writesymbolvalue(self.TundishCar2_heatovt_limitsw, 1, 'S7WLBit')

            writegeneral.writesymbolvalue(self.TundishCar2_castovt_limitsw, 1, 'S7WLBit')

            sta_con_plc.disconnect()

        except Exception as e:

            level = logging.INFO
            messege = "TundishCar2" + ":" + " Exception rasied(initilization): " + str(e.args) + str(e)
            logger.log(level, messege)






    def process(self):

        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)

            self.actualpostion = readgeneral.readDBvalue(self.Actualposition, 'S7WLReal')

            # Heat position

            if self.actualpostion > 10075:

                writegeneral.writesymbolvalue(self.TundishCar2_heatovt_limitsw, 0, 'S7WLBit')

            else:
                writegeneral.writesymbolvalue(self.TundishCar2_heatovt_limitsw, 1, 'S7WLBit')

            if self.actualpostion > 9905 and self.actualpostion < 10200:
                writegeneral.writesymbolvalue(self.TundishCar2_heatstop_limitsw, 1, 'S7WLBit')

            else:
                writegeneral.writesymbolvalue(self.TundishCar2_heatstop_limitsw, 0, 'S7WLBit')

            if self.actualpostion > 8500 and self.actualpostion < 10000:
                writegeneral.writesymbolvalue(self.TundishCar2_heatslow_limitsw, 1, 'S7WLBit')

            else:
                writegeneral.writesymbolvalue(self.TundishCar2_heatslow_limitsw, 0, 'S7WLBit')

                # Cast position

            if self.actualpostion < -50:
                writegeneral.writesymbolvalue(self.TundishCar2_castovt_limitsw, 0, 'S7WLBit')
            else:
                writegeneral.writesymbolvalue(self.TundishCar2_castovt_limitsw, 1, 'S7WLBit')

            if self.actualpostion < 120 and self.actualpostion > -100:
                writegeneral.writesymbolvalue(self.TundishCar2_caststop_limitsw, 1, 'S7WLBit')
            else:
                writegeneral.writesymbolvalue(self.TundishCar2_caststop_limitsw, 0, 'S7WLBit')

            if self.actualpostion < 800 and self.actualpostion > 50:
                writegeneral.writesymbolvalue(self.TundishCar2_castslow_limitsw, 1, 'S7WLBit')

            else:
                writegeneral.writesymbolvalue(self.TundishCar2_castslow_limitsw, 0, 'S7WLBit')

            sta_con_plc.disconnect()


        except Exception as e:

            level = logging.INFO
            messege = "TundishCar" + ":" + " Exception rasied(process): " + str(e.args) + str(e)
            logger.log(level, messege)









