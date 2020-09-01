from clientcomm_v1 import *

logger = logging.getLogger("main.log")




class railswitchProcess4:
    def __init__(self,alldevices):
        self.alldevices = alldevices


    def process(self):
        self.alldevices.allrailswitch4.railswitchobject4.process()
