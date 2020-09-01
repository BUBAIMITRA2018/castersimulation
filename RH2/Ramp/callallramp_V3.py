from logger import *
from fn_ramp_V3 import *
import logging
import threading

logger = logging.getLogger("main.log")


class Cal_AllRampInputs:

    def __init__(self,df,com,filename):
        self.mylock = threading.Lock()
        self.df = df
        self.filename = filename
        self.com = com
        self.listoframpobjects = []
        self.listoframparea = []
        self.devicelistperarea = [[]]
        self.setup()


    def setup(self):
        try:

            # Make a lis of area
            self.listoframparea = list(set(self.df['Sub-Area']))
            print(self.listoframparea)

            # Make a list of devices
            n= 0
            self.listoframpobjects.clear()
            while n< len(self.df.index):
                self.df.iloc[n, 0] = Fn_Ramp(self.com, self.df, n,self.filename)
                self.listoframpobjects.append(self.df.iloc[n,0])
                n = n + 1

            # per area wise device list
            # Declear empty list
            for area in self.listoframparea:
                list1 = []
                for item in self.listoframpobjects:
                    if str(item.areaname) == str(area):
                        list1.append(item)
                self.devicelistperarea.append(list1)


            keys = self.listoframparea
            values = self.devicelistperarea[1:]
            # Declear empty list
            self.dictionary = dict(zip(keys, values))
            print(self.dictionary)






        except Exception as e:
            level = logging.ERROR
            messege = 'Event:' + "callallanalogs" + str(e.args)
            logger.log(level, messege)
            log_exception(e)




    @property
    def listoframps(self):
        if len(self.listoframpobjects) > 0:
            return self.listoframpobjects

    @property
    def listofanalogareas(self):
        return self.listoframparea

    @property
    def getanalogdictionary(self):
        return self.dictionary

