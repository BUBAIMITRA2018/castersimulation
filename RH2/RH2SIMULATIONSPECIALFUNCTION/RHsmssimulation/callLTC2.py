from logger import *
from  fn_LTC2_Operation import *
import logging




logger = logging.getLogger("main.log")


class Cal_LTC2:

    def __init__(self,filename):
        self.filename = filename
        self.setup()

    def setup(self):
        try:

            self.LTC2 = Fn_LTC2signal( self.filename)

        except Exception as e :
            log_exception(e)
            level = logging.ERROR
            messege = 'Event:' + "callLTC2" + str(e.args)
            logger.log(level, messege)



    @property
    def ltc2object(self):
        return self.LTC2



