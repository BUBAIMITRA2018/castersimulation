from logger import *
from  fn_LTC2_StandbyOperation import *
import logging




logger = logging.getLogger("main.log")


class Cal_LTC2Standby:

    def __init__(self,filename):
        self.filename = filename
        self.setup()

    def setup(self):
        try:

            self.LTC2standby = Fn_LTC2Standbysignal( self.filename)

        except Exception as e :
            log_exception(e)
            level = logging.ERROR
            messege = 'Event:' + "LTC1Standby" + str(e.args)
            logger.log(level, messege)



    @property
    def ltc2standbyobject(self):
        return self.LTC2standby



