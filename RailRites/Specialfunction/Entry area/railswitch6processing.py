from clientcomm_v1 import *

logger = logging.getLogger("main.log")




class railswitchProcess6:
    def __init__(self,alldevices):
        self.alldevices = alldevices


    def process(self):
        self.alldevices.allrailswitch6.railswitchobject6.process()
