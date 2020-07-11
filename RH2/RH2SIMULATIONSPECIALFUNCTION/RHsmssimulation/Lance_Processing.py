

from clientcomm_v1 import *


logger = logging.getLogger("main.log")




class LanceProcess:
    def __init__(self,alldevices):
        self.alldevices = alldevices


    def process(self):
        self.alldevices.CallLance.lanceobject.process()












