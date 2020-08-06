
from fn_plc_to_plc_communication import *


import logging

logger = logging.getLogger("main.log")


class Cal_AllPLC2PLCCOMMUNICATION:

    def __init__(self):

        self.setup()


    def setup(self):
        try:
            self.PLC_2_PLC_COMMUNICATION =  Fn_PLC_2_PLC_COMMUNICATION()



        except Exception as e:
            level = logging.ERROR
            messege = 'Event:' + "Cal_AllPLC2PLCCOMMUNICATION" + str(e.args)
            logger.log(level, messege)


    @property
    def plctoplccommunication(self):
        return  self.PLC_2_PLC_COMMUNICATION






