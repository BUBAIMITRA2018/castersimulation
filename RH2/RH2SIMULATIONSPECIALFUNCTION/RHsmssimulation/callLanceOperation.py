from logger import *
from  fn_LANCE_Operation import *
import logging

logger = logging.getLogger("main.log")


class Cal_Lanceoperation:

    def __init__(self,filename):
        self.filename = filename
        self.setup()

    def setup(self):
        try:

            self.Lance = Fn_LANCEsignal( self.filename)

        except Exception as e :
            log_exception(e)
            level = logging.ERROR
            messege = 'Event:' + "LTC1Standby" + str(e.args)
            logger.log(level, messege)



    @property
    def lanceobject(self):
        return self.Lance



