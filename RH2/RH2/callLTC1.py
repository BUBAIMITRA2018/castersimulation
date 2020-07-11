from logger import *
from  fn_LTC1_Operation import *
import logging
import threading



logger = logging.getLogger("main.log")


class Cal_LTC1:

    def __init__(self,filename):
        self.filename = filename
        self.setup()

    def setup(self):
        try:

            self.LTC1 = Fn_LTC1signal( self.filename)

        except Exception as e :
            log_exception(e)
            level = logging.ERROR
            messege = 'Event:' + "CallLTC1" + str(e.args)
            logger.log(level, messege)



    @property
    def ltc1object(self):
        return self.LTC1



