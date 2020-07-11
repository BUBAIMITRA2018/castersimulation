from clientcomm_v1 import *

logger = logging.getLogger("main.log")




class railswitchProcess10:
    def __init__(self,alldevices):
        self.alldevices = alldevices


    def process(self):
        self.alldevices.allrailswitch10.railswitchobject10.process()
