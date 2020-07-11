from logger import *
from fn_railswitch10 import *
import logging


logger = logging.getLogger("main.log")

class Cal_AllRailSwitch10:
    def __init__(self,filename):
        self.filename = filename
        self.listofrailswitch = []
        self.listofrailswitcharea = []
        self.devicelistperarea = [[]]
        self.setup()

    def setup(self):
        try:
             self.railswitchs10 = Fn_RailSwitch10(self.filename)



        except Exception as e:
            log_exception(e)
            level = logging.ERROR
            messege = 'Event:' + "callallmotor2D" + str(e.args)
            logger.log(level, messege)






    @property
    def railswitchobject10(self):
        return self.railswitchs10
