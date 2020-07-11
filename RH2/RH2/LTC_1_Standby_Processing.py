
from observable import *
from clientcomm_v1 import *
from readgeneral_v2 import *

logger = logging.getLogger("main.log")




class LTC1StandbyProcess:
    def __init__(self,alldevices):
        self.alldevices = alldevices


    def process(self):
        self.alldevices.CallStandbyLTC1.ltc1standbyobject.process()












