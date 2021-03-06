from logger import *
from fn_damper import *
import logging
import threading

logger = logging.getLogger("main.log")


class Cal_AllDamper:
    def __init__(self, df, com,filename):
        self.filename = filename
        self.df = df
        self.com = com
        self.listofdamper = []
        self.listofdamperarea = []
        self.devicelistperarea = [[]]
        self.setup()

    def setup(self):
        try:

            # Make a lis of area
            self.listofdamperarea = list(set(self.df['Sub-Area']))

            # Make a lis of devices

            n = 0
            self.listofdamper.clear()
            while n < len(self.df.index):
                self.df.iloc[n, 0] = Fn_Damper(self.com, self.df, n,self.filename)
                self.listofdamper.append(self.df.iloc[n, 0])
                n = n + 1

            # per area wise device list
            # Declear empty list
            for area in self.listofdamperarea:
                list1 = []
                for item in self.listofdamper:

                    if str(item.areaname) == str(area):
                        list1.append(item)
                self.devicelistperarea.append(list1)

            keys = self.listofdamperarea
            values = self.devicelistperarea[1:]

            # Declear empty list
            self.dictionary = dict(zip(keys, values))




        except Exception as e:
            log_exception(e)
            print("Error messege is:",e.args)
            level = logging.ERROR
            messege = 'Event:' + "callallsov2s" + str(e.args)
            logger.log(level, messege)

    def __getstate__(self):
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        del state['mylock']
        return state

    def __setstate__(self, state):
        # Restore instance attributes.
        self.__dict__.update(state)

    @property
    def listofallsov2s(self):
        if len(self.listofdamper) > 0:
            return self.listofdamper


    @property
    def listofsov2sareas(self):
        return self.listofdamperarea

    @property
    def getmotordictionary(self):
        return self.dictionary