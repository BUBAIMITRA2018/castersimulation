from clientcomm_v1 import *

logger = logging.getLogger("main.log")




class railswitchProcess2:
    def __init__(self,alldevices):
        self.alldevices = alldevices


    def process(self):
        self.alldevices.Cal_AllRailSwitch2.railswitchobject2.process()
