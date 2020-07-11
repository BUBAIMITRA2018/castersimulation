from clientcomm_v1 import *

logger = logging.getLogger("main.log")




class railswitchProcess5:
    def __init__(self,alldevices):
        self.alldevices = alldevices


    def process(self):
        self.alldevices.allrailswitch5.railswitchobject5.process()
