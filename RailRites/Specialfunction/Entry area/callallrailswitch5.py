from logger import *
from fn_railswitch5 import *
import logging


logger = logging.getLogger("main.log")

class Cal_AllRailSwitch5:
    def __init__(self,filename):
        self.filename = filename
        self.listofrailswitch = []
        self.listofrailswitcharea = []
        self.devicelistperarea = [[]]
        self.setup()

    def setup(self):
        try:
             self.railswitchs5 = Fn_RailSwitch5(self.filename)




        except Exception as e:
            log_exception(e)
            level = logging.ERROR
            messege = 'Event:' + "callallmotor2D" + str(e.args)
            logger.log(level, messege)






    @property
    def railswitchobject5(self):
        return self.railswitchs5
