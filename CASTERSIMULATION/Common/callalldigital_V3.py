from logger import *
from fn_digitalsignal_V3 import *
import logging
import threading

logger = logging.getLogger("main.log")


class Cal_AllDigital:

    def __init__(self,df,com,filename):
        self.mylock = threading.Lock()
        self.df = df
        self.com = com
        self.filename = filename
        self.listofdigital = []
        self.listofdigitalarea = []
        self.devicelistperarea = [[]]
        self.setup()

    def setup(self):
        try:

            # Make a lis of area
            self.listofdigitalarea = list(set(self.df['Sub-Area']))
            # Make a list of devices
            n =0
            self.listofdigital.clear()
            while n< len(self.df.index):
                self.df.iloc[n, 0] = Fn_digitalsignal(self.com, self.df, n,self.filename)
                self.listofdigital.append(self.df.iloc[n,0])
                n = n + 1



            # per area wise device list
            # Declear empty list
            for area in self.listofdigitalarea:
                list1 = []
                for item in self.listofdigital:

                    if str(item.areaname) == str(area):
                        list1.append(item)

                self.devicelistperarea.append(list1)

            keys = self.listofdigitalarea

            values = self.devicelistperarea[1:]

            # Declear empty list
            self.dictionary = dict(zip(keys,values))



        except Exception as e :
            log_exception(e)
            level = logging.ERROR
            messege = 'Event:' + "callalldigitalinput" + str(e.args)
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
    def listofdigitalinput(self):
        return self.listofdigital

    @property
    def listofdigitalareas(self):
        return self.listofdigitalarea


    @property
    def getdigitaldictionary(self):
        return self.dictionary


