from logger import *
from fn_railswitch1 import *
import logging


logger = logging.getLogger("main.log")

class Cal_AllRailSwitch1:
    def __init__(self,filename):
        self.filename = filename
        self.listofrailswitch = []
        self.listofrailswitcharea = []
        self.devicelistperarea = [[]]
        self.setup()

    def setup(self):
        try:
             self.railswitchs1 = Fn_RailSwitch1(self.filename)




        except Exception as e:
            log_exception(e)
            level = logging.ERROR
            messege = 'Event:' + "callallmotor2D" + str(e.args)
            logger.log(level, messege)






    @property
    def railswitchobject1(self):
        return self.railswitchs1
