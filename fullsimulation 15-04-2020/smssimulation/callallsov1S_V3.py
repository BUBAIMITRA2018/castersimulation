from logger import *
import threading
from fn_sov1S_V3 import *
import logging
import time


setup_logging_to_file("allsov1S.log")
logger = logging.getLogger("main.log")


class Cal_AllSov1S:

    def __init__(self,df,com,filename):
        self.mylock = threading.Lock()
        self.df = df
        self.filename = filename
        self.com = com
        self.logger = logger
        self.listofsov1s = []
        self.listofsov1sarea = []
        self.devicelistperarea = [[]]
        self.setup()


    def setup(self):
        try:

            # Make a lis of area
            self.listofsov1sarea = list(set(self.df['Sub-Area']))

            # Make a lis of devices
            n= 0
            self.listofsov1s.clear()
            while n< len(self.df.index):

                self.df.iloc[n, 0] = Fn_Sov1S(self.com, self.df, n,self.filename)
                self.listofsov1s.append(self.df.iloc[n,0])
                n = n + 1



            for area in self.listofsov1sarea:
                list1 = []
                for item in self.listofsov1s:
                    if str(item.areaname) == str(area):
                        list1.append(item)
                self.devicelistperarea.append(list1)

            keys = self.listofsov1sarea
            values = self.devicelistperarea[1:]
            # Declear empty list
            self.dictionary = dict(zip(keys,values))

        except Exception as e :
            log_exception(e)
            log_exception(e)
            level = logging.ERROR
            messege = 'Event:' + "callallsov1s" + str(e.args)
            logger.log(level, messege)






    @property
    def listofallsov1s(self):
        return self.listofsov1s

    @property
    def listofsov1sareas(self):
        return self.listofsov1sarea

    @property
    def getmotordictionary(self):
        return self.dictionary




