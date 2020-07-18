from logger import *
from fn_ProportionValve_V3 import *
import logging
import threading

logger = logging.getLogger("main.log")


class Cal_AllProportionalValves:

    def __init__(self,df,com,filename):
        self.df = df
        self.filename = filename
        self.mylock = threading.Lock()
        self.com = com
        self.listofPropotionalValve = []
        self.listofvfarea = []
        self.devicelistperarea = [[]]
        self.setup()


    def setup(self):
        try:
            # Make a lis of area
            self.listofProportionalvalvearea = list(set(self.df['Sub-Area']))

            # Make a lis of devices
            n =0
            self.listofPropotionalValve.clear()
            while n< len(self.df.index):
                self.df.iloc[n, 0] = FN_ProportionalValve(self.com, self.df,  n,self.filename)
                self.listofPropotionalValve.append(self.df.iloc[n,0])
                n = n + 1

            # per area wise device list
            # Declear empty list

            for area in self.listofProportionalvalvearea:
                list1 = []
                for item in self.listofPropotionalValve:
                    if str(item.areaname) == str(area):
                        list1.append(item)
                self.devicelistperarea.append(list1)

            keys = self.listofProportionalvalvearea
            values = self.devicelistperarea[1:]
            # Declear empty list
            self.dictionary = dict(zip(keys,values))


        except Exception as e :
            log_exception(e)
            level = logging.ERROR
            messege = 'Event:' + "Cal_AllProportionalValves" + str(e.args)
            logger.log(level, messege)




    @property
    def listofPropotionalvalves(self):
        if len(self.listofPropotionalValve) > 0:
            return self.listofPropotionalValve

    @property
    def listofpropotionvalvesareas(self):
        return self.listofProportionalvalvearea

    @property
    def getmotordictionary(self):
        return self.dictionary



