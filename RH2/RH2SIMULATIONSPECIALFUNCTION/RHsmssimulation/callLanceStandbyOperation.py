from logger import *
from  fn_LANCE_StandbyOperation import *
import logging

logger = logging.getLogger("main.log")


class Cal_Lancestandbyoperation:

    def __init__(self,filename):
        self.filename = filename
        self.setup()

    def setup(self):
        try:

            self.LanceStandby =Fn_LanceStandbysignal( self.filename)

        except Exception as e :
            log_exception(e)
            level = logging.ERROR
            messege = 'Event:' + "LanceStandby" + str(e.args)
            logger.log(level, messege)



    @property
    def lancestandbyobject(self):
        return self.LanceStandby



