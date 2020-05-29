from logger import *
from fn_vibrofeeder_V3 import *
import logging
import threading

logger = logging.getLogger("main.log")


class Cal_AllVibroFeeder:

    def __init__(self,df,com,filename):
        self.df = df
        self.mylock = threading.Lock()
        self.com = com
        self.filename = filename
        self.listofvibrofeeder = []
        self.listofvfarea = []
        self.devicelistperarea = [[]]
        self.setup()


    def setup(self):
        try:
            # Make a lis of area
            self.listofvfarea = list(set(self.df['Sub-Area']))

            # Make a lis of devices
            n =0
            self.listofvibrofeeder.clear()
            while n< len(self.df.index):
                self.df.iloc[n, 0] = Fn_VibroFeeder(self.com, self.df, n,self.filename)
                self.listofvibrofeeder.append(self.df.iloc[n,0])
                n = n + 1

            # per area wise device list
            # Declear empty list

            for area in self.listofvfarea:
                list1 = []
                for item in self.listofvibrofeeder:
                    if item.areaname == area:
                        list1.append(item)
                self.devicelistperarea.append(list1)

            keys = self.listofvfarea
            values = self.devicelistperarea[1:]
            # Declear empty list
            self.dictionary = dict(zip(keys,values))


        except Exception as e :
            log_exception(e)
            level = logging.ERROR
            messege = 'Event:' + "callallvibofeeder" + str(e.args)
            logger.log(level, messege)



    @property
    def listofvibrofeedermotor(self):
        if len(self.listofvibrofeeder) > 0:
            return self.listofvibrofeeder

    @property
    def listofvibrofeederareas(self):
        return self.listofvfarea

    @property
    def getmotordictionary(self):
        return self.dictionary



