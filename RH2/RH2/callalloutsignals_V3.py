from logger import *
import threading
from fn_outsignal_V3 import *
import logging




logger = logging.getLogger("main.log")


class Cal_AllOutsingnal:

    def __init__(self,df,com,filename):
        self.mylock = threading.Lock()
        self.df = df
        self.filename = filename
        self.com = com
        self.logger = logger
        self.listofdigitalsignal = []
        self.setup()


    def setup(self):
        try:

            # Make a lis of devices
            n= 0
            while n< len(self.df.index):
                self.df.iloc[n, 0] = Fn_outsignal(self.com, self.df, n,self.filename)
                self.listofdigitalsignal.append(self.df.iloc[n,0])
                n = n + 1



        except Exception as e :

            log_exception(e)
            level = logging.ERROR
            messege = 'Event:' + "callallsov1s" + str(e.args)
            logger.log(level, messege)



    @property
    def listofalldigitalsignal(self):
        return self.listofdigitalsignal





