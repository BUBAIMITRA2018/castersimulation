from logger import *
from fn_analogTx_V3 import *
import logging
import threading

logger = logging.getLogger("main.log")


class Cal_AllAnalogInputs:

    def __init__(self,df,com,filename):
        self.mylock = threading.Lock()
        self.df = df
        self.filename = filename
        self.com = com
        self.listofanalogobjects = []
        self.listofanalogarea = []
        self.devicelistperarea = [[]]
        self.setup()


    def setup(self):
        try:

            # Make a lis of area
            self.listofanalogarea = list(set(self.df['Sub-Area']))

            # Make a list of devices
            n= 0
            self.listofanalogobjects.clear()
            while n< len(self.df.index):
                self.df.iloc[n, 0] = Fn_AnalogTx(self.com, self.df, n,self.filename)
                self.listofanalogobjects.append(self.df.iloc[n,0])
                n = n + 1

            # per area wise device list
            # Declear empty list
            for area in self.listofanalogarea:
                list1 = []
                for item in self.listofanalogobjects:
                    if str(item.areaname) == str(area):
                        list1.append(item)
                self.devicelistperarea.append(list1)


            keys = self.listofanalogarea
            values = self.devicelistperarea[1:]
            # Declear empty list
            self.dictionary = dict(zip(keys, values))




        except Exception as e:
            level = logging.ERROR
            messege = 'Event:' + "callallanalogs" + str(e.args)
            logger.log(level, messege)
            log_exception(e)

    def __getstate__(self):
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        del state['mylock']
        return state

    def __setstate__(self, state):
        # Restore instance attributes.
        self.__dict__.update(state)


    @property
    def listofanalogs(self):
        if len(self.listofanalogobjects) > 0:
            return self.listofanalogobjects

    @property
    def listofanalogareas(self):
        return self.listofanalogarea

    @property
    def getanalogdictionary(self):
        return self.dictionary

