from logger import *
from fn_conveyor1D_V3 import *
import logging
import threading


setup_logging_to_file("allconveyor.log")
logger = logging.getLogger("main.log")


class Cal_AllConveyor1D:

    def __init__(self,df,com):
        self.df = df
        self.mylock = threading.Lock()
        self.com = com
        self.logger = logger
        self.listofconveyor1D = []
        self.listofconveyorarea = []
        self.devicelistperarea = [[]]
        self.setup()


    def setup(self):
        try:
            # Make a lis of area
            self.listofconveyorarea = list(set(self.df['Sub-Area']))

            # Make a list of devices
            n =0
            self.listofconveyor1D.clear()
            while n< len(self.df.index):
                self.df.iloc[n, 0] = Fn_Conveyor1D(self.com, self.df, n)
                self.listofconveyor1D.append(self.df.iloc[n,0])
                n = n + 1

            # per area wise device list
            # Declear empty list

            for area in self.listofconveyorarea:

                list1 = []
                for item in self.listofconveyor1D:
                    if item.areaname == area:
                        list1.append(item)
                self.devicelistperarea.append(list1)

            keys = self.listofconveyorarea
            values = self.devicelistperarea[1:]
            # Declear empty list
            self.dictionary = dict(zip(keys, values))

        except Exception as e :
            log_exception(e)
            level = logging.ERROR
            messege = 'Event:' + "callallconveyor" + str(e.args)
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
    def listofconveyorareas(self):
        return self.listofconveyorarea

    @property
    def getmotordictionary(self):
        return self.dictionary

    @property
    def listofconveyors(self):
        if len(self.listofconveyor1D) > 0:
            return self.listofconveyor1D



