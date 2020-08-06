
from callallplctoplccommunication import *


logger = logging.getLogger("main.log")



class Allplctoplccommunicationprocess:
    def __init__(self):

        self.alldevices =Cal_AllPLC2PLCCOMMUNICATION()


    def plc_to_plc_communication_process(self):
        self.alldevices.plctoplccommunication.process()





















