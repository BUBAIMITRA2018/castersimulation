
from clientcomm_v1 import *

logger = logging.getLogger("main.log")




class railswitchProcess8:
    def __init__(self,alldevices):
        self.alldevices = alldevices


    def process(self):
        self.alldevices.allrailswitch8.railswitchobject8.process()
