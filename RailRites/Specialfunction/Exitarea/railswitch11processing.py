from clientcomm_v1 import *

logger = logging.getLogger("main.log")




class railswitchProcess11:
    def __init__(self,alldevices):
        self.alldevices = alldevices


    def process(self):
        self.alldevices.allrailswitch11.railswitchobject11.process()
