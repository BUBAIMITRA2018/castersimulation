from clientcomm_v1 import *

logger = logging.getLogger("main.log")




class railswitchProcess9:
    def __init__(self,alldevices):
        self.alldevices = alldevices


    def process(self):
        self.alldevices.allrailswitch9.railswitchobject9.process()
