from  fn_dummybar_V3 import  *

import logging


logger = logging.getLogger("main.log")


class Cal_AllDummybar:

    def __init__(self,filename):
        self.filename = filename

    def setup(self):
        try:

            self.Dummybar_1 =  Fn_DummyBar(self.filename)



        except Exception as e:
            level = logging.ERROR
            messege = 'Event:' + "callalldummybar" + str(e.args)
            logger.log(level, messege)



    @property
    def dummybar1(self):
        return self.Dummybar_1


