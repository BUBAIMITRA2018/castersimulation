from logger import *
# from fn_motor1D_V3 import *
from  fn_dummybar_V3 import *
import logging
import threading


setup_logging_to_file("allmotor1D.log")
logger = logging.getLogger("main.log")


class Cal_AllDummyBar:

    def __init__(self,df,com,filename):
        self.mylock = threading.Lock()
        self.df = df
        self.com = com
        self.filename = filename
        self.listodummybar = []
        self.listofdummybararea = []
        self.devicelistperarea = [[]]
        self.setup()

    def setup(self):
        try:
            # print("dictionary is executed ", self.dictionary)

            # Make a lis of area
            self.listofdummybararea = list(set(self.df['Sub-Area']))

            # Make a list of devices

            n =0
            self.listodummybar.clear()
            while n< len(self.df.index):
                self.df.iloc[n, 0] = Fn_DummyBar(self.com, self.df, n,self.filename)
                self.listodummybar.append(self.df.iloc[n,0])
                n = n + 1



            # per area wise device list
            # Declear empty list
            for area in self.listofdummybararea:
                list1 = []
                for item in self.listodummybar:

                    if str(item.areaname) == str(area):
                        list1.append(item)

                self.devicelistperarea.append(list1)

            keys = self.listofdummybararea

            values = self.devicelistperarea[1:]


            # Declear empty list
            self.dictionary = dict(zip(keys,values))






        except Exception as e :
            log_exception(e)
            level = logging.ERROR
            messege = 'Event:' + "callalldummybar" + str(e.args)
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
    def listofdummybars(self):
        return self.listodummybar

    @property
    def listofdummybarareas(self):
        return self.listofdummybararea


    @property
    def getdummybardictionary(self):
        return self.dictionary
