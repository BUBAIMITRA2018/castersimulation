
from callalldummybar import *


logger = logging.getLogger("main.log")



class alldummybarprocess:
    def __init__(self,filename):
        self.filename = filename
        self.dummybar = Cal_AllDummybar(self.filename)

    def process(self):
        self.dummybar.dummybar1.process()


















