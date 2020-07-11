
from clientcomm_v1 import *


logger = logging.getLogger("main.log")




class LTC2Process:
    def __init__(self,alldevices):
        self.alldevices = alldevices


    def process(self):
        self.alldevices.CallTC2.ltc2object.process()












