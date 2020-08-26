from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import  time
from time import sleep
import logging
import threading
logger = logging.getLogger("main.log")

__all__ = ['Fn_TundishCar1']





class Fn_TundishCar1():

    def __init__(self,filename):
        self.filename = filename
        self.setup()
        self.initilizedigitalinput()




    def setup(self):
        try:

            self.Actualposition = str('db3666.dbd50')


            self.TundishCar1_heatovt_cmd = str('db3666.dbx42.0')
            self.TundishCar1_heatovt_limitsw = str(610.0)

            self.TundishCar1_heatstop_cmd = str('db3666.dbx42.1')

            self.TundishCar1_heatstop_limitsw = str(610.1)

            self.TundishCar1_heatslow_cmd = str('db3666.dbx42.2')
            self.TundishCar1_heatslow_limitsw = str(610.2)



            self.TundishCar1_castovt_cmd = str('db3666.dbx42.6')
            self.TundishCar1_castovt_limitsw = str(610.5)

            self.TundishCar1_caststop_cmd = str('db3666.dbx42.5')
            self.TundishCar1_caststop_limitsw = str(610.4)

            self.TundishCar1_castslow_cmd = str('db3666.dbx42.4')
            self.TundishCar1_castslow_limitsw = str(610.3)








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

            writegeneral.writesymbolvalue(self.TundishCar1_heatovt_limitsw, 1, 'S7WLBit')

            writegeneral.writesymbolvalue(self.TundishCar1_castovt_limitsw, 1, 'S7WLBit')

            sta_con_plc.disconnect()

        except Exception as e:
            level = logging.INFO
            messege = "TundishCar" + ":" + " Exception rasied(initilization): " + str(e.args) + str(e)
            logger.log(level, messege)

    def process(self):


        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)


            self.actualpostion = readgeneral.readDBvalue(self.Actualposition, 'S7WLReal')

            # Heat position



            if  self.actualpostion > 13000:

                writegeneral.writesymbolvalue(self.TundishCar1_heatovt_limitsw, 0, 'S7WLBit')

            else:
                writegeneral.writesymbolvalue(self.TundishCar1_heatovt_limitsw, 1, 'S7WLBit')




            if  self.actualpostion > 11390 and self.actualpostion < 13100 :
                writegeneral.writesymbolvalue(self.TundishCar1_heatstop_limitsw, 1, 'S7WLBit')

            else:
                writegeneral.writesymbolvalue(self.TundishCar1_heatstop_limitsw, 0, 'S7WLBit')



            if self.actualpostion > 11000 and self.actualpostion < 12200:
                writegeneral.writesymbolvalue(self.TundishCar1_heatslow_limitsw, 1, 'S7WLBit')

            else:
                writegeneral.writesymbolvalue(self.TundishCar1_heatslow_limitsw, 0, 'S7WLBit')


                  # Cast position



            if self.actualpostion < -50:
                writegeneral.writesymbolvalue(self.TundishCar1_castovt_limitsw, 0, 'S7WLBit')
            else:
                writegeneral.writesymbolvalue(self.TundishCar1_castovt_limitsw, 1, 'S7WLBit')


            if self.actualpostion < 120 and self.actualpostion > -100:
                writegeneral.writesymbolvalue(self.TundishCar1_caststop_limitsw, 1, 'S7WLBit')
            else:
                writegeneral.writesymbolvalue(self.TundishCar1_caststop_limitsw, 0, 'S7WLBit')



            if self.actualpostion < 800 and self.actualpostion > 50:
                writegeneral.writesymbolvalue(self.TundishCar1_castslow_limitsw, 1, 'S7WLBit')

            else:
                writegeneral.writesymbolvalue(self.TundishCar1_castslow_limitsw, 0, 'S7WLBit')



            #
            # heatovrtravel = readgeneral.readDBvalue(self.TundishCar1_heatovt_cmd, 'S7WLBit')
            # writegeneral.writesymbolvalue(self.TundishCar1_heatovt_limitsw, heatovrtravel, 'S7WLBit')
            #
            # heatstop = readgeneral.readDBvalue(self.TundishCar1_heatstop_limitsw, 'S7WLBit')
            # writegeneral.writesymbolvalue(self.TundishCar1_heatstop_limitsw, heatstop, 'S7WLBit')
            #
            # heatslow = readgeneral.readDBvalue(self.TundishCar1_heatslow_cmd, 'S7WLBit')
            # writegeneral.writesymbolvalue(self.TundishCar1_heatslow_limitsw, heatslow, 'S7WLBit')
            #
            #
            # # Cast
            #
            # castovrtravel = readgeneral.readDBvalue(self.TundishCar1_castovt_cmd, 'S7WLBit')
            # writegeneral.writesymbolvalue(self.TundishCar1_castovt_limitsw, castovrtravel, 'S7WLBit')
            #
            # caststop = readgeneral.readDBvalue(self.TundishCar1_caststop_limitsw, 'S7WLBit')
            # writegeneral.writesymbolvalue(self.TundishCar1_caststop_limitsw, caststop, 'S7WLBit')
            #
            # castslow = readgeneral.readDBvalue(self.TundishCar1_castslow_cmd, 'S7WLBit')
            # writegeneral.writesymbolvalue(self.TundishCar1_castslow_limitsw, castslow, 'S7WLBit')



            sta_con_plc.disconnect()


        except Exception as e:

            level = logging.INFO
            messege = "TundishCar" + ":" + " Exception rasied(process): " + str(e.args) + str(e)
            logger.log(level, messege)









