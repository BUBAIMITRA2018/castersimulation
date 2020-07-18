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

            self.TundishCar1_Pos = str('db1430.dbd176')
            self.TundishCar1_limitsw1 = str(611.2)
            self.TundishCar1_limitsw2 = str(611.1)
            self.TundishCar1_limitsw3 = str(611.0)
            self.TundishCar1_limitsw4 = str(611.3)
            self.TundishCar1_limitsw5 = str(611.4)
            self.TundishCar1_limitsw6 = str(611.5)




        except Exception as e:
            level = logging.ERROR
            messege = "TundishCar" + "" + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)




    def initilizedigitalinput(self):

        client = Communication()
        sta_con_plc = client.opc_client_connect(self.filename)
        readgeneral = ReadGeneral(sta_con_plc)
        writegeneral = WriteGeneral(sta_con_plc)

        writegeneral.writesymbolvalue(self.TundishCar1_limitsw4, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.TundishCar1_limitsw5, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.TundishCar1_limitsw6, 1, 'S7WLBit')

        writegeneral.writesymbolvalue(self.TundishCar1_limitsw1, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.TundishCar1_limitsw2, 0, 'S7WLBit')
        writegeneral.writesymbolvalue(self.TundishCar1_limitsw3, 1, 'S7WLBit')

        sta_con_plc.disconnect()






    def process(self):

        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)

            self.tundishCar1_Pos_value = readgeneral.readDBvalue(self.TundishCar1_Pos, 'S7WLReal')

            print("turdishcar2 position value ", self.tundishCar1_Pos_value)

            if self.tundishCar1_Pos_value < 0:
                writegeneral.writesymbolvalue(self.TundishCar1_limitsw4, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.TundishCar1_limitsw5, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.TundishCar1_limitsw6, 1, 'S7WLBit')

                time.sleep(30)
                writegeneral.writesymbolvalue(self.TundishCar1_limitsw1, 1, 'S7WLBit')
                time.sleep(5)
                writegeneral.writesymbolvalue(self.TundishCar1_limitsw2, 1, 'S7WLBit')
                time.sleep(5)
                writegeneral.writesymbolvalue(self.TundishCar1_limitsw3, 0, 'S7WLBit')

            if self.tundishCar1_Pos_value > 0:
                writegeneral.writesymbolvalue(self.TundishCar1_limitsw1, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.TundishCar1_limitsw2, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.TundishCar1_limitsw3, 1, 'S7WLBit')

                time.sleep(30)
                writegeneral.writesymbolvalue(self.TundishCar1_limitsw4, 1, 'S7WLBit')
                time.sleep(5)
                writegeneral.writesymbolvalue(self.TundishCar1_limitsw5, 1, 'S7WLBit')
                time.sleep(5)
                writegeneral.writesymbolvalue(self.TundishCar1_limitsw6, 0, 'S7WLBit')

            sta_con_plc.disconnect()


        except Exception as e:

            level = logging.INFO
            messege = "TundishCar" + ":" + " Exception rasied(process): " + str(e.args) + str(e)
            logger.log(level, messege)









