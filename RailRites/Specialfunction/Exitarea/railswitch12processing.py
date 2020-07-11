from clientcomm_v1 import *

logger = logging.getLogger("main.log")




class railswitchProcess12:
    def __init__(self,alldevices):
        self.alldevices = alldevices


    def process(self):
        self.alldevices.allrailswitch12.railswitchobject12.process()
