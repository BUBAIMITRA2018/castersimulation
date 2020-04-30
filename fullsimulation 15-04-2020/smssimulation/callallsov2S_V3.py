from logger import *
from fn_sov2S_V3 import *
import logging
import threading

setup_logging_to_file("allsov2S.log")
logger = logging.getLogger("main.log")


class Cal_AllSov2S:
    def __init__(self, df, com):
        self.df = df
        self.com = com
        self.listofsov2s = []
        self.listofsov2sarea = []
        self.devicelistperarea = [[]]
        self.setup()

    def setup(self):
        try:

            # Make a lis of area
            self.listofsov2sarea = list(set(self.df['Sub-Area']))

            # Make a lis of devices

            n = 0
            self.listofsov2s.clear()
            while n < len(self.df.index):
                self.df.iloc[n, 0] = Fn_Sov2S(self.com, self.df, n)
                self.listofsov2s.append(self.df.iloc[n, 0])
                n = n + 1

            # per area wise device list
            # Declear empty list
            for area in self.listofsov2sarea:
                list1 = []
                for item in self.listofsov2s:

                    if item.areaname == area:
                        list1.append(item)
                self.devicelistperarea.append(list1)

            keys = self.listofsov2sarea
            values = self.devicelistperarea[1:]

            # Declear empty list
            self.dictionary = dict(zip(keys, values))
            print(self.dictionary)



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
        if len(self.listofsov2s) > 0:
            return self.listofsov2s


    @property
    def listofsov2sareas(self):
        return self.listofsov2sarea

    @property
    def getmotordictionary(self):
        return self.dictionary