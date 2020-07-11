from logger import *
from  fn_LTC1_StandbyOperation import *
import logging




logger = logging.getLogger("main.log")


class Cal_LTC1Standby:

    def __init__(self,filename):
        self.filename = filename
        self.setup()

    def setup(self):
        try:

            self.LTC1standby = Fn_LTC1Standysignal( self.filename)

        except Exception as e :
            log_exception(e)
            level = logging.ERROR
            messege = 'Event:' + "LanceStandby" + str(e.args)
            logger.log(level, messege)



    @property
    def ltc1standbyobject(self):
        return self.LTC1standby



